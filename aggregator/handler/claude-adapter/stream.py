"""Claude Code stream-json, one line at a time, into the event names the OpenAI panel reads.

The panel (aggregator/handler/codex/runtime/panel.html, consume()) renders Codex app-server events:
turn/started, item/agentMessage/delta, item/started and item/completed (agentMessage, userMessage,
commandExecution, dynamicToolCall, fileChange, webSearch), item/commandExecution/outputDelta,
turn/completed, item/tool/requestUserInput, rplace/questionAnswered and error. A Translator turns
one Claude turn's stream into those names. It writes nothing; the actor appends what it returns to
events.jsonl, and every raw line stays in the turn's stream.jsonl, so nothing is lost when a line
has no panel form.

What a reader of the panel sees:
- the analyst's words, streamed and then whole, in the conversation;
- every tool call as one row: Bash with its command, a file tool with its path, and the output when
  it returns;
- every helper (Agent or Task tool) as one row whose text is the full prompt the analyst wrote for
  it, then the helper's reply; the helper's own tool calls and words as rows marked with its name;
- context compaction and permission refusals as rows;
- never the private reasoning (thinking blocks), as for Codex.

The message shapes come from the Claude Code headless documentation and the CLI's --help (2.1.289);
they are not yet checked against a live stream. adapter/probe.py does that on the Mac.
"""
import json

LIMIT = 20000   # characters of one tool output or prompt per event; the rest stays in stream.jsonl
KIND = {'Bash': 'commandExecution', 'BashOutput': 'commandExecution', 'KillShell': 'commandExecution',
        'Write': 'fileChange', 'Edit': 'fileChange', 'MultiEdit': 'fileChange', 'NotebookEdit': 'fileChange',
        'WebSearch': 'webSearch', 'WebFetch': 'webSearch'}
HELPERS = ('Agent', 'Task')


def clip(text, n=LIMIT):
    text = text if isinstance(text, str) else json.dumps(text, ensure_ascii=False)
    return text if len(text) <= n else text[:n] + '\n[%d more characters in the turn\'s stream.jsonl]' % (len(text) - n)


def flatten(content):
    """A tool result's content: a string, or blocks of text and images."""
    if content is None:
        return ''
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for b in content:
            if isinstance(b, dict) and b.get('type') == 'text':
                parts.append(b.get('text') or '')
            elif isinstance(b, dict) and b.get('type') == 'image':
                parts.append('[image]')
            else:
                parts.append(json.dumps(b, ensure_ascii=False))
        return '\n'.join(parts)
    return json.dumps(content, ensure_ascii=False)


def title(name, args):
    """The row's label: what a reader needs to know the call at a glance."""
    a = args if isinstance(args, dict) else {}
    if name == 'Bash':
        return 'Bash: ' + str(a.get('command', ''))
    if name in ('Read', 'Write', 'Edit', 'MultiEdit', 'NotebookEdit'):
        return '%s %s' % (name, a.get('file_path') or a.get('notebook_path') or '')
    if name in ('Grep', 'Glob'):
        return '%s %s' % (name, a.get('pattern', ''))
    if name in HELPERS:
        return 'Helper (%s): %s' % (a.get('subagent_type') or 'general-purpose', a.get('description', ''))
    if name == 'WebFetch':
        return 'WebFetch ' + str(a.get('url', ''))
    if name == 'WebSearch':
        return 'WebSearch ' + str(a.get('query', ''))
    return name


class Translator:
    def __init__(self, thread, turn):
        self.thread, self.turn = thread, turn
        self.n = 0
        self.tools = {}       # tool_use id -> what its result row needs
        self.final_texts = {}  # message id -> text blocks seen in whole messages
        self.stream_texts = {}  # message id -> text blocks seen in stream events
        self.block = {}       # (message id, block index) -> text ordinal
        self.current = None   # the top-level message being streamed
        self.init = None      # the system/init line
        self.result = None    # the result line

    def next(self):
        self.n += 1
        return self.n

    def params(self, **p):
        p.update(threadId=self.thread, turnId=self.turn)
        return p

    def note(self, key, head, text, status='completed'):
        """A row in the panel that is no tool call: compaction, a refusal, a helper's words."""
        return ('item/completed', self.params(item={'type': 'dynamicToolCall', 'id': key, 'command': head,
                                                    'status': status, 'aggregatedOutput': clip(text)}))

    @staticmethod
    def text_id(message, ordinal):
        return 'msg-%s-%d' % (message, ordinal)

    def helper_name(self, parent):
        rec = self.tools.get(parent) or {}
        return '"%s"' % rec['description'] if rec.get('description') else parent[-8:]

    def feed(self, m):
        if not isinstance(m, dict):
            return []
        kind, parent = m.get('type'), m.get('parent_tool_use_id')
        if kind == 'system':
            return self.system(m)
        if kind == 'stream_event':
            return self.partial(m.get('event') or {}, parent)
        if kind == 'assistant':
            return self.assistant(m.get('message') or {}, parent)
        if kind == 'user':
            return self.user(m.get('message') or {}, parent)
        if kind == 'result':
            self.result = m
        return []   # result, and kinds without a panel form: kept in stream.jsonl only

    def system(self, m):
        sub = str(m.get('subtype') or '')
        if sub == 'init':
            self.init = m
            return []
        if sub == 'compact_boundary':
            return [self.note('compact-%d' % self.next(), 'Context compacted',
                              json.dumps(m.get('compact_metadata') or {}, ensure_ascii=False))]
        if 'denied' in sub:   # the headless docs name permission_denied; its fields are not pinned yet
            rest = {k: v for k, v in m.items() if k not in ('type', 'subtype', 'session_id', 'uuid')}
            return [self.note('denied-%d' % self.next(), 'Permission refused', json.dumps(rest, ensure_ascii=False),
                              status='failed')]
        return []

    def partial(self, e, parent):
        if parent:
            return []   # a helper's words arrive whole (--forward-subagent-text)
        et = e.get('type')
        if et == 'message_start':
            self.current = (e.get('message') or {}).get('id')
        elif et == 'content_block_start':
            if (e.get('content_block') or {}).get('type') == 'text' and self.current:
                k = self.stream_texts.get(self.current, 0)
                self.stream_texts[self.current] = k + 1
                self.block[(self.current, e.get('index'))] = k
        elif et == 'content_block_delta':
            d = e.get('delta') or {}
            k = self.block.get((self.current, e.get('index')))
            if d.get('type') == 'text_delta' and k is not None:
                return [('item/agentMessage/delta', self.params(itemId=self.text_id(self.current, k),
                                                                 delta=d.get('text') or ''))]
        return []

    def assistant(self, msg, parent):
        out, mid = [], msg.get('id') or 'm%d' % self.next()
        for b in msg.get('content') or []:
            if not isinstance(b, dict):
                continue
            bt = b.get('type')
            if bt == 'text' and (b.get('text') or '').strip():
                if parent:
                    out.append(self.note('helper-text-%d' % self.next(), 'Helper %s says' % self.helper_name(parent),
                                         b['text']))
                else:
                    k = self.final_texts.get(mid, 0)
                    self.final_texts[mid] = k + 1
                    out.append(('item/completed', self.params(item={'type': 'agentMessage', 'id': self.text_id(mid, k),
                                                                    'text': b['text']})))
            elif bt in ('tool_use', 'server_tool_use'):
                out.append(self.tool_start(b, parent))
            # thinking and redacted_thinking: private reasoning, never shown
        return out

    def tool_start(self, b, parent):
        tid = b.get('id') or 'tool-%d' % self.next()
        name = b.get('name') or 'tool'
        args = b.get('input') if isinstance(b.get('input'), dict) else {}
        kind = KIND.get(name, 'dynamicToolCall')
        head = title(name, args)
        if parent:
            head = 'Helper %s · %s' % (self.helper_name(parent), head)
        rec = {'type': kind, 'command': head, 'name': name, 'parent': parent}
        item = {'type': kind, 'id': tid, 'command': head}
        if name in HELPERS:
            rec.update(prompt=str(args.get('prompt', '')), description=str(args.get('description', '')))
            item['aggregatedOutput'] = 'The prompt the analyst wrote for this helper:\n' + clip(rec['prompt'])
        elif name != 'Bash':
            item['aggregatedOutput'] = 'Input: ' + clip(json.dumps(args, ensure_ascii=False))
        self.tools[tid] = rec
        return ('item/started', self.params(item=item))

    def user(self, msg, parent):
        out, content = [], msg.get('content')
        if isinstance(content, str):
            content = [{'type': 'text', 'text': content}]
        for b in content or []:
            if not isinstance(b, dict):
                continue
            bt, text = b.get('type'), b.get('text') or ''
            if bt == 'tool_result':
                out.append(self.tool_done(b))
            elif bt == 'text' and text.strip() and parent:
                # a helper's first message is the prompt it was given; show it only if it differs from
                # the prompt already on the helper's row
                if text.strip() != (self.tools.get(parent) or {}).get('prompt', '').strip():
                    out.append(self.note('helper-prompt-%d' % self.next(),
                                         'Helper %s · prompt received' % self.helper_name(parent), text))
            elif bt == 'text' and text.strip():
                out.append(self.note('context-%d' % self.next(), 'Added to the conversation', text))
        return out

    def tool_done(self, b):
        tid = b.get('tool_use_id') or 'tool-%d' % self.next()
        rec = self.tools.get(tid) or {'type': 'dynamicToolCall', 'command': 'Tool result', 'name': ''}
        text = clip(flatten(b.get('content')))
        if rec.get('name') in HELPERS:
            text = ('The prompt the analyst wrote for this helper:\n%s\n\nThe helper\'s reply:\n%s'
                    % (clip(rec.get('prompt', '')), text))
        return ('item/completed', self.params(item={'type': rec['type'], 'id': tid, 'command': rec['command'],
                                                    'status': 'failed' if b.get('is_error') else 'completed',
                                                    'aggregatedOutput': text}))

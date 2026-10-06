"""One cancellable HTTP operation. Credential arrives on stdin, never argv or disk."""
import json, sys, urllib.request, urllib.error

def main():
    args=json.load(sys.stdin); secret=args['key']; path=args['path']
    if path!='chat/completions' and not path.startswith('generation?id='):
        raise ValueError('Unsupported OpenRouter endpoint')
    headers={'Authorization':'Bearer '+secret,'Content-Type':'application/json','X-OpenRouter-Title':'rplace research fleet'}
    body=args.get('body')
    request=urllib.request.Request('https://openrouter.ai/api/v1/'+path,
        data=None if body is None else json.dumps(body).encode(),headers=headers)
    # Never forward credentials across redirects.
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*a,**kw): return None
    try:
        with urllib.request.build_opener(NoRedirect).open(request,timeout=args['timeout']) as response:
            answer={'data':json.load(response)}
    except urllib.error.HTTPError as e:
        answer={'error':'OpenRouter HTTP '+str(e.code),'http_status':e.code}
    except Exception as e:
        answer={'error':'OpenRouter transport or response error: '+type(e).__name__}
    print(json.dumps(answer).replace(secret,'[REDACTED]'))

if __name__=='__main__': main()

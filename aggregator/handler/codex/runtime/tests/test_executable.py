"""Terminal PATH must not decide whether the installed native runtime is usable."""
import contextlib, io, json, os, sys, tempfile, tomllib, unittest
from pathlib import Path
from unittest.mock import patch
from runtime import cli, native
from runtime.common import Error, TMP

class ExecutableTests(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=TMP)
        self.root=Path(self.temp.name)
        self.app=self.root/'Application With Spaces.app/Contents/MacOS/codex'
        self.app.parent.mkdir(parents=True)
        self.app.write_text('#!/bin/sh\nexit 0\n');self.app.chmod(0o755)
    def tearDown(self): self.temp.cleanup()
    def test_terminal_without_path_finds_app(self):
        with patch.dict(os.environ,{'PATH':''}),patch.object(native,'bundled_executables',return_value=[self.app]):
            self.assertEqual(native.resolve_executable(),str(self.app.resolve()))
    def test_path_install_takes_precedence(self):
        other=self.root/'codex';other.write_text('#!/bin/sh\nexit 0\n');other.chmod(0o755)
        with patch.dict(os.environ,{'PATH':str(self.root)}),patch.object(native,'bundled_executables',return_value=[self.app]):
            self.assertEqual(native.resolve_executable(),str(other.resolve()))
    def test_missing_explicit_runtime_never_falls_back(self):
        with patch.object(native,'bundled_executables',return_value=[self.app]):
            with self.assertRaisesRegex(Error,'no fallback'):native.resolve_executable(self.root/'missing')
    def test_absent_or_nonexecutable_install_has_clear_error(self):
        self.app.chmod(0o644)
        with patch.dict(os.environ,{'PATH':''}),patch.object(native,'bundled_executables',return_value=[self.app]):
            self.assertIsNone(native.resolve_executable(required=False))
            with self.assertRaisesRegex(Error,'not found on PATH'):native.resolve_executable()
    def test_login_uses_absolute_app_and_private_home(self):
        with patch.dict(os.environ,{'PATH':''}),patch.object(native,'bundled_executables',return_value=[self.app]),patch.object(native,'configure'),patch.object(cli.subprocess,'call',return_value=0) as call:
            self.assertEqual(cli.main(['login']),0)
        args=call.call_args
        self.assertEqual(args.args[0],[str(self.app.resolve()),'login'])
        self.assertEqual(args.kwargs['env']['CODEX_HOME'],str(cli.DATA/'login'))
        self.assertEqual(args.kwargs['cwd'],cli.ROOT)
    def test_doctor_reports_same_executable(self):
        output=io.StringIO()
        with patch.dict(os.environ,{'PATH':''}),patch.object(native,'bundled_executables',return_value=[self.app]),patch.object(cli,'scientific_dependencies',return_value={}),contextlib.redirect_stdout(output):
            self.assertEqual(cli.main(['doctor']),0)
        self.assertEqual(json.loads(output.getvalue())['codex'],str(self.app.resolve()))
    def test_venv_and_base_python_readable_without_opening_private_state(self):
        home=self.root/'actor/native';workspace=self.root/'actor/workspace'
        for probe in (False,True):
            native.configure(home,'gpt-6-sol','medium',workspace,probe=probe)
            config=tomllib.loads((home/'config.toml').read_text())
            fs=config['permissions']['rplace']['filesystem']
            for prefix in (sys.prefix,sys.base_prefix,sys.base_exec_prefix):
                self.assertEqual(fs[str(Path(prefix).resolve())],'read')
            self.assertNotIn(str(TMP.parent),fs)
            self.assertEqual(fs[str(workspace)],'deny' if probe else 'read')
            if not probe:self.assertEqual(fs[str(workspace/'out/_transcripts')],'deny')
    def test_tool_shell_keeps_managed_python_and_actor_temp(self):
        home=self.root/'actor/native';native.configure(home,'gpt-6-sol','medium')
        config=tomllib.loads((home/'config.toml').read_text())
        policy=config['shell_environment_policy'];settings=policy['set']
        self.assertFalse(config['allow_login_shell'])
        self.assertEqual(policy['inherit'],'core')
        self.assertIn('PYTHONHOME',policy['exclude']);self.assertIn('PYTHONPATH',policy['exclude'])
        self.assertEqual(settings['PATH'].split(':')[0],str(Path(sys.executable).parent))
        for name in ('TMPDIR','TMP','TEMP'):
            self.assertEqual(settings[name],str(home.parent/'scratch/tmp'))
    def test_terminal_answer_uses_current_actor_question(self):
        state={'actors':[{'id':'analyst','questions':[{'requestKey':'pending-key','questions':[{'id':'choice'}]}]}]}
        with patch.object(cli,'request',side_effect=[state,{'new_turn_started':False}]) as call:
            cli.chat_request('analyst','/answer My choice')
        self.assertEqual(call.call_args.args[0],{'action':'answer','actor':'analyst','request':'pending-key','answers':{'choice':'My choice'}})
    def test_noninteractive_workers_do_not_receive_question_tool(self):
        home=self.root/'worker/native';native.configure(home,'gpt-6-sol','medium',interactive=False)
        self.assertFalse(tomllib.loads((home/'config.toml').read_text())['features']['default_mode_request_user_input'])

# Use the live panel from your phone

Target length: under 400 words.

The Mac runs the agents, files and checkpoints. Your phone uses the same conversations through a private HTTPS connection. Keep the Mac awake and online. Closing the phone browser leaves work running. A screenshot, downloaded page or OPENAI-LIVE.html attachment is not a phone connection. That launcher works on the Mac only.

## Set up once

1. Install Tailscale on the Mac and phone. Sign into the same account on both.
2. On macOS 15 or later: System Settings, General, Login Items & Extensions, Network Extensions. Enable Tailscale, approve with Touch ID or your password, and allow the VPN configuration. [Official Mac steps](https://tailscale.com/docs/concepts/macos-sysext).
3. Keep v42 untouched and start the separate v43 controller first. In a separate Mac terminal, run:

```bash
"$HOME/Jail/.rplace-runtime/tools/python311/venv/bin/python3" \
  "$HOME/Jail/r-place/aggregator/handler/codex/run.py" phone
```

This checks sign-in, finds the Mac's private hostname, starts or reuses the separate gateway and configures Tailscale Serve on HTTPS port 8444. It refuses conflicting services and public Funnel exposure. It sends no research command. Existing actors keep their conversations and files.

If HTTPS setup needs approval or times out, enable MagicDNS and HTTPS Certificates on the Tailscale admin console DNS page, then repeat the command. [Official HTTPS steps](https://tailscale.com/docs/how-to/set-up-https-certificates). An existing route is reused. Add `--check` to check status without starting the gateway or exposing a link.

Open the printed private link in your phone browser with Tailscale connected. Keep that link out of Git and shared messages. Credentials and gateway logs stay in the private runtime folder beside the repository. The gateway stays running after this terminal closes. After a Mac restart, restore the controller normally and run `phone` again.

## Use and check

Choose the study and its current stage/leg. Read Conversation, expand tool activity, send guidance and answer pending questions. Selection does not start an agent. Closed legs open as separate interviews.

Before relying on access away from home, test over mobile data: read an existing conversation, reload and reconnect. The setup command verifies the Mac route; only this phone test confirms remote access.

To invalidate links without stopping actors, run `run.py remote-revoke`. Obtain the replacement with `run.py remote-link`. To disable the HTTPS listener, use the Tailscale CLI:

```bash
tailscale serve --https=8444 off
```

Never retry an uncertain research command automatically. Reconnect and inspect Jobs first.

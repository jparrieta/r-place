#!/usr/bin/env bash
# Always launched by step.sh. The analyst sees only 00_GIVE-THE-AGENT/.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
RUN="$(harness_run_dir)"; G="$RUN/CONTROL/harness/protocol_guard.py"
exec python3 "$G" locked "$RUN" python3 "$G" launch "$RUN" "$@"

from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent / "tools"))
from chunk_compare import main
main()

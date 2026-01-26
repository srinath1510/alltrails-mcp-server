import sys
from pathlib import Path

# Add the project root to sys.path so tests can import from app
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

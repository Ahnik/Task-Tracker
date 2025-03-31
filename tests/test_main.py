import pytest
import subprocess
import os
import sys
from pathlib import Path
import json

# Add the app directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

# Import functions from main.py
from main import add_task, update_task, delete_task, mark_in_progress, mark_done, list_tasks
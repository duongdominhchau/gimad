import os
from pathlib import Path

MIGRATION_DIR = Path(os.environ.get("GIMAD_MIGRATION_DIR", "data_migrations")).resolve()
PERMANENT_DIR = "permanent"
ONEOFF_DIR = "oneoff"

CONFIG_NAME = "gimad"

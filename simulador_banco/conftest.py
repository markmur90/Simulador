import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).resolve().parent / 'simulador_banco'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simulador_banco.simulador_banco.settings')
os.environ.setdefault('FIELD_ENCRYPTION_KEY', 'DbQG9CWLvBRa8Iu9pv9fJDVURCdKYQQErlZ9oCYGsY8=')
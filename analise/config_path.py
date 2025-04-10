import sys
import os

# Caminho absoluto até a raiz do projeto
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Garante que o caminho raiz esteja no sys.path
if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)
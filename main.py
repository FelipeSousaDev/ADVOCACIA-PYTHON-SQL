import sys
import os

    # Adiciona o diretório raiz do projeto ao PATH
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

    # Importa a função principal para rodar o app
from frontend.app import run_app

if __name__ == '__main__':
    run_app()

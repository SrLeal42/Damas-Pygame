import sys
import os

def resource_path(relative_path):
    """Retorna o caminho absoluto para os recursos, compatível com PyInstaller"""
    try:
        # PyInstaller cria uma pasta temporária e armazena o path em _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
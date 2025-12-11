# utils.py
from PIL import Image, ImageDraw
import os
import sys

def resource_path(relative_path):
    """ Retorna o caminho absoluto do recurso, funciona em dev e no PyInstaller """
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se estiver rodando no VS Code, usa a pasta atual
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def limpar_dados(artist_raw, title_raw, album_raw):
    """Limpa a sujeira do Apple Music (Hifens e Travessões)"""
    # Limpa Artista (Remove ' — Album')

    clean_artist = artist_raw
    clean_title = title_raw
    found_album = album_raw

    # --- CASO 1: Álbum grudado no Artista (ex: "Artista — Album") ---
    if " — " in artist_raw:
        parts = artist_raw.split(" — ")
        clean_artist = parts[0]
        # Se o Windows não deu álbum, ou se o álbum for igual ao título (bug comum),
        # usa essa segunda parte do texto como o álbum real.
        if not found_album or found_album == title_raw:
            if len(parts) > 1:
                found_album = parts[1]

    # --- CASO 2: Álbum grudado no Título (ex: "Album - Musica") ---
    if " - " in title_raw:
        parts = title_raw.split(" - ")
        if len(parts) >= 2:
            clean_title = parts[-1] 
            
    return clean_artist, clean_title, found_album

def criar_icone_padrao():
    """Gera o ícone vermelho via código"""
    width = 64
    height = 64
    color1 = "red"
    color2 = "black"
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    return image

def abrir_log(logfile):
    if os.path.exists(logfile):
        os.startfile(logfile)
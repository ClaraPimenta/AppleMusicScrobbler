import threading
import asyncio
import logging
import sys
import pystray
import os

import configs
import utils
import scrobbler

# Configuração encoding
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')

logging.basicConfig(
    filename=configs.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# --- ESTADO GLOBAL ---

tray_icon = None
current_status = "Iniciando..."

# --- FUNÇÕES DE MENU ---

def get_status_label(item):
    """Retorna o texto da música para o 1º item do menu"""
    return f"🎵 {current_status}"

def get_toggle_label(item):
    """Muda o texto do botão Ativar/Desativar"""
    if scrobbler.PAUSED:
        return "Retomar Scrobbling"
    else:
        return "Pausar Scrobbling"

def on_toggle_click(icon, item):
    """Ação ao clicar em Pausar/Retomar"""
    novo_estado = not scrobbler.PAUSED
    scrobbler.set_paused(novo_estado)
    
    # Força atualização visual do ícone (muda cor ou texto)
    if novo_estado: # Se pausou
        icon.title = "Scrobbler Pausado"
    else:
        icon.title = "Retomando..."

# --- LOOP ---

def ui_updater(text, notify=False):
    global tray_icon, current_status
    current_status = text
    
    if tray_icon:
        tray_icon.title = text # Tooltip (mouse em cima)
        # removemos o notify() para não aparecer banner roxo
        
        # Atualiza o menu para refletir a nova música
        tray_icon.update_menu()

def start_background_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(scrobbler.run_loop(ui_updater))

def on_exit(icon, item):
    icon.stop()
    os._exit(0)

def on_open_log(icon, item):
    utils.abrir_log(configs.LOG_FILE)

if __name__ == "__main__":
    t = threading.Thread(target=start_background_loop)
    t.daemon = True
    t.start()

    # --- MENU INTELIGENTE ---
    # Item 1: A música
    # Item 2: Separador
    # Item 3: Botão de Pausa (checkbox)
    
    menu = pystray.Menu(
        pystray.MenuItem(get_status_label, action=None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(get_toggle_label, on_toggle_click, checked=lambda item: not scrobbler.PAUSED),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Abrir Log de Erros', on_open_log),
        pystray.MenuItem('Sair', on_exit)
    )
    
    icon_path = utils.resource_path("app_icon.ico")
    try:
        icon_img = utils.Image.open(icon_path)
    except:
        icon_img = utils.criar_icone_padrao()

    # Configura o clique esquerdo (default=True) para ser 'neutro',
    # pois o usuário deve clicar para abrir o menu.
    tray_icon = pystray.Icon(configs.APP_NAME, icon_img, "Iniciando...", menu)
    tray_icon.run()
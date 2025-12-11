import asyncio
import time
import logging
import services
import utils
import configs

# --- CONTROLE GLOBAL DE ESTADO ---
PAUSED = False # Começa ativado

def set_paused(status):
    """Função que o main.py vai chamar para pausar/despausar"""
    global PAUSED
    PAUSED = status

async def run_loop(update_ui_callback):
    logging.info("Scrobbler Engine iniciado.")
    
    network = services.connect_lastfm()
    if not network:
        update_ui_callback("Erro de Login", notify=True)
        return

    current_signature = None
    start_time = 0
    scrobbled = False
    
    # Cache
    final_artist, final_title, final_album = "", "", ""

    while True:
        try:
            # --- CHECAGEM DE PAUSA ---
            if PAUSED:
                # Se estiver pausado, avisa a interface e dorme
                update_ui_callback("Scrobbler Pausado")
                await asyncio.sleep(2)
                continue
            # -------------------------

            media = await services.get_windows_media_info()
            
            if not media or "Apple" not in media['app_id']:
                update_ui_callback("Aguardando música...")
                await asyncio.sleep(configs.CHECK_INTERVAL)
                continue

            c_artist, c_title, c_album = utils.limpar_dados(media['artist'], media['title'], media['album'])
            new_sig = f"{c_artist} - {c_title} ({c_album})"

            if new_sig != current_signature:
                logging.info(f"Nova faixa: {new_sig}")
                
                final_artist, final_title = services.buscar_nome_oficial(network, c_artist, c_title)
                final_album = c_album

                current_signature = new_sig
                start_time = time.time()
                scrobbled = False
                
                # Atualiza texto do ícone
                texto_tooltip = f"{final_title} - {final_artist}"
                update_ui_callback(texto_tooltip)
                
                try:
                    network.update_now_playing(artist=final_artist, title=final_title, album=final_album)
                except: pass

            if not scrobbled and current_signature:
                elapsed = time.time() - start_time
                duration = media['duration']
                
                should_scrobble = False
                if duration > 0:
                    if (elapsed / duration) * 100 >= 50: should_scrobble = True
                elif elapsed >= 60:
                    should_scrobble = True
                
                if should_scrobble:
                    try:
                        network.scrobble(artist=final_artist, title=final_title, album=final_album, timestamp=int(start_time))
                        scrobbled = True
                        logging.info(f"Scrobbled: {final_title}")
                        # Removemos o notify=True daqui para não ter notificação chata
                        update_ui_callback(f"✅ Scrobblado: {final_title}")
                    except Exception as e:
                        logging.error(f"Falha: {e}")

            await asyncio.sleep(configs.CHECK_INTERVAL)

        except Exception as e:
            logging.error(f"Erro Loop: {e}")
            await asyncio.sleep(10)
# services.py
import pylast
import logging
from winsdk.windows.media.control import GlobalSystemMediaTransportControlsSessionManager
import configs

# --- LAST.FM SERVICE ---
def connect_lastfm():
    try:
        password_hash = pylast.md5(configs.PASSWORD)
        return pylast.LastFMNetwork(
            api_key=configs.API_KEY, 
            api_secret=configs.API_SECRET, 
            username=configs.USERNAME, 
            password_hash=password_hash
        )
    except Exception as e:
        logging.critical(f"Erro ao conectar LastFM: {e}")
        return None

def buscar_nome_oficial(network, artist, title):
    """Tenta achar o nome canônico no Last.fm"""
    try:
        track = network.get_track(artist, title)
        return track.get_artist().get_name(), track.get_name()
    except:
        return artist, title # Retorna o original se falhar

# --- WINDOWS SERVICE ---
async def get_windows_media_info():
    try:
        sessions = await GlobalSystemMediaTransportControlsSessionManager.request_async()
        current_session = sessions.get_current_session()
        
        if current_session:
            info = await current_session.try_get_media_properties_async()
            timeline = current_session.get_timeline_properties()
            app_id = current_session.source_app_user_model_id
            
            return {
                "app_id": app_id,
                "artist": info.artist,
                "title": info.title,
                "album": info.album_title,
                "duration": timeline.end_time.total_seconds() if timeline else 0
            }
    except Exception as e:
        logging.error(f"Erro ao ler Windows API: {e}")
    return None
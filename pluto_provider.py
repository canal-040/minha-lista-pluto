import os
import requests

def get_live_token():
    # Cabeçalhos simulando o navegador para evitar bloqueio 403
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://pluto.tv',
        'Referer': 'https://pluto.tv/'
    }
    # API de autenticação que gera a sessão e o JWT válido
    url = "https://pluto.tv"
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get('session', {}).get('jwt', None)
    except Exception as e:
        print(f"Erro ao obter sessão dinâmica: {e}")
    return None

def create_playlist():
    jwt_token = get_live_token()
    if not jwt_token:
        print("Não foi possível gerar um token JWT válido.")
        return

    # ID oficial do canal Novelíssima extraído do seu link
    channel_id = "6a281d2bd1e6d3ba6b553c7c"
    
    # Monta a URL de transmissão idêntica injetando o novo token dinâmico
    stream_url = (
        f"https://ipv4.pluto.tv/api/tn/video/playout/v2/stitch/hls/channel/{channel_id}/master.m3u8?"
        f"advertisingId=&appName=web&appVersion=8.1.0&app_name=web&clientDeviceType=0&"
        f"clientID=9bda8b26-ca3d-11f1-a9dd-7ced8dd53dce&clientModelNumber=1.0.0&country=BR&"
        f"deviceDNT=false&deviceId=9bda8b26-ca3d-11f1-a9dd-7ced8dd53dce&deviceLat=-22.8400&"
        f"deviceLon=-43.3400&deviceMake=chrome&deviceModel=web&deviceType=web&deviceVersion=133.0.0&"
        f"marketingRegion=BR&serverSideAds=false&sessionID=9bdfe071-ca3d-11f1-acc3-827da81beb23&"
        f"sid=9bdfe071-ca3d-11f1-acc3-827da81beb23&userId=&jwt={jwt_token}&quality=720p&"
        f"deviceMake=chrome&deviceType=web&deviceModel=web&deviceVersion=133.0.0&architecture=x86_64&"
        f"buildVersion=1.0.0&includeExtendedEvents=true&masterJWTPassthrough=true"
    )

    # Grava o arquivo final estruturado para o VLC/IPTV Player
    with open("pluto_br.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write('#EXTINF:-1 tvg-id="novelissima" tvg-logo="https://pluto.tv" group-title="Novelas", Novelíssima\n')
        f.write('#EXTVLCOPT:http-user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"\n')
        f.write(f"{stream_url}\n")
    
    print("Lista pluto_br.m3u gerada com sucesso com token renovado!")

if __name__ == "__main__":
    create_playlist()


import json
import os
import re
import sys
import requests

def get_session(region):
    # Cabeçalho de navegador completo para evitar o Erro 403 de bloqueio
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://pluto.tv',
        'Referer': 'https://pluto.tv/'
    }
    # Rota de autenticação oficial para adquirir o Token JWT necessário para os canais
    url = f"https://pluto.tv{region.lower()}"
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get('session', {}).get('jwt', None)
    except Exception as e:
        print(f"Erro ao obter sessao para {region}: {e}")
    return None

def generate_playlist(region, jwt_token):
    if not jwt_token:
        return
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Authorization': f'Bearer {jwt_token}'
    }
    # Rota correta que traz a lista completa de canais e streams de vídeo da região informada
    url = f"https://pluto.tv{region.lower()}"
    try:
        res = requests.get(url, headers=headers, timeout=15)
        data = res.json()
        channels = data.get('data', []) if isinstance(data, dict) else []
    except Exception as e:
        print(f"Erro ao buscar canais de {region}: {e}")
        return

    if not channels:
        print(f"Nenhum canal localizado para a regiao: {region}")
        return

    filename = f"pluto_{region.lower()}.m3u"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for channel in channels:
            if not channel.get('id') or not channel.get('name'):
                continue
            cid = channel['id']
            name = channel['name']
            category = channel.get('category', 'Geral').capitalize()
            
            # Garante a extração correta da logo do canal
            logo = ""
            for img in channel.get('images', []):
                if img.get('type') == 'logo' or img.get('type') == 'channel-logo':
                    logo = img.get('url', '')
                    break
            
            # Captura a URL real do vídeo HLS (.m3u8)
            stream_url = ""
            for st in channel.get('stm', []):
                if st.get('typ') == 'hls':
                    stream_url = st.get('url', '')
                    break
            
            if stream_url:
                # Caso a URL precise do token JWT injetado
                if "jwt=" not in stream_url:
                    connector = "&" if "?" in stream_url else "?"
                    stream_url = f"{stream_url}{connector}jwt={jwt_token}"
                
                f.write(f'#EXTINF:-1 tvg-id="{cid}" tvg-logo="{logo}" group-title="{category}", {name}\n')
                f.write('#EXTVLCOPT:http-user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"\n')
                f.write(f"{stream_url}\n")
                
    print(f"Lista {filename} criada com sucesso.")

def merge_playlists():
    # Criação do arquivo master pluto_all.m3u reunindo as listas regionais geradas
    files = [f for f in os.listdir('.') if f.startswith('pluto_') and f.endswith('.m3u') and f != 'pluto_all.m3u']
    if not files:
        return
    with open("pluto_all.m3u", "w", encoding="utf-8") as outfile:
        outfile.write("#EXTM3U\n")
        for fname in files:
            with open(fname, "r", encoding="utf-8") as infile:
                lines = infile.readlines()
                if lines and lines[0].startswith("#EXTM3U"):
                    lines = lines[1:]
                outfile.writelines(lines)
    print("Lista master unificada 'pluto_all.m3u' criada com sucesso.")

if __name__ == "__main__":
    # Suporte tanto para os comandos individuais das regiões quanto para a unificação mestre (--merge)
    if len(sys.argv) > 1 and sys.argv[1] == "--merge":
        merge_playlists()
    else:
        # Pega a região vinda da fila do GitHub Actions ou usa 'br' por padrão
        r = os.getenv("PLUTO_REGION", "br").lower()
        token = get_session(r)
        if token:
            generate_playlist(r, token)


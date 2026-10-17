import json
import os
import sys
import requests

def get_channels(region):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    url = f"https://pluto.tv{region.lower()}"
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                return data.get('data', [])
            elif isinstance(data, list):
                return data
    except Exception as e:
        print(f"Erro ao buscar dados para {region}: {e}")
    return []

def generate_playlist(region):
    channels = get_channels(region)
    if not channels:
        print(f"Nenhum canal localizado para {region}.")
        return

    filename = f"pluto_{region.lower()}.m3u"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for channel in channels:
            if not isinstance(channel, dict):
                continue
            cid = channel.get('id')
            name = channel.get('name')
            if not cid or not name:
                continue
                
            category = channel.get('category', 'Geral').capitalize()
            
            logo = ""
            for img in channel.get('images', []):
                if img.get('type') in ['logo', 'channel-logo']:
                    logo = img.get('url', '')
                    break
            
            stream_url = ""
            for st in channel.get('stm', []):
                if st.get('typ') == 'hls':
                    stream_url = st.get('url', '')
                    break
            
            if stream_url:
                f.write(f'#EXTINF:-1 tvg-id="{cid}" tvg-logo="{logo}" group-title="{category}", {name}\n')
                f.write('#EXTVLCOPT:http-user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"\n')
                f.write(f"{stream_url}\n")
    print(f"Lista {filename} criada com sucesso.")

def merge_playlists():
    files = [f for f in os.listdir('.') if f.startswith('pluto_') and f.endswith('.m3u') and f != 'pluto_all.m3u']
    if not files:
        print("Nenhum arquivo individual localizado para unificar.")
        return
    with open("pluto_all.m3u", "w", encoding="utf-8") as outfile:
        outfile.write("#EXTM3U\n")
        for fname in files:
            with open(fname, "r", encoding="utf-8") as infile:
                for line in infile:
                    if line.strip() == "#EXTM3U":
                        continue
                    outfile.write(line)
    print("Lista unificada pluto_all.m3u criada com sucesso.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--merge":
        merge_playlists()
    else:
        regioes = ['br', 'us', 'mx']
        for r in regioes:
            print(f"Processando regiao: {r}")
            generate_playlist(r)


import os
import re
import requests

def download_and_split():
    # Fonte oficial de dados estável que o outro repositório utiliza
    regions = ['ar', 'br', 'ca', 'cl', 'de', 'dk', 'es', 'fi', 'fr', 'gb', 'it', 'mx', 'no', 'se', 'us']
    
    print("Iniciando o download e processamento das listas...")
    
    # Criar uma lista para juntar todos os canais depois (Master Playlist)
    master_channels = []
    
    for region in regions:
        url = f"https://githubusercontent.com{region}.m3u8"
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                lines = response.text.splitlines()
                regional_channels = []
                
                # Processa o arquivo .m3u8 linha por linha
                current_info = None
                for line in lines:
                    if line.startswith("#EXTINF"):
                        current_info = line
                    elif line.startswith("http") and current_info:
                        regional_channels.append((current_info, line))
                        master_channels.append((current_info, line))
                        current_info = None
                
                # Salva o arquivo individual daquela região (ex: pluto_br.m3u)
                if regional_channels:
                    filename = f"pluto_{region}.m3u"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f'#EXTM3U url-tvg="https://github.com{region}.xml.gz"\n')
                        for info, stream in regional_channels:
                            f.write(f"{info}\n{stream}\n")
                    print(f"Lista criada: {filename} ({len(regional_channels)} canais)")
            else:
                print(f"Regiao {region} nao encontrada no servidor (Status {response.status_code})")
        except Exception as e:
            print(f"Erro ao processar a regiao {region}: {e}")

    # Salva o arquivo master unificado com todas as regiões (pluto_all.m3u)
    if master_channels:
        with open("pluto_all.m3u", "w", encoding="utf-8") as f:
            f.write('#EXTM3U url-tvg="https://github.comall.xml.gz"\n')
            for info, stream in master_channels:
                f.write(f"{info}\n{stream}\n")
        print(f"Lista Master criada: pluto_all.m3u ({len(master_channels)} canais no total)")

if __name__ == "__main__":
    download_and_split()


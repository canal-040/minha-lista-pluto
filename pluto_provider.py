import os
import requests

def download_and_split():
    # Lista com as siglas de todas as regiões suportadas
    regions = ['ar', 'br', 'ca', 'cl', 'de', 'dk', 'es', 'fi', 'fr', 'gb', 'it', 'mx', 'no', 'se', 'us']
    
    print("Iniciando o download e processamento das listas...")
    master_channels = []
    
    for region in regions:
        # A URL abaixo foi corrigida com a barra e estrutura certas para acessar o servidor
        url = f"https://githubusercontent.com{region}.m3u8"
        try:
            response = requests.get(url, timeout=20)
            if response.status_code == 200:
                lines = response.text.splitlines()
                regional_channels = []
                
                current_info = None
                for line in lines:
                    if line.startswith("#EXTINF"):
                        current_info = line
                    elif line.startswith("http") and current_info:
                        regional_channels.append((current_info, line))
                        master_channels.append((current_info, line))
                        current_info = None
                
                if regional_channels:
                    filename = f"pluto_{region}.m3u"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f'#EXTM3U url-tvg="https://github.com{region}.xml.gz"\n')
                        for info, stream in regional_channels:
                            f.write(f"{info}\n{stream}\n")
                    print(f"Lista criada com sucesso: {filename} ({len(regional_channels)} canais)")
            else:
                print(f"Regiao {region} retornou status de erro: {response.status_code}")
        except Exception as e:
            print(f"Erro ao processar a regiao {region}: {e}")

    # Geração da lista master unificada pluto_all.m3u
    if master_channels:
        with open("pluto_all.m3u", "w", encoding="utf-8") as f:
            f.write('#EXTM3U url-tvg="https://github.comall.xml.gz"\n')
            for info, stream in master_channels:
                f.write(f"{info}\n{stream}\n")
        print(f"Lista Master criada com sucesso: pluto_all.m3u ({len(master_channels)} canais no total)")

if __name__ == "__main__":
    download_and_split()


import os
import requests

def download_brasil_list():
    print("Iniciando a sincronização com a base de dados validada...")
    
    # URL da lista brasileira estável com tokens já renovados pela comunidade
    url = "https://githubusercontent.com"
    
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
                    current_info = None
            
            # Grava a lista final pluto_br.m3u contendo o Novelíssima
            if regional_channels:
                filename = "pluto_br.m3u"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write('#EXTM3U url-tvg="https://github.com"\n')
                    for info, stream in regional_channels:
                        f.write(f"{info}\n{stream}\n")
                print(f"Sucesso! Lista criada com {len(regional_channels)} canais brasileiros.")
            else:
                print("Nenhum canal foi encontrado dentro da resposta obtida.")
        else:
            print(f"Erro ao acessar base de dados: Status {response.status_code}")
            
    except Exception as e:
        print(f"Falha crítica ao processar a lista: {e}")

if __name__ == "__main__":
    download_brasil_list()


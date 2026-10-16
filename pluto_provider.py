import json
import requests

def executar_conversao():
    print("Iniciando a captura de canais da Pluto TV...")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    url_boot = "https://pluto.tv"
    
    try:
        response_boot = requests.get(url_boot, headers=headers)
        if response_boot.status_code != 200:
            print("Falha ao se conectar com o servidor de boot.")
            return
            
        token_jwt = response_boot.json().get("session", {}).get("jwt", "")
        if not token_jwt:
            print("Token JWT nao encontrado.")
            return
            
        url_api = "https://pluto.tv"
        
        response_api = requests.get(url_api, headers=headers)
        dados_canais = response_api.json()
        
        with open("pluto_brasil.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            for canal in dados_canais:
                if not canal.get("id") or not canal.get("name"):
                    continue
                    
                id_canal = canal["id"]
                nome_canal = canal["name"]
                categoria = canal.get("category", "Geral").capitalize() if canal.get("category") else "Geral"
                
                images = canal.get("images", [])
                logo = images.get("path", "") if images else ""
                
                f.write(f'#EXTINF:-1 tvg-id="{id_canal}" tvg-logo="{logo}" group-title="{categoria}", {nome_canal}\n')
                f.write('#EXTVLCOPT:http-user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"\n')
                
                url_stream = f"https://pluto.tv{id_canal}/master.m3u8?appName=web&deviceMake=Chrome&deviceType=web&jwt={token_jwt}\n"
                f.write(url_stream)
                
        print("Arquivo pluto_brasil.m3u gerado com sucesso!")
    except Exception as e:
        print(f"Erro durante a execucao: {e}")

if __name__ == "__main__":
    executar_conversao()

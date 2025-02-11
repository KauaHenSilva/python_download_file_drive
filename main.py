import re
import os
import requests
import gdown
import argparse
from tqdm import tqdm

try:
    from google.colab import auth
    from googleapiclient.discovery import build
    auth.authenticate_user()
    service = build('drive', 'v3')
except ImportError:
    raise ImportError("Este script deve ser executado no Google Colab")
except AttributeError:
    raise AttributeError("""
Este script deve ser executado no Google Colab. É necessário autenticar o usuário para acessar o Google Drive.
Para isso, execute o seguinte código no Google Colab:       

from google.colab import auth
from googleapiclient.discovery import build
auth.authenticate_user()                         
""")


def listar_arquivos(service, folder_id, destination, links, paths, names):
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, pageSize=1000, fields="nextPageToken, files(id, name, mimeType, parents)").execute()
    items = results.get('files', [])

    if items:
        for item in items:
            file_id = item['id']
            file_name = item['name']
            mime_type = item['mimeType']
            link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

            caminho_destino = os.path.join(destination, file_name)
            if mime_type == "application/vnd.google-apps.folder":
                os.makedirs(caminho_destino, exist_ok=True)
                listar_arquivos(service, file_id, caminho_destino, links, paths, names)
            else:
                links.append(link)
                paths.append(caminho_destino)
                names.append(file_name)


def obter_url_final(link):
    try:
        response = requests.get(link, allow_redirects=True)
        return response.url
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o link: {e}")
        return None


def download(links, paths, names):
    for link, path, name in tqdm(zip(links, paths, names), total=len(names), desc="Baixando arquivos", unit="arquivo"):
        if os.path.exists(path):
            continue
        
        path = path.replace(name, "")
        try:
            gdown.download(link, path, quiet=True, fuzzy=True)
        except Exception:
            gdown.download(obter_url_final(link), path, quiet=True, fuzzy=True)
  
def retirar_id(url) -> tuple:
    if "folders" in url:
        return url.split("folders/")[1].split("?")[0], "Folder"
    else:
        return url.split("file/d/")[1].split("/view")[0], "File"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download de arquivos/pastas do Google Drive')
    parser.add_argument('url', help="url do recurso")
    parser.add_argument('output', help='Caminho de saída')
    parser.add_argument('--folder', help='Discontinuado')
    parser.add_argument('--fuzzy', help='Discontinuado')
    parser.add_argument('--use-cookies', help='Discontinuado')

    args = parser.parse_args()
    url = args.url
    folder_id, tipo = retirar_id(url)
    destination = args.output

    if tipo == "Folder":
        links, paths, names = [], [], []
        listar_arquivos(service, folder_id, destination, links, paths, names)
        download(links, paths, names)
    elif tipo == "File":
        name = service.files().get(fileId=folder_id).execute()['name']
        path = os.path.join(destination, name)
        download([url], [path], [name])
        
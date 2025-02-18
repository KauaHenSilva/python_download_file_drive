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


def obter_url_final(link):
    response = requests.get(link, allow_redirects=True)
    return response.url, response.status_code

def retirar_id(url) -> tuple:
    """Extrai o ID de um link do Google Drive e seu tipo"""
    if "folders" in url:
        return url.split("folders/")[1].split("?")[0], "application/vnd.google-apps.folder"
    else:
        return url.split("file/d/")[1].split("/view")[0], "File"

def listar_arquivos(service, folder_id, destination, links, paths, names):
    """Lista arquivos e pastas no Google Drive e obtém seus links"""
    query = f"'{folder_id}' in parents and trashed = false"
    results = service.files().list(q=query, pageSize=1000, fields="nextPageToken, files(id, name, mimeType, parents)").execute()
    items = results.get('files', [])

    if items:
        for item in items:
            file_id = item['id']
            file_name = item['name']
            mime_type = item['mimeType']

            caminho_destino = os.path.join(destination, file_name)

            if mime_type == "application/vnd.google-apps.shortcut":
                link = f"https://drive.google.com/folder/d/{file_id}/view?usp=sharing"
                link, status = obter_url_final(link)

                if status == 200:
                    file_id, mime_type = retirar_id(link)

                else:
                    link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
                    link, status = obter_url_final(link)
                    file_id, mime_type = retirar_id(link)

            if mime_type == "application/vnd.google-apps.folder":
                os.makedirs(caminho_destino, exist_ok=True)
                listar_arquivos(service, file_id, caminho_destino, links, paths, names)

            else:
                link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
                links.append(link)
                paths.append(caminho_destino)
                names.append(file_name)


def download(links, paths, names):
    for link, path, name in tqdm(zip(links, paths, names), total=len(names), desc="Baixando arquivos", unit="arquivo"):
        if os.path.exists(path):
            continue
        
        path = path.replace(name, "")
        gdown.download(link, path, quiet=True, fuzzy=True)

def main(download_with_file: bool = False, file_with_links: bool = False, url: str = None, output: str = None):
    folder_id, tipo = retirar_id(url)
    
    if download_with_file:
        download([url], [output], ['arquivos_download.csv'])
        with open(f"{output}/arquivos_download.csv", "r") as file:
            lines = file.readlines()
            lines = [(line.split(",")[0], line.split(",")[1],line.split(",")[2])  for line in lines]
            links, paths, names = zip(*lines)
    else:
        links, paths, names = [], [], []
        if tipo == "application/vnd.google-apps.folder" and file_with_links:
            listar_arquivos(service, folder_id, output, links, paths, names)
        else:
            names.append(service.files().get(fileId=folder_id).execute()['name'])
            links.append(obter_url_final(url)[0])
            paths.append(os.path.join(output, names[0]))
            
    print(links, paths, names)
    download(links, paths, names)

    if args.file_with_links:
        with open(f"{output}/arquivos_download.csv", "w") as file:
            file.write("link,caminho,nome\n")
            for link, path, name in zip(links, paths, names):
                file.write(f"{link},{path},{name}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download de arquivos/pastas do Google Drive')
    parser.add_argument('url', help="url do recurso")
    parser.add_argument('output', help='Caminho de saída')
    parser.add_argument('--folder', help='Discontinuado', action='store_true')
    parser.add_argument('--fuzzy', help='Discontinuado', action='store_true')
    parser.add_argument('--use-cookies', help='Discontinuado', action='store_true')
    parser.add_argument('--file-with-links', help='Possui links para download junto com os nomes dos arquivos e pastas', action='store_true')
    parser.add_argument('--download_with_file', help='Baixar arquivos com base em um arquivo com links', action='store_true')
    args = parser.parse_args()
    main(args.download_with_file, args.file_with_links, args.url, args.output)

import gdown
import argparse
import os

def download_from_drive(url_or_id, output, fuzzy=False, folder=False, use_cookies=False):
    """Download de arquivos ou pastas do Google Drive"""
    if folder:
        if "drive.google.com" in url_or_id:
            folder_id = url_or_id.split("/folders/")[-1].split("?")[0]
        else:
            folder_id = url_or_id
        
        gdown.download_folder(
            id=folder_id,
            output=output,
            use_cookies=use_cookies
        )
    else:
        if "drive.google.com" in url_or_id:
            gdown.download(
                url=url_or_id,
                output=output,
                fuzzy=fuzzy,
                use_cookies=use_cookies
            )
        else:
            gdown.download(
                id=url_or_id,
                output=output,
                use_cookies=use_cookies
            )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download de arquivos/pastas do Google Drive')
    parser.add_argument('url_or_id', help='URL ou ID do recurso')
    parser.add_argument('output', help='Caminho de saída')
    parser.add_argument('--fuzzy', action='store_true', help='Para URLs não canônicas de arquivos')
    parser.add_argument('--folder', action='store_true', help='Indica que é uma pasta')
    parser.add_argument('--use-cookies', action='store_true', help='Usar autenticação via cookies')
    
    args = parser.parse_args()
    
    if os.path.exists(args.output):
        print(f"O arquivo {args.output} já existe")
    else:
        download_from_drive(
            args.url_or_id,
            args.output,
            fuzzy=args.fuzzy,
            folder=args.folder,
            use_cookies=args.use_cookies
        )
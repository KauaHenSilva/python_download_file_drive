# Google Drive Downloader (Python)

Um script simples para baixar arquivos ou pastas do Google Drive via linha de comando utilizando a biblioteca `gdown`.

---

## 📦 Funcionalidades
- **Download de arquivos individuais**: Suporte a URLs ou IDs de arquivos.
- **Download de pastas inteiras**: Mantém a estrutura de diretórios.
- **Modo `fuzzy`**: Para URLs não canônicas.
- **Autenticação via cookies**: Acesso a arquivos/pastas restritos.
- **Verificação de existência**: Alerta se o arquivo/pasta já existe localmente.

---

## ⚙️ Requisitos
- Python 3
- Pacotes listados em `requirements.txt`

---

## 🛠️ Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/google-drive-downloader.git
   cd google-drive-downloader
   ```
2. Instale as dependências:
   ```bash
    pip install -r requirements.txt
   ```

## 🚀 Como Usar

### 📂 Download Básico

Execute o seguinte comando no terminal:

   ```bash
   python script.py <URL_OU_ID> <CAMINHO_SAIDA>
   ```

Exemplo:

   ```bash
    python script.py "https://drive.google.com/file/d/1A2B3C4D5E6F/view" "meu_arquivo.zip"
   ```


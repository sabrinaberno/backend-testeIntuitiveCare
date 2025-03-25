# Site que auxiliou na busca: https://www.geeksforgeeks.org/downloading-pdfs-with-python-using-requests-and-beautifulsoup/
# Site de documentação da compactação ZIP: https://docs.python.org/pt-br/3.7/library/zipfile.html

import requests
from bs4 import BeautifulSoup
import os
import zipfile

# Página onde estão os anexos
url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'

# Simula um acesso por um navegador
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Fazendo a requisição para obter o HTML da página
response = requests.get(url, headers=headers)
response.raise_for_status() 

# Passa o conteúdo da página para o BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Busca todos os links dentro da página
links = soup.find_all('a', href=True)

anexos = {}

# Verifica se o link contém 'Anexo_I' ou 'Anexo_II' e se termina com .pdf
for link in links:
    href = link['href']
    if 'Anexo_I' in href and href.endswith('.pdf'):
        anexos['Anexo I'] = href
    if 'Anexo_II' in href and href.endswith('.pdf'):
        anexos['Anexo II'] = href

# Criando uma pasta para armazenar os anexos
output_dir = 'arquivos_anexos'
os.makedirs(output_dir, exist_ok=True)

# Lista para armazenar os caminhos dos arquivos baixados
downloaded_files = []

# Faz o download dos PDFs e salva na pasta atual
for filename, link in anexos.items():
    if not link.startswith('http'):
        link = f'https://www.gov.br{link}'
    
    response = requests.get(link, headers=headers)
    response.raise_for_status()
    
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, 'wb') as file:
        file.write(response.content)
    
    downloaded_files.append(file_path)
    print(f'{filename} baixado e salvo em {file_path}')

# Compactando a pasta em um arquivo ZIP
zip_filename = 'arquivos_anexos.zip'
zip_path = zip_filename  

# Abre o arquivo ZIP no modo de escrita
# DEFLATE: método de compressão padrão e eficiente para arquivos ZIP
# as zipf: cria um alias zipf para o arquivo ZIP aberto, que será usado para adicionar arquivos ao ZIP
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for foldername, subfolders, filenames in os.walk(output_dir):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            # Adicionando os arquivos da pasta no ZIP
            zipf.write(file_path, os.path.relpath(file_path, output_dir))

print(f'A pasta {output_dir} foi compactada em {zip_path}')

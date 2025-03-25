# site que auxiliou na busca: https://www.geeksforgeeks.org/downloading-pdfs-with-python-using-requests-and-beautifulsoup/

import requests
from bs4 import BeautifulSoup
import os

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

# Faz o download dos PDFs e salva na pasta atual
for anexo, link in anexos.items():
    if not link.startswith('http'):
        link = f'https://www.gov.br{link}'
    
    response = requests.get(link, headers=headers)
    response.raise_for_status()
    
    filename = f'{anexo}.pdf'
    
    with open(filename, 'wb') as file:
        file.write(response.content)
    
    print(f'{anexo} baixado e salvo como {filename}')

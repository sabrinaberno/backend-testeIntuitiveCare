import pdfplumber
import csv
import os
import zipfile

pdf_dir = "arquivos_anexos"  
csv_dir = "arquivos_csv"  
zip_filename = "Teste_Sabrina.zip" 

# Criando a pasta arquivos_csv, se ainda não existir
os.makedirs(csv_dir, exist_ok=True)

pdf_file = os.path.join(pdf_dir, "AnexoI.pdf")
csv_file = os.path.join(csv_dir, "anexo_I_tabela.csv")

substituicoes = {
    "OD": "Seg. Odontológica",
    "AMB": "Seg. Ambulatorial"
}

# Abre o arquivo PDF
with pdfplumber.open(pdf_file) as pdf:
    table_data = []

    # Percorre todas as páginas do PDF
    for page in pdf.pages:
        tables = page.extract_tables()  # Extrai as tabelas da página

        # Adiciona todas as tabelas encontradas
        for table in tables:
            for row in table:
                # Substitui abreviações nas colunas OD e AMB
                row = [substituicoes.get(cell, cell) if cell in substituicoes else cell for cell in row]
                table_data.append(row)

# Salva os dados extraídos em um arquivo CSV dentro da pasta arquivos_csv
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(table_data)

print(f"Os dados do Anexo I foram extraídos e salvos em {csv_file}.")

# Compactando o CSV em um ZIP
zip_path = os.path.join(csv_dir, zip_filename)

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_file, os.path.basename(csv_file))

print(f"O arquivo {zip_filename} foi criado com sucesso!")

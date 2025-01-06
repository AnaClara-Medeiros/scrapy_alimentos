from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configurar o driver do Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Executa o navegador em modo headless (opcional)
driver = webdriver.Chrome(options=options, executable_path="caminho/para/chromedriver")

# URL do site
url = "https://www.econodata.com.br/empresas/sp-itapeva/alimentos"  # Substitua pela URL correta
driver.get(url)

# Aguardar o carregamento da tabela
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#ecdt-table-container > div > div > table"))
    )
except:
    print("Tabela não carregada a tempo!")
    driver.quit()
    exit()

# Função para extrair os dados da tabela em uma página
def extrair_dados_tabela():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.select_one("#ecdt-table-container > div > div > table")
    if not table:
        return []

    # Cabeçalhos da tabela
    headers = [th.text.strip() for th in table.select("thead tr th")]

    # Linhas de dados
    rows = table.select("tbody tr")
    data = []
    for row in rows:
        cols = [td.text.strip() for td in row.select("td")]
        data.append(cols)
    
    return headers, data

# Inicializar armazenamento dos dados
todas_as_paginas = []
headers = []

while True:
    # Extrair dados da tabela atual
    headers, dados = extrair_dados_tabela()
    todas_as_paginas.extend(dados)

    try:
        botao_proximo = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#ecdt-table-container > div.py-5.hidden.lg\\:flex.justify-end.gap-\\[5px\\] > div:nth-child(8) > div"))
        )
        botao_proximo.click()
        time.sleep(2)  # Aguardar a próxima página carregar
    except:
        print("Não há mais páginas.")
        break
# Fechar o navegador
driver.quit()

# Criar DataFrame e salvar em CSV
df = pd.DataFrame(todas_as_paginas, columns=headers)
df.to_csv("tabela_dados.csv", index=False, encoding="utf-8")
print("Dados extraídos com sucesso!")

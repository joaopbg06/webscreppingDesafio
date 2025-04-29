# pip install selenium

# módulo para controlar o navegador web
from selenium import webdriver

# localizador de elementos
from selenium.webdriver.common.by import By

# serviço para configurar o caminho do executável chromedriver
from selenium.webdriver.chrome.service import Service

# classe que permite executar ações de avançar(o mover do mouse, clique/arrasta)
from selenium.webdriver.common.action_chains import ActionChains

# classe que espera de forma explícita até uma condição seja satisfeita(ex: que um elemento apareça)
from selenium.webdriver.support.ui import WebDriverWait

#Condições esperadas usadas com WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# trabalhar com dataframe
import pandas as pd

#uso de funções relacionada ao tempo
import time 

#uso para tratamento de exceção
from selenium.common.exceptions import TimeoutException


from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

import numpy as np

chrome_driver_path = "C:\Program Files\chromedriver-win64\chromedriver.exe"

service = Service(chrome_driver_path) #navegador controlado pelo Selenium
options = webdriver.ChromeOptions() #configurar as opções do navegador
options.add_argument('--disable-gpu') #evita possíveis erros gráficos
options.add_argument('--window-size=1920,1080') #defini uma resolução fixa
# options.add_argument('--headless') # ativa o modo headless (sem abrir o navegador;

driver = webdriver.Chrome(service=service, options=options)

url_base = 'https://www.vivareal.com.br/venda/?transacao=venda&pagina=1'
driver.get(url_base)
time.sleep(5) 

casas = {"metragem": [], 'quartos': [], 'banheiros': [], 'vagas': [], 'valor': [], 'nomeRua': []}
pagina = 1
limite_imoveis = 100  # Define o limite de imóveis

while len(casas['nomeRua']) <= limite_imoveis:

    print(f"\nColetando dados da página {pagina}...")

    try:
        WebDriverWait(driver, 30).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-cy="rp-property-cd"]'))
        )
        print('Elementos encontrados com sucesso')

    except TimeoutException:

        print('Tempo de espera excedido na página {pagina}. Encerrando.')
        break

    produtos = driver.find_elements(By.CSS_SELECTOR, '[data-cy="rp-property-cd"]')

    if not produtos:
        print(f"Nenhum produto encontrado na página {pagina}. Encerrando.")
        break

    for produto in produtos:

        try:
            nomeRua = produto.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-street-txt"]').text.strip()
            valor = produto.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-price-txt"]').text.strip()

            metragem = produto.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-propertyArea-txt"]').text.strip() if produto.find_elements(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-propertyArea-txt"]') else np.nan
            quartos = produto.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bedroomQuantity-txt"]').text.strip() if produto.find_elements(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bedroomQuantity-txt"]') else np.nan
            banheiros = produto.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bathroomQuantity-txt"]').text.strip() if produto.find_elements(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bathroomQuantity-txt"]') else np.nan
            vagas = produto.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-parkingSpacesQuantity-txt"]').text.strip() if produto.find_elements(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-parkingSpacesQuantity-txt"]') else np.nan

            print(f"{nomeRua} - {valor}")

            casas['metragem'].append(metragem)
            casas['quartos'].append(quartos)
            casas['banheiros'].append(banheiros)
            casas['vagas'].append(vagas)
            casas['valor'].append(valor)
            casas['nomeRua'].append(nomeRua)

        except NoSuchElementException as e:
            print(f"Erro ao coletar dados de um produto: {str(e)}")

        except Exception as e:
            print(f"Erro inesperado: {str(e)}")

    try:

        botao_proximo = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="next-page"]'))
        )

        driver.execute_script("arguments[0].scrollIntoView();", botao_proximo)
        
        time.sleep(1)
        botao_proximo.click()

        pagina += 1
        print(f"Indo para a página {pagina}")

        time.sleep(5)

    except TimeoutException:
        print("Botão de próxima página não encontrado. Encerrando.")
        break

    except WebDriverException as e:
        print(f"Erro ao clicar no botão de próxima página: {str(e)}")
        break

driver.quit()

df = pd.DataFrame(casas)
df.to_excel('imovel.xlsx', index=False)

print(f"{len(df)} produtos encontrados")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import _find_elements
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as condicao_esperada
from time import sleep
import openpyxl


def raspagem_de_dados():

    email = input(
        'Digite o email para receber o relatorio de valores dos celulares!')
    email.lower()

    lista_nome_celulares = []
    lista_preco_celulares = []

    chrome_options = Options()
    chrome_options.add_argument('--lang=pr-BR')
    chrome_options.add_argument('--disable-notifications')
    path = r'G:\Dropbox\OHomemnãoparaNunca\curso_automacao\web_scraping_olx_excel\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=path, options=chrome_options)
    link = 'https://telefonesimportados.netlify.app/'
    driver.get(link)
    sleep(5)

    for p in range(5):

        item = 1

        for i in range(12):

            lista_nomes = driver.find_elements_by_xpath(
                f'/html/body/div[5]/div[2]/div[1]/div[{item}]/div/h2/a')

            lista_nome_celulares.append(lista_nomes[0].text)

            sleep(2)

            lista_precos = driver.find_elements_by_xpath(
                f'//div[{item}]/div[@class="single-shop-product" and 1]/div[@class="product-carousel-price" and 2]/ins[1]')

            lista_preco_celulares.append(lista_precos[0].text)

            item += 1

            sleep(2)

        try:

            botao_proximo = driver.find_element_by_xpath(
                '/html/body/div[5]/div[2]/div[2]/div/div/nav/ul/li[7]/a')
            botao_proximo.click()
            print('Navegando para proxima pagina')
            sleep(5)

        except NoSuchElementException:

            print('Não há mais paginas')
            print('Escaneamento Concluido')

    index = 2
    planilha = openpyxl.Workbook()
    celulares = planilha['Sheet']
    celulares.title = 'Celulares'
    celulares['A1'] = 'Nome'
    celulares['B1'] = 'Preço'

    for nome, preco in zip(lista_nome_celulares, lista_preco_celulares):

        celulares.cell(column=1, row=index, value=nome)
        celulares.cell(column=2, row=index, value=preco)
        index += 1

    planilha.save("exemplos2.xlsx")


raspagem_de_dados()

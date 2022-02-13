import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options  # Definir o tamanho da janela
from time import sleep

options = Options()
options.add_argument('--headless')  # Não fazer as etapas, não abre o navegador

navegador = webdriver.Firefox()

lista = []

nome = input("Digite o nome: ")

navegador.get(f"https://www.amazon.com.br/s?k={nome}")

sleep(2)

page_content1 = navegador.page_source

site1 = BeautifulSoup(page_content1, 'html.parser')

pag = site1.find('span', attrs={'class': 's-pagination-item s-pagination-disabled'})

for page_nb in range(int(pag.text)):

    navegador.get(f"https://www.amazon.com.br/s?k={nome}&page={page_nb}")

    sleep(3)

    page_content = navegador.page_source

    site = BeautifulSoup(page_content, 'html.parser')

    cel = site.findAll('div', attrs={'class': 'a-section a-spacing-small s-padding-left-small s-padding-right-small'})

    for vaga in cel:

        titulo = vaga.find('span', attrs={'class': 'a-size-base-plus a-color-base a-text-normal'})

        preco = vaga.find('span', attrs={'class': 'a-price-whole'})

        link = vaga.find('a', attrs={
            'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

        if preco:
            lista.append([titulo.text, preco.text, link['href']])

    dt = pd.DataFrame(lista, columns=['Titulo', 'Preço', 'Link'])

    dt.to_excel('AmazonBeautiful.xlsx', index=False)
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime  # Para capturar a data e hora atuais

def extract_data(driver):
    print("Iniciando a extração de dados...")
    driver.get("http://quotes.toscrape.com/")

    # Lista para armazenar as citações, autores e links
    data = []

    # Localiza todas as citações na página inicial
    quotes = driver.find_elements(By.CLASS_NAME, "quote")

    for quote in quotes:
        # Extrai o texto da citação, autor e o link para o autor
        text = quote.find_element(By.CLASS_NAME, "text").text.strip()
        author = quote.find_element(By.CLASS_NAME, "author").text.strip()
        author_link = quote.find_element(By.TAG_NAME, "a").get_attribute("href").strip()

        # Adiciona as informações à lista de dados
        data.append([text, author, author_link])

    # Cria a pasta collectDados, se não existir
    output_dir = "CollectDados"
    os.makedirs(output_dir, exist_ok=True)

    # Gera o nome do arquivo com a data e hora atual
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = os.path.join(output_dir, f"extracted_data_{timestamp}.csv")

    # Salva os dados extraídos em um novo arquivo CSV
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Quote", "Author", "Author Link"])  # Cabeçalho
        writer.writerows(data)  # Escreve os dados

    print(f"Dados extraídos e salvos em '{output_file}'.")

# Exemplo de como iniciar o Selenium e chamar a função:
if __name__ == "__main__":
    # Inicia o WebDriver com o chromedriver na mesma pasta
    chromedriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
    driver = webdriver.Chrome(executable_path=chromedriver_path)  # Caminho relativo do chromedriver
    extract_data(driver)
    driver.quit()

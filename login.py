import os
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime  # Importa o módulo datetime

# Verifica se a pasta 'loginLogs' existe. Se não, cria.
login_logs_dir = 'loginLogs'
if not os.path.exists(login_logs_dir):
    os.makedirs(login_logs_dir)
    logging.info(f"Pasta '{login_logs_dir}' criada.")

# Verifica se a pasta 'screenshots' dentro de 'loginLogs' existe. Se não, cria.
screenshot_dir = os.path.join(login_logs_dir, 'screenshots')
if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)
    logging.info(f"Pasta '{screenshot_dir}' criada.")

# Configuração do logging com data, hora e minuto no formato desejado
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato com data e hora
    datefmt='%Y-%m-%d %H:%M:%S',  # Formato da data e hora
    handlers=[
        logging.FileHandler(os.path.join(login_logs_dir, 'login.log')),  # Caminho para o arquivo de log
        logging.StreamHandler()
    ]
)

def login():
    # Configuração do WebDriver com Selenium Manager
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "C:\\Users\\muril\\Documents\\chrome-win64\\chrome.exe"
    
    # Inicializa o driver sem o caminho manual do chromedriver
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    login_url = "http://quotes.toscrape.com/login"
    
    driver.get(login_url)

    try:
        logging.info("Iniciando o login...")
        # Login
        email_field = wait.until(EC.presence_of_element_located((By.ID, "username")))

        logging.info("Preenchendo o campo de email...")
        email_field.send_keys("test_user")
        driver.find_element(By.ID, "password").send_keys("secure_password")
        driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Login"]').click()

        # Aguardar redirecionamento (espera até que a URL mude após o login)
        wait.until(EC.url_changes(login_url))

        # Verifique a URL após o redirecionamento
        current_url = driver.current_url
        logging.info(f"URL após login: {current_url}")

        # Validar a URL ou presença de um elemento específico na página de sucesso após o login
        if "quotes.toscrape.com" in current_url:
            logging.info("Login realizado com sucesso!")
        else:
            logging.error("Login falhou. Página de redirecionamento não encontrada.")
            raise Exception("Login falhou. Página de redirecionamento não encontrada.")

    except Exception as e:
        # Grava o erro no log e faz a captura da screenshot
        logging.error("Erro durante o login:", exc_info=True)

        # Gera o timestamp e formata para o nome do arquivo
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot_path = os.path.join(screenshot_dir, f"error_screenshot_{timestamp}.png")
        
        # Salva a screenshot do erro
        driver.save_screenshot(screenshot_path)

        # Registra a informação no log com o caminho da screenshot
        logging.info(f"Screenshot salva em: {screenshot_path}")

    finally:
        # Em qualquer caso (sucesso ou erro), o final do processo é logado
        logging.info("Login process completed.")

    # Retorna o driver caso o login seja bem-sucedido ou não
    return driver

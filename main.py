from login import login
from data_table import extract_data

def main():
    driver = None
    try:
        # Etapa 1: Login
        driver = login()  # Chama a função de login
        print("Login concluído com sucesso.")

    except Exception as e:
        # Logar o erro, mas continuar a execução
        print(f"Ocorreu um erro no login: {e}")
        # Defina o driver como None ou algo mais apropriado se necessário
        driver = None

    # Etapa 2: Extração de dados (sempre será chamado)
    try:
        if driver:
            print("Iniciando a extração de dados...")
            extract_data(driver)
            print("Extração de dados concluída com sucesso.")
        else:
            print("Erro: driver não inicializado.")
    except Exception as e:
        print(f"Ocorreu um erro na extração de dados: {e}")
    
    finally:
        # Garantir que o driver seja fechado (se foi inicializado)
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()

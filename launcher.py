import sys
from streamlit.web import cli as stcli

if __name__ == "__main__":
    # Define los argumentos del comando como si los escribieras en la consola
    sys.argv = ["streamlit", "run", "streamlit_app.py"]

    # Inicia el servidor de Streamlit
    sys.exit(stcli.main())
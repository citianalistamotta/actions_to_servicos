from pywinauto import Application
from pywinauto import findwindows
from pywinauto.win32functions import PostMessage
from pywinauto.win32defines import WM_CLOSE
from datetime import datetime
from historico import Historico
from relatorio import Relatorio


def InicializaBot():
    try:
        chrome_window = findwindows.find_windows(title_re=".*Google Chrome.*")
        if chrome_window:
            app = Application().connect(title_re=".*Google Chrome")
            chrome = app.top_window()
            PostMessage(chrome_window[0], WM_CLOSE, 0, 0)
        else:
            print("Nenhum processo do Google Chrome em execução.")
    except Exception as e:
        print(f"Erro ao inicializar o bot: {e}")

if __name__ == "__main__":
        data_atual = datetime.now()
        historico = Historico()
        relatorio = Relatorio()

        relatorio.relatorioServicos() 
        InicializaBot()
        print("-----------------------------enviarRelatorioServicos-----------------------")
        relatorio.enviarRelatorioServicos()

        

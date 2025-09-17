from datetime import datetime
from historico import Historico
from relatorio import Relatorio
from enviadorWhats import EnviadorWhats


if __name__ == "__main__":
    data_atual = datetime.now()
    historico = Historico()
    relatorio = Relatorio()
    enviadorWhats = EnviadorWhats() 

    print("-----------------------------Historico-----------------------")
    df_ordenado = historico.get_valorOrdenadoCompleto()
    if df_ordenado is not None:
        print("Execução finalizada.")
    else:
        print("Execução falhou.")
    
    print("-----------------------------Relatório-----------------------")
    relatorio.relatorioServicos() 

    print("-----------------------------Enviar Relatório-----------------------")
    enviadorWhats.enviar_relatorio()


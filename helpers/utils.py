from PySide6.QtCore import QDate

def format_month_year(date: QDate) -> str:
    meses_ptbr = {
        1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
        5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
        9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
    }
    
    num_mes = date.month()
    ano = date.year()

    nome_mes = meses_ptbr.get(num_mes, "Mês") 
    
    return f"{nome_mes} {ano}"
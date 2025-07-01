from datetime import datetime, timedelta

def generar_intervalos(hora_inicio, hora_fin, duracion_min=30, formato='%H:%M'):
    """
    Retorna una lista de tuplas (inicio, fin) para los intervalos entre hora_inicio y hora_fin.
    """
    resultado = []
    actual = datetime.strptime(str(hora_inicio), formato)
    fin = datetime.strptime(str(hora_fin), formato)
    while actual + timedelta(minutes=duracion_min) <= fin:
        inicio = actual.strftime(formato)
        actual += timedelta(minutes=duracion_min)
        fin_intervalo = actual.strftime(formato)
        resultado.append((inicio, fin_intervalo))
    return resultado
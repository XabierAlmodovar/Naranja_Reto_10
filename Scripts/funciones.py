def formato_fechas(segundos):
    segundos = int(segundos)
    dias = segundos // 86400
    horas = (segundos % 86400) // 3600
    minutos = (segundos % 3600) // 60
    texto = []
    if dias > 0: texto.append(f"{dias}d")
    if horas > 0: texto.append(f"{horas}h")
    if minutos > 0: texto.append(f"{minutos}m")
    return " ".join(texto) if texto else "< 1m"
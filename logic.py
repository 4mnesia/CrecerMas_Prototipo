# logic.py
def simular_ia_riesgo(asistencia, notas):
    score_base = 100 - asistencia
    if notas < 4.0:
        score_base += 20
    score = min(score_base, 100)
    
    if score > 70:
        return "ALTO", score
    elif score > 40:
        return "MEDIO", score
    else:
        return "BAJO", score
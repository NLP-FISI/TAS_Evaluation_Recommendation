import math

def prob_correct(theta, beta):
    return 1.0 / (1.0 + math.exp(-(theta - beta)))

def actualizar_dificultad(theta, racha, beta, resultado, eta=0.6): 
    """
    theta: dificultad acumulada actual (float)
    racha: entero entre -3 y +3 (valor previo)
    beta: dificultad del reto anterior (1..5)
    resultado: 1 si correcto, 0 si incorrecto
    devuelve: theta_nuevo, racha_nuevo, beta_siguiente, prob_estimada
    """
    p = prob_correct(theta, beta)
    
    # actualizar racha
    if resultado == 1:
        racha = min(racha + 1, 3)
    else:
        racha = max(racha - 1, -3)
    
    # factor por racha
    factor = 1.0 + 0.1 * abs(racha)
    
    # actualizar theta
    theta_nuevo = theta + eta * factor * (resultado - p)
    
    # limitar theta_nuevo entre 1 y 5
    theta_nuevo = max(1, min(5, theta_nuevo))
    
    # mapear a dificultad siguiente
    beta_siguiente = round(theta_nuevo)
    
    return theta_nuevo, racha, beta_siguiente, p


# #DATOS>
# theta = 3.0   # dificultad acumulada inicial
# racha = 0     # sin racha aún
# beta = 3      # el reto anterior fue dificultad 3


# resultados = [1, 1, 1, 1, 0, 0]  # tres aciertos seguidos

# for r in resultados:
#     theta, racha, beta_siguiente, p = actualizar_dificultad(theta, racha, beta, r)
#     print(f"r={r}, θ={theta:.3f}, racha={racha}, prob={p:.3f}, siguiente={beta_siguiente}")
#     beta = beta_siguiente

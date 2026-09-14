# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 13:14:04 2026

@author: anton
"""

import random
import math
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURACIÓN DEL EXPERIMENTO
# ============================================================

NUM_CIUDADES = 8

TAM_POBLACION = 50

TASA_MUTACION = 0.10

GENERACIONES = 500

ELITISMO = 2

TAM_TORNEO = 3

# Semilla para poder repetir exactamente el mismo experimento.
# Puedes cambiarla o poner None para obtener resultados diferentes.
SEMILLA = None


# ============================================================
# 1. CREAR MATRIZ DE DISTANCIAS
# ============================================================

def crear_matriz_distancias(n):
    """
    Crea una matriz de distancias aleatorias y simétrica.

    La distancia entre una ciudad y ella misma es 0.
    """
    
    matriz = [[0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        
        for j in range(i + 1, n):
            
            distancia = random.randint(10, 100)
            
            matriz[i][j] = distancia
            matriz[j][i] = distancia
    
    return matriz


# ============================================================
# 2. CREAR INDIVIDUO
# ============================================================

def crear_individuo(n):
    """
    Crea una ruta válida.

    Ejemplo:
    [0, 3, 1, 5, 2, 4, 7, 6]
    
    Cada ciudad aparece exactamente una vez.
    """
    
    ruta = list(range(n))
    
    random.shuffle(ruta)
    
    return ruta


# ============================================================
# 3. CREAR POBLACIÓN
# ============================================================

def crear_poblacion(n, tam_poblacion):
    """
    Crea una población inicial de rutas.
    """
    
    poblacion = []
    
    for _ in range(tam_poblacion):
        poblacion.append(crear_individuo(n))
    
    return poblacion


# ============================================================
# 4. CALCULAR DISTANCIA DE UNA RUTA
# ============================================================

def calcular_distancia(ruta, matriz):
    """
    Calcula la distancia total de una ruta.

    También incluye el regreso desde la última ciudad
    hasta la ciudad inicial.
    """
    
    distancia_total = 0
    
    for i in range(len(ruta) - 1):
        
        ciudad_actual = ruta[i]
        ciudad_siguiente = ruta[i + 1]
        
        distancia_total += matriz[
            ciudad_actual
        ][
            ciudad_siguiente
        ]
    
    # Regresar a la ciudad inicial
    ultima_ciudad = ruta[-1]
    primera_ciudad = ruta[0]
    
    distancia_total += matriz[
        ultima_ciudad
    ][
        primera_ciudad
    ]
    
    return distancia_total


# ============================================================
# 5. SELECCIÓN POR TORNEO
# ============================================================

def seleccion_torneo(
        poblacion,
        matriz,
        tam_torneo
    ):
    """
    Selecciona el individuo con menor distancia
    entre varios individuos elegidos aleatoriamente.
    """
    
    participantes = random.sample(
        poblacion,
        tam_torneo
    )
    
    ganador = min(
        participantes,
        key=lambda ruta: calcular_distancia(
            ruta,
            matriz
        )
    )
    
    return ganador.copy()


# ============================================================
# 6. CRUZAMIENTO OX
# ============================================================

def cruzamiento_ox(padre1, padre2):
    """
    Order Crossover (OX).

    Produce hijos que siguen siendo permutaciones válidas.
    """
    
    n = len(padre1)
    
    # Seleccionar dos puntos de corte
    inicio, fin = sorted(
        random.sample(range(n), 2)
    )
    
    # Crear hijos vacíos
    hijo1 = [None] * n
    hijo2 = [None] * n
    
    # Copiar segmento de cada padre
    hijo1[inicio:fin] = padre1[inicio:fin]
    hijo2[inicio:fin] = padre2[inicio:fin]
    
    # --------------------------------------------------------
    # Completar hijo 1 con información de padre 2
    # --------------------------------------------------------
    
    restantes = [
        ciudad
        for ciudad in padre2
        if ciudad not in hijo1
    ]
    
    posicion = fin % n
    
    for ciudad in restantes:
        
        while hijo1[posicion] is not None:
            posicion = (posicion + 1) % n
        
        hijo1[posicion] = ciudad
        
        posicion = (posicion + 1) % n
    
    # --------------------------------------------------------
    # Completar hijo 2 con información de padre 1
    # --------------------------------------------------------
    
    restantes = [
        ciudad
        for ciudad in padre1
        if ciudad not in hijo2
    ]
    
    posicion = fin % n
    
    for ciudad in restantes:
        
        while hijo2[posicion] is not None:
            posicion = (posicion + 1) % n
        
        hijo2[posicion] = ciudad
        
        posicion = (posicion + 1) % n
    
    return hijo1, hijo2


# ============================================================
# 7. MUTACIÓN SWAP
# ============================================================

def mutacion_swap(ruta, tasa_mutacion):
    """
    Mutación por intercambio.

    Si ocurre la mutación, se intercambian dos ciudades.
    """
    
    nueva_ruta = ruta.copy()
    
    if random.random() < tasa_mutacion:
        
        posicion1, posicion2 = random.sample(
            range(len(nueva_ruta)),
            2
        )
        
        nueva_ruta[posicion1], nueva_ruta[posicion2] = (
            nueva_ruta[posicion2],
            nueva_ruta[posicion1]
        )
    
    return nueva_ruta


# ============================================================
# 8. ALGORITMO GENÉTICO
# ============================================================

def algoritmo_genetico(
        matriz,
        tam_poblacion,
        tasa_mutacion,
        generaciones,
        elitismo,
        tam_torneo
    ):
    
    n = len(matriz)
    
    # Crear población inicial
    poblacion = crear_poblacion(
        n,
        tam_poblacion
    )
    
    mejor_ruta = None
    mejor_distancia = math.inf
    
    historial = []
    
    # --------------------------------------------------------
    # CICLO DE GENERACIONES
    # --------------------------------------------------------
    
    for generacion in range(generaciones):
        
        # Ordenar de mejor a peor
        poblacion.sort(
            key=lambda ruta: calcular_distancia(
                ruta,
                matriz
            )
        )
        
        # Mejor individuo actual
        distancia_actual = calcular_distancia(
            poblacion[0],
            matriz
        )
        
        # Actualizar mejor solución global
        if distancia_actual < mejor_distancia:
            
            mejor_distancia = distancia_actual
            mejor_ruta = poblacion[0].copy()
        
        # Guardar para la gráfica
        historial.append(
            mejor_distancia
        )
        
        # ----------------------------------------------------
        # CREAR NUEVA POBLACIÓN
        # ----------------------------------------------------
        
        nueva_poblacion = []
        
        # ELITISMO
        for i in range(elitismo):
            
            nueva_poblacion.append(
                poblacion[i].copy()
            )
        
        # Crear individuos restantes
        while len(nueva_poblacion) < tam_poblacion:
            
            # Selección
            padre1 = seleccion_torneo(
                poblacion,
                matriz,
                tam_torneo
            )
            
            padre2 = seleccion_torneo(
                poblacion,
                matriz,
                tam_torneo
            )
            
            # Cruzamiento
            hijo1, hijo2 = cruzamiento_ox(
                padre1,
                padre2
            )
            
            # Mutación
            hijo1 = mutacion_swap(
                hijo1,
                tasa_mutacion
            )
            
            hijo2 = mutacion_swap(
                hijo2,
                tasa_mutacion
            )
            
            # Agregar hijos
            nueva_poblacion.append(hijo1)
            
            if len(nueva_poblacion) < tam_poblacion:
                nueva_poblacion.append(hijo2)
        
        poblacion = nueva_poblacion
    
    return (
        mejor_ruta,
        mejor_distancia,
        historial
    )


# ============================================================
# 9. MOSTRAR MATRIZ
# ============================================================

def mostrar_matriz(matriz):
    
    print("\nMatriz de distancias:")
    
    for fila in matriz:
        
        print(fila)


# ============================================================
# 10. MOSTRAR RUTA
# ============================================================

def mostrar_ruta(ruta):
    
    ruta_mostrada = ruta + [ruta[0]]
    
    texto = " -> ".join(
        str(ciudad)
        for ciudad in ruta_mostrada
    )
    
    print(texto)


# ============================================================
# 11. PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":
    
    # Configurar semilla
    if SEMILLA is not None:
        random.seed(SEMILLA)
    
    print("=" * 60)
    print("PROBLEMA DEL AGENTE VIAJERO - ALGORITMO GENÉTICO")
    print("=" * 60)
    
    print(f"\nNúmero de ciudades: {NUM_CIUDADES}")
    print(f"Tamaño de población: {TAM_POBLACION}")
    print(f"Tasa de mutación: {TASA_MUTACION}")
    print(f"Número de generaciones: {GENERACIONES}")
    print(f"Elitismo: {ELITISMO}")
    
    # Crear matriz
    matriz = crear_matriz_distancias(
        NUM_CIUDADES
    )
    
    mostrar_matriz(matriz)
    
    # Ejecutar algoritmo
    (
        mejor_ruta,
        mejor_distancia,
        historial
    ) = algoritmo_genetico(
        matriz,
        TAM_POBLACION,
        TASA_MUTACION,
        GENERACIONES,
        ELITISMO,
        TAM_TORNEO
    )
    
    # Mostrar resultados
    print("\n" + "=" * 60)
    print("RESULTADO")
    print("=" * 60)
    
    print("\nMejor ruta encontrada:")
    mostrar_ruta(mejor_ruta)
    
    print(
        f"\nDistancia total: {mejor_distancia}"
    )
    
    # Gráfica
    plt.figure()
    
    plt.plot(historial)
    
    plt.xlabel("Generación")
    plt.ylabel("Mejor distancia")
    
    plt.title(
        "Evolución de la mejor ruta"
    )
    
    plt.grid()
    plt.show()
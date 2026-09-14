# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 12:34:12 2026

@author: anton
"""

import random
import matplotlib.pyplot as plt


# ============================================================
# 1. CREAR UN INDIVIDUO
# ============================================================

def crear_individuo(n):
    """
    Crea una solución aleatoria para N-Reinas.

    Cada número representa la fila de una reina.
    El índice representa la columna.

    Ejemplo para N=6:
    [2, 5, 1, 4, 0, 3]
    """
    
    individuo = list(range(n))
    random.shuffle(individuo)
    
    return individuo


# ============================================================
# 2. CREAR LA POBLACIÓN
# ============================================================

def crear_poblacion(n, tam_poblacion):
    """
    Crea una población de individuos.
    """
    
    poblacion = []
    
    for _ in range(tam_poblacion):
        poblacion.append(crear_individuo(n))
    
    return poblacion


# ============================================================
# 3. FUNCIÓN DE APTITUD
# ============================================================

def calcular_conflictos(individuo):
    """
    Calcula la cantidad de conflictos diagonales.

    Si dos reinas están en la misma diagonal:
        abs(fila1 - fila2) == abs(columna1 - columna2)

    Como usamos una permutación, nunca hay conflictos
    por compartir una misma fila.
    """
    
    conflictos = 0
    n = len(individuo)
    
    for i in range(n):
        for j in range(i + 1, n):
            
            diferencia_filas = abs(individuo[i] - individuo[j])
            diferencia_columnas = abs(i - j)
            
            if diferencia_filas == diferencia_columnas:
                conflictos += 1
    
    return conflictos


# ============================================================
# 4. SELECCIÓN POR TORNEO
# ============================================================

def seleccion_torneo(poblacion, tam_torneo=3):
    """
    Selecciona un individuo mediante torneo.

    Se escogen varios individuos al azar y se devuelve
    el que tenga menos conflictos.
    """
    
    participantes = random.sample(poblacion, tam_torneo)
    
    ganador = min(
        participantes,
        key=calcular_conflictos
    )
    
    return ganador.copy()


# ============================================================
# 5. CRUZAMIENTO OX (ORDER CROSSOVER)
# ============================================================

def cruzamiento_ox(padre1, padre2):
    """
    Order Crossover (OX).

    Es apropiado para cromosomas representados
    como permutaciones.
    """
    
    n = len(padre1)
    
    # Elegimos dos puntos de corte
    inicio, fin = sorted(random.sample(range(n), 2))
    
    # Crear hijos vacíos
    hijo1 = [None] * n
    hijo2 = [None] * n
    
    # Copiar segmento de los padres
    hijo1[inicio:fin] = padre1[inicio:fin]
    hijo2[inicio:fin] = padre2[inicio:fin]
    
    # Completar hijo 1 usando padre 2
    valores_padre2 = [
        gen for gen in padre2
        if gen not in hijo1
    ]
    
    posicion = fin % n
    
    for gen in valores_padre2:
        
        while hijo1[posicion] is not None:
            posicion = (posicion + 1) % n
        
        hijo1[posicion] = gen
        posicion = (posicion + 1) % n
    
    # Completar hijo 2 usando padre 1
    valores_padre1 = [
        gen for gen in padre1
        if gen not in hijo2
    ]
    
    posicion = fin % n
    
    for gen in valores_padre1:
        
        while hijo2[posicion] is not None:
            posicion = (posicion + 1) % n
        
        hijo2[posicion] = gen
        posicion = (posicion + 1) % n
    
    return hijo1, hijo2


# ============================================================
# 6. MUTACIÓN POR INTERCAMBIO
# ============================================================

def mutacion_swap(individuo, tasa_mutacion):
    """
    Realiza una mutación por intercambio.

    Con cierta probabilidad se intercambian dos posiciones.
    """
    
    individuo = individuo.copy()
    
    if random.random() < tasa_mutacion:
        
        posicion1, posicion2 = random.sample(
            range(len(individuo)),
            2
        )
        
        individuo[posicion1], individuo[posicion2] = (
            individuo[posicion2],
            individuo[posicion1]
        )
    
    return individuo


# ============================================================
# 7. ALGORITMO GENÉTICO
# ============================================================

def algoritmo_genetico(
        n,
        tam_poblacion=50,
        tasa_mutacion=0.1,
        generaciones_max=1000,
        elitismo=2
    ):
    """
    Ejecuta el algoritmo genético.

    Retorna:
        mejor_individuo
        mejor_aptitud
        generacion_solucion
        historial
    """
    
    # Crear población inicial
    poblacion = crear_poblacion(n, tam_poblacion)
    
    historial = []
    
    mejor_individuo = None
    mejor_aptitud = float("inf")
    
    for generacion in range(generaciones_max):
        
        # Ordenar población de menor a mayor conflicto
        poblacion.sort(key=calcular_conflictos)
        
        # Mejor individuo de esta generación
        actual = poblacion[0]
        aptitud_actual = calcular_conflictos(actual)
        
        # Guardar la mejor solución encontrada
        if aptitud_actual < mejor_aptitud:
            mejor_aptitud = aptitud_actual
            mejor_individuo = actual.copy()
        
        # Guardar datos para la gráfica
        historial.append(mejor_aptitud)
        
        # ¿Encontramos solución?
        if mejor_aptitud == 0:
            return (
                mejor_individuo,
                mejor_aptitud,
                generacion,
                historial
            )
        
        # ----------------------------------------------------
        # NUEVA POBLACIÓN
        # ----------------------------------------------------
        
        nueva_poblacion = []
        
        # ELITISMO
        # Conservamos directamente los mejores individuos.
        for i in range(elitismo):
            nueva_poblacion.append(
                poblacion[i].copy()
            )
        
        # Crear el resto de la población
        while len(nueva_poblacion) < tam_poblacion:
            
            # Selección
            padre1 = seleccion_torneo(poblacion)
            padre2 = seleccion_torneo(poblacion)
            
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
        
        # Reemplazar población
        poblacion = nueva_poblacion
    
    return (
        mejor_individuo,
        mejor_aptitud,
        generaciones_max,
        historial
    )


# ============================================================
# 8. MOSTRAR TABLERO
# ============================================================

def mostrar_tablero(individuo):
    """
    Muestra visualmente el tablero de N-Reinas.
    """
    
    n = len(individuo)
    
    print("\nTablero:")
    
    for fila in range(n):
        
        fila_tablero = ""
        
        for columna in range(n):
            
            if individuo[columna] == fila:
                fila_tablero += "Q "
            else:
                fila_tablero += ". "
        
        print(fila_tablero)


# ============================================================
# 9. EJECUTAR UNA PRUEBA
# ============================================================

def ejecutar_prueba(
        n,
        tam_poblacion,
        tasa_mutacion
    ):
    """
    Ejecuta una prueba individual.
    """
    
    print("\n" + "=" * 60)
    print("PRUEBA")
    print("=" * 60)
    
    print(f"N = {n}")
    print(f"Población = {tam_poblacion}")
    print(f"Tasa de mutación = {tasa_mutacion}")
    
    (
        solucion,
        conflictos,
        generacion,
        historial
    ) = algoritmo_genetico(
        n=n,
        tam_poblacion=tam_poblacion,
        tasa_mutacion=tasa_mutacion
    )
    
    print("\nMejor solución:")
    print(solucion)
    
    print(f"Conflictos: {conflictos}")
    print(f"Generación encontrada: {generacion}")
    
    mostrar_tablero(solucion)
    
    # Gráfica
    plt.figure()
    plt.plot(historial)
    plt.xlabel("Generación")
    plt.ylabel("Mejor cantidad de conflictos")
    plt.title(
        f"N={n}, Población={tam_poblacion}, "
        f"Mutación={tasa_mutacion}"
    )
    plt.grid()
    plt.show()
    
    return generacion, conflictos


# ============================================================
# 10. PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":
    
    ejecutar_prueba(
        n=6,
        tam_poblacion=50,
        tasa_mutacion=0.1
    )
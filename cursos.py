# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 13:18:42 2026

@author: anton
"""

import random


# ============================================================
# CONFIGURACIÓN
# ============================================================

NUM_CURSOS = 8
NUM_SALAS = 4
NUM_FRANJAS = 5

TAM_POBLACION = 50
GENERACIONES = 500

TASA_MUTACION = 0.10
ELITISMO = 2

SEMILLA = None


# ============================================================
# DATOS
# ============================================================

# Curso:
# [nombre, estudiantes, recursos requeridos]

cursos = [
    ["Programacion", 30, ["PC"]],
    ["Bases de Datos", 25, ["PC", "BD"]],
    ["IA", 20, ["PC", "IA"]],
    ["Redes", 35, ["PC", "RED"]],
    ["Calculo", 40, []],
    ["Diseno", 25, ["PC", "DISENO"]],
    ["Sistemas Operativos", 30, ["PC", "SO"]],
    ["Seguridad", 20, ["PC", "RED"]]
]


# Sala:
# [nombre, capacidad, recursos disponibles]

salas = [
    ["Sala A", 40, ["PC", "BD", "IA"]],
    ["Sala B", 35, ["PC", "RED", "SO"]],
    ["Sala C", 25, ["PC", "DISENO"]],
    ["Sala D", 50, ["PC", "BD", "RED", "SO", "IA"]]
]


# Franjas bloqueadas para ciertos cursos
# (curso, franja)

franjas_bloqueadas = [
    (0, 4),   # Programacion no puede ir en franja 4
    (3, 0),   # Redes no puede ir en franja 0
    (6, 2)    # Sistemas Operativos no puede ir en franja 2
]


# ============================================================
# CREAR INDIVIDUO
# ============================================================

def crear_individuo():
    """
    Cada gen contiene:
    (sala, franja)
    """

    individuo = []

    for _ in range(NUM_CURSOS):

        sala = random.randrange(NUM_SALAS)
        franja = random.randrange(NUM_FRANJAS)

        individuo.append((sala, franja))

    return individuo


# ============================================================
# CREAR POBLACIÓN
# ============================================================

def crear_poblacion():
    
    return [
        crear_individuo()
        for _ in range(TAM_POBLACION)
    ]


# ============================================================
# FUNCIÓN DE PENALIZACIÓN
# ============================================================

def calcular_penalizacion(individuo):
    
    penalizacion = 0

    # --------------------------------------------------------
    # 1. RESTRICCIONES DE CADA CURSO
    # --------------------------------------------------------

    for curso_id, (sala_id, franja) in enumerate(individuo):

        curso = cursos[curso_id]
        sala = salas[sala_id]

        estudiantes = curso[1]
        recursos_requeridos = curso[2]

        capacidad = sala[1]
        recursos_disponibles = sala[2]

        # Sobrecupo
        if estudiantes > capacidad:
            penalizacion += (estudiantes - capacidad) * 10

        # Recursos faltantes
        for recurso in recursos_requeridos:

            if recurso not in recursos_disponibles:
                penalizacion += 50

        # Franja bloqueada
        if (curso_id, franja) in franjas_bloqueadas:
            penalizacion += 100

    # --------------------------------------------------------
    # 2. DOS CURSOS EN LA MISMA SALA Y FRANJA
    # --------------------------------------------------------

    for i in range(NUM_CURSOS):

        for j in range(i + 1, NUM_CURSOS):

            sala_i, franja_i = individuo[i]
            sala_j, franja_j = individuo[j]

            if sala_i == sala_j and franja_i == franja_j:
                penalizacion += 100

    # --------------------------------------------------------
    # 3. EQUILIBRIO
    # --------------------------------------------------------

    # Penalización pequeña si una sala tiene muchos cursos
    cursos_por_sala = [0] * NUM_SALAS

    for sala, franja in individuo:
        cursos_por_sala[sala] += 1

    promedio = NUM_CURSOS / NUM_SALAS

    for cantidad in cursos_por_sala:
        penalizacion += abs(cantidad - promedio)

    return penalizacion


# ============================================================
# SELECCIÓN POR TORNEO
# ============================================================

def seleccion_torneo(poblacion):

    participantes = random.sample(
        poblacion,
        3
    )

    return min(
        participantes,
        key=calcular_penalizacion
    ).copy()


# ============================================================
# CRUZAMIENTO
# ============================================================

def cruzamiento(padre1, padre2):

    punto = random.randint(
        1,
        NUM_CURSOS - 1
    )

    hijo1 = (
        padre1[:punto] +
        padre2[punto:]
    )

    hijo2 = (
        padre2[:punto] +
        padre1[punto:]
    )

    return hijo1, hijo2


# ============================================================
# MUTACIÓN
# ============================================================

def mutacion(individuo):

    individuo = individuo.copy()

    if random.random() < TASA_MUTACION:

        curso = random.randrange(NUM_CURSOS)

        sala = random.randrange(NUM_SALAS)
        franja = random.randrange(NUM_FRANJAS)

        individuo[curso] = (sala, franja)

    return individuo


# ============================================================
# ALGORITMO GENÉTICO
# ============================================================

def algoritmo_genetico():

    poblacion = crear_poblacion()

    mejor = None
    mejor_penalizacion = float("inf")

    historial = []

    for generacion in range(GENERACIONES):

        poblacion.sort(
            key=calcular_penalizacion
        )

        actual = poblacion[0]
        penalizacion_actual = calcular_penalizacion(
            actual
        )

        if penalizacion_actual < mejor_penalizacion:

            mejor_penalizacion = penalizacion_actual
            mejor = actual.copy()

        historial.append(
            mejor_penalizacion
        )

        # Si llegamos a 0, no existen penalizaciones
        if mejor_penalizacion == 0:
            break

        nueva_poblacion = []

        # ----------------------------------------------------
        # ELITISMO
        # ----------------------------------------------------

        for i in range(ELITISMO):
            nueva_poblacion.append(
                poblacion[i].copy()
            )

        # ----------------------------------------------------
        # RESTO DE LA POBLACIÓN
        # ----------------------------------------------------

        while len(nueva_poblacion) < TAM_POBLACION:

            padre1 = seleccion_torneo(poblacion)
            padre2 = seleccion_torneo(poblacion)

            hijo1, hijo2 = cruzamiento(
                padre1,
                padre2
            )

            hijo1 = mutacion(hijo1)
            hijo2 = mutacion(hijo2)

            nueva_poblacion.append(hijo1)

            if len(nueva_poblacion) < TAM_POBLACION:
                nueva_poblacion.append(hijo2)

        poblacion = nueva_poblacion

    return mejor, mejor_penalizacion, generacion


# ============================================================
# MOSTRAR HORARIO
# ============================================================

def mostrar_horario(solucion):

    print("\nHORARIO FINAL")
    print("-" * 65)

    print(
        f"{'Curso':<25}"
        f"{'Sala':<12}"
        f"{'Franja':<10}"
        f"{'Estudiantes':<12}"
    )

    print("-" * 65)

    for curso_id, asignacion in enumerate(solucion):

        sala, franja = asignacion

        print(
            f"{cursos[curso_id][0]:<25}"
            f"{salas[sala][0]:<12}"
            f"{franja:<10}"
            f"{cursos[curso_id][1]:<12}"
        )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    if SEMILLA is not None:
        random.seed(SEMILLA)

    solucion, penalizacion, generacion = (
        algoritmo_genetico()
    )

    print("=" * 65)
    print("ASIGNACIÓN DE CURSOS A SALAS")
    print("=" * 65)

    print(f"\nPenalización final: {penalizacion}")
    print(f"Generación: {generacion}")

    mostrar_horario(solucion)
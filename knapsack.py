# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 13:20:47 2026

@author: anton
"""

import random


# ============================================================
# CONFIGURACIÓN
# ============================================================

CAPACIDAD = 100

TAM_POBLACION = 50
GENERACIONES = 500

TASA_MUTACION = 0.10
ELITISMO = 2

# "penalizacion" o "reparacion"
METODO = "penalizacion"

SEMILLA = None


# ============================================================
# DATOS DE LOS OBJETOS
# [nombre, peso, valor]
# ============================================================

objetos = [
    ["Objeto 1", 10, 60],
    ["Objeto 2", 20, 100],
    ["Objeto 3", 15, 80],
    ["Objeto 4", 25, 120],
    ["Objeto 5", 18, 90],
    ["Objeto 6", 30, 150],
    ["Objeto 7", 12, 70],
    ["Objeto 8", 22, 110],
    ["Objeto 9", 8, 50],
    ["Objeto 10", 28, 130],
    ["Objeto 11", 16, 85],
    ["Objeto 12", 24, 115],
    ["Objeto 13", 14, 75],
    ["Objeto 14", 26, 125],
    ["Objeto 15", 19, 95]
]


# ============================================================
# CREAR INDIVIDUO
# ============================================================

def crear_individuo():

    return [
        random.randint(0, 1)
        for _ in objetos
    ]


# ============================================================
# CREAR POBLACIÓN
# ============================================================

def crear_poblacion():

    return [
        crear_individuo()
        for _ in range(TAM_POBLACION)
    ]


# ============================================================
# CALCULAR PESO Y VALOR
# ============================================================

def calcular_peso(individuo):

    peso = 0

    for i in range(len(objetos)):

        if individuo[i] == 1:
            peso += objetos[i][1]

    return peso


def calcular_valor(individuo):

    valor = 0

    for i in range(len(objetos)):

        if individuo[i] == 1:
            valor += objetos[i][2]

    return valor


# ============================================================
# FUNCIÓN DE APTITUD CON PENALIZACIÓN
# ============================================================

def aptitud_penalizacion(individuo):

    peso = calcular_peso(individuo)
    valor = calcular_valor(individuo)

    # Si supera la capacidad, penalizamos
    if peso > CAPACIDAD:

        exceso = peso - CAPACIDAD

        return valor - (exceso * 10)

    return valor


# ============================================================
# REPARACIÓN
# ============================================================

def reparar(individuo):

    individuo = individuo.copy()

    while calcular_peso(individuo) > CAPACIDAD:

        objetos_seleccionados = [
            i for i in range(len(individuo))
            if individuo[i] == 1
        ]

        # Eliminar aleatoriamente uno de los objetos
        objeto = random.choice(
            objetos_seleccionados
        )

        individuo[objeto] = 0

    return individuo


# ============================================================
# FUNCIÓN DE APTITUD
# ============================================================

def aptitud(individuo):

    if METODO == "reparacion":

        individuo = reparar(individuo)

    return aptitud_penalizacion(individuo)


# ============================================================
# SELECCIÓN POR TORNEO
# ============================================================

def seleccion_torneo(poblacion):

    participantes = random.sample(
        poblacion,
        3
    )

    return max(
        participantes,
        key=aptitud
    ).copy()


# ============================================================
# CRUZAMIENTO DE UN PUNTO
# ============================================================

def cruzamiento(padre1, padre2):

    punto = random.randint(
        1,
        len(objetos) - 1
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
# MUTACIÓN DE BITS
# ============================================================

def mutacion(individuo):

    individuo = individuo.copy()

    for i in range(len(individuo)):

        if random.random() < TASA_MUTACION:

            if individuo[i] == 0:
                individuo[i] = 1
            else:
                individuo[i] = 0

    return individuo


# ============================================================
# ALGORITMO GENÉTICO
# ============================================================

def algoritmo_genetico():

    poblacion = crear_poblacion()

    mejor = None
    mejor_aptitud = float("-inf")

    generacion_mejor = 0

    for generacion in range(GENERACIONES):

        # Reparar individuos si corresponde
        if METODO == "reparacion":

            poblacion = [
                reparar(individuo)
                for individuo in poblacion
            ]

        # Ordenar de mejor a peor
        poblacion.sort(
            key=aptitud,
            reverse=True
        )

        # Mejor individuo actual
        actual = poblacion[0]

        aptitud_actual = aptitud(actual)

        if aptitud_actual > mejor_aptitud:

            mejor_aptitud = aptitud_actual
            mejor = actual.copy()

            generacion_mejor = generacion

        # Nueva población
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

    # Asegurarnos de que la solución final sea válida
    if METODO == "reparacion":

        mejor = reparar(mejor)

    return (
        mejor,
        calcular_peso(mejor),
        calcular_valor(mejor),
        generacion_mejor
    )


# ============================================================
# MOSTRAR RESULTADO
# ============================================================

def mostrar_resultado(
        mejor,
        peso,
        valor,
        generacion
    ):

    print("\n" + "=" * 60)
    print("RESULTADO")
    print("=" * 60)

    print("\nCromosoma:")
    print(mejor)

    print(f"\nPeso total: {peso}")
    print(f"Valor total: {valor}")
    print(f"Capacidad: {CAPACIDAD}")
    print(f"Generación del mejor: {generacion}")

    print("\nObjetos seleccionados:")

    for i in range(len(mejor)):

        if mejor[i] == 1:

            print(
                f"- {objetos[i][0]} "
                f"(Peso: {objetos[i][1]}, "
                f"Valor: {objetos[i][2]})"
            )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

if __name__ == "__main__":

    if SEMILLA is not None:
        random.seed(SEMILLA)

    print("=" * 60)
    print("PROBLEMA DE LA MOCHILA - KNAPSACK")
    print("=" * 60)

    print(f"\nCapacidad: {CAPACIDAD}")
    print(f"Población: {TAM_POBLACION}")
    print(f"Generaciones: {GENERACIONES}")
    print(f"Tasa de mutación: {TASA_MUTACION}")
    print(f"Método: {METODO}")

    (
        mejor,
        peso,
        valor,
        generacion
    ) = algoritmo_genetico()

    mostrar_resultado(
        mejor,
        peso,
        valor,
        generacion
    )
import random
import math
import matplotlib.pyplot as plt


NUM_CIUDADES = 10
TAM_POBLACION = 80
TASA_MUTACION = 0.20
GENERACIONES = 500
ELITISMO = 2

TAM_TORNEO = 3
SEMILLA = None


def crear_matriz_distancias(n):
    matriz = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            distancia = random.randint(10, 100)
            matriz[i][j] = distancia
            matriz[j][i] = distancia

    return matriz


def crear_individuo(n):
    ruta = list(range(n))
    random.shuffle(ruta)
    return ruta


def crear_poblacion(n, tam_poblacion):
    return [
        crear_individuo(n)
        for _ in range(tam_poblacion)
    ]


def calcular_distancia(ruta, matriz):
    distancia_total = 0

    for i in range(len(ruta)):
        ciudad_actual = ruta[i]
        ciudad_siguiente = ruta[(i + 1) % len(ruta)]

        distancia_total += matriz[ciudad_actual][ciudad_siguiente]

    return distancia_total


def seleccion_torneo(
    poblacion,
    matriz,
    tam_torneo=3
):
    participantes = random.sample(
        poblacion,
        min(tam_torneo, len(poblacion))
    )

    return min(
        participantes,
        key=lambda ruta: calcular_distancia(ruta, matriz)
    )


def cruzamiento_ox(padre1, padre2):
    n = len(padre1)

    inicio, fin = sorted(random.sample(range(n), 2))

    hijo = [None] * n
    hijo[inicio:fin] = padre1[inicio:fin]

    posicion = fin

    for ciudad in padre2:

        if ciudad not in hijo:

            if posicion >= n:
                posicion = 0

            hijo[posicion] = ciudad
            posicion += 1

    return hijo


def mutacion_swap(ruta, tasa_mutacion):
    ruta = ruta.copy()

    if random.random() < tasa_mutacion:

        i, j = random.sample(range(len(ruta)), 2)

        ruta[i], ruta[j] = ruta[j], ruta[i]

    return ruta


def algoritmo_genetico(
    matriz,
    tam_poblacion,
    tasa_mutacion,
    generaciones,
    elitismo,
    tam_torneo,
    semilla=None
):
    if semilla is not None:
        random.seed(semilla)

    n = len(matriz)

    poblacion = crear_poblacion(
        n,
        tam_poblacion
    )

    mejor_ruta = min(
        poblacion,
        key=lambda ruta: calcular_distancia(ruta, matriz)
    )

    mejor_distancia = calcular_distancia(
        mejor_ruta,
        matriz
    )

    historial = [mejor_distancia]

    for _ in range(generaciones):

        poblacion.sort(
            key=lambda ruta: calcular_distancia(ruta, matriz)
        )

        actual = poblacion[0]

        distancia_actual = calcular_distancia(
            actual,
            matriz
        )

        if distancia_actual < mejor_distancia:

            mejor_ruta = actual.copy()
            mejor_distancia = distancia_actual

        historial.append(mejor_distancia)

        nueva_poblacion = [
            ruta.copy()
            for ruta in poblacion[:elitismo]
        ]

        while len(nueva_poblacion) < tam_poblacion:

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

            hijo = cruzamiento_ox(
                padre1,
                padre2
            )

            hijo = mutacion_swap(
                hijo,
                tasa_mutacion
            )

            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

    return (
        mejor_ruta,
        mejor_distancia,
        historial
    )


def mostrar_matriz(matriz):
    print("\nMatriz de distancias:")

    for fila in matriz:
        print(fila)


def mostrar_ruta(ruta):
    ruta_mostrada = ruta + [ruta[0]]

    print(
        " -> ".join(
            str(ciudad)
            for ciudad in ruta_mostrada
        )
    )


if __name__ == "__main__":

    if SEMILLA is not None:
        random.seed(SEMILLA)

    matriz = crear_matriz_distancias(
        NUM_CIUDADES
    )

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

    mostrar_matriz(matriz)

    print("\nMejor ruta:")
    mostrar_ruta(mejor_ruta)

    print(
        "Distancia:",
        mejor_distancia
    )

    plt.plot(historial)
    plt.xlabel("Generación")
    plt.ylabel("Distancia")
    plt.title("Evolución del algoritmo genético")
    plt.grid()
    plt.show()
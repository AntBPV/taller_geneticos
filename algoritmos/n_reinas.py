import random
import matplotlib.pyplot as plt


def crear_individuo(n):
    individuo = list(range(n))
    random.shuffle(individuo)
    return individuo


def crear_poblacion(n, tam_poblacion):
    return [crear_individuo(n) for _ in range(tam_poblacion)]


def calcular_conflictos(individuo):
    conflictos = 0
    n = len(individuo)

    for i in range(n):
        for j in range(i + 1, n):

            misma_fila = individuo[i] == individuo[j]
            misma_diagonal = abs(individuo[i] - individuo[j]) == abs(i - j)

            if misma_fila or misma_diagonal:
                conflictos += 1

    return conflictos


def seleccion_torneo(poblacion, tam_torneo=3):
    participantes = random.sample(
        poblacion,
        min(tam_torneo, len(poblacion))
    )

    return min(participantes, key=calcular_conflictos)


def cruzamiento_ox(padre1, padre2):
    n = len(padre1)

    inicio, fin = sorted(random.sample(range(n), 2))

    hijo = [None] * n
    hijo[inicio:fin] = padre1[inicio:fin]

    posicion = fin

    for gen in padre2:
        if gen not in hijo:
            if posicion >= n:
                posicion = 0

            hijo[posicion] = gen
            posicion += 1

    return hijo


def mutacion_swap(individuo, tasa_mutacion):
    individuo = individuo.copy()

    if random.random() < tasa_mutacion:
        i, j = random.sample(range(len(individuo)), 2)
        individuo[i], individuo[j] = individuo[j], individuo[i]

    return individuo


def algoritmo_genetico(
    n,
    tam_poblacion=50,
    tasa_mutacion=0.1,
    generaciones_max=1000,
    elitismo=2,
    semilla=None
):
    if semilla is not None:
        random.seed(semilla)

    poblacion = crear_poblacion(n, tam_poblacion)

    mejor_individuo = min(poblacion, key=calcular_conflictos)
    mejor_aptitud = calcular_conflictos(mejor_individuo)
    generacion_mejor = 0

    historial = [mejor_aptitud]

    for generacion in range(generaciones_max):

        poblacion.sort(key=calcular_conflictos)

        actual = poblacion[0]
        actual_aptitud = calcular_conflictos(actual)

        if actual_aptitud < mejor_aptitud:
            mejor_individuo = actual.copy()
            mejor_aptitud = actual_aptitud
            generacion_mejor = generacion

        historial.append(mejor_aptitud)

        if mejor_aptitud == 0:
            break

        nueva_poblacion = [
            individuo.copy()
            for individuo in poblacion[:elitismo]
        ]

        while len(nueva_poblacion) < tam_poblacion:

            padre1 = seleccion_torneo(poblacion)
            padre2 = seleccion_torneo(poblacion)

            hijo = cruzamiento_ox(padre1, padre2)
            hijo = mutacion_swap(hijo, tasa_mutacion)

            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

    return (
        mejor_individuo,
        mejor_aptitud,
        generacion_mejor,
        historial
    )


def mostrar_tablero(individuo):
    n = len(individuo)

    for fila in range(n):
        linea = ""

        for columna in range(n):
            if individuo[columna] == fila:
                linea += "Q "
            else:
                linea += ". "

        print(linea)


def ejecutar_prueba(
    n,
    tam_poblacion=50,
    tasa_mutacion=0.1,
    generaciones_max=1000,
    elitismo=2
):
    (
        mejor,
        conflictos,
        generacion,
        historial
    ) = algoritmo_genetico(
        n,
        tam_poblacion,
        tasa_mutacion,
        generaciones_max,
        elitismo
    )

    print("Mejor solución:", mejor)
    print("Conflictos:", conflictos)
    print("Generación:", generacion)

    print("\nTablero:")
    mostrar_tablero(mejor)

    plt.plot(historial)
    plt.xlabel("Generación")
    plt.ylabel("Conflictos")
    plt.title(f"Evolución - {n} Reinas")
    plt.grid()
    plt.show()


if __name__ == "__main__":

    n = 8
    tam_poblacion = 60
    tasa_mutacion = 0.2
    generaciones_max = 1000
    elitismo = 2

    ejecutar_prueba(
        n,
        tam_poblacion,
        tasa_mutacion,
        generaciones_max,
        elitismo
    )
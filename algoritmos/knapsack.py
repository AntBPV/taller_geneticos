import random


CAPACIDAD = 140
TAM_POBLACION = 50
GENERACIONES = 500
TASA_MUTACION = 0.10
ELITISMO = 2

METODO = "penalizacion"
SEMILLA = None

# objeto | peso | valor
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


def crear_individuo():
    return [
        random.randint(0, 1)
        for _ in objetos
    ]


def crear_poblacion(tam_poblacion):
    return [
        crear_individuo()
        for _ in range(tam_poblacion)
    ]


def calcular_peso(individuo):
    return sum(
        individuo[i] * objetos[i][1]
        for i in range(len(objetos))
    )


def calcular_valor(individuo):
    return sum(
        individuo[i] * objetos[i][2]
        for i in range(len(objetos))
    )


def aptitud_penalizacion(individuo, capacidad):
    peso = calcular_peso(individuo)
    valor = calcular_valor(individuo)

    if peso > capacidad:
        exceso = peso - capacidad
        return valor - (exceso * 10)

    return valor


def reparar(individuo, capacidad):
    individuo = individuo.copy()

    while calcular_peso(individuo) > capacidad:

        seleccionados = [
            i for i in range(len(individuo))
            if individuo[i] == 1
        ]

        if not seleccionados:
            break

        indice = random.choice(seleccionados)

        individuo[indice] = 0

    return individuo


def aptitud(individuo, capacidad, metodo):

    if metodo == "reparacion":
        individuo = reparar(
            individuo,
            capacidad
        )

    return aptitud_penalizacion(
        individuo,
        capacidad
    )


def seleccion_torneo(
    poblacion,
    capacidad,
    metodo,
    tam_torneo=3
):
    participantes = random.sample(
        poblacion,
        min(tam_torneo, len(poblacion))
    )

    return max(
        participantes,
        key=lambda individuo: aptitud(
            individuo,
            capacidad,
            metodo
        )
    )


def cruzamiento(padre1, padre2):

    punto = random.randint(
        1,
        len(padre1) - 1
    )

    hijo = (
        padre1[:punto]
        + padre2[punto:]
    )

    return hijo


def mutacion(individuo, tasa_mutacion):

    individuo = individuo.copy()

    for i in range(len(individuo)):

        if random.random() < tasa_mutacion:

            individuo[i] = 1 - individuo[i]

    return individuo


def algoritmo_genetico(
    capacidad=100,
    tam_poblacion=50,
    generaciones=500,
    tasa_mutacion=0.10,
    elitismo=2,
    metodo="penalizacion",
    semilla=None
):

    if semilla is not None:
        random.seed(semilla)

    poblacion = crear_poblacion(
        tam_poblacion
    )

    if metodo == "reparacion":

        poblacion = [
            reparar(individuo, capacidad)
            for individuo in poblacion
        ]

    mejor = max(
        poblacion,
        key=lambda individuo: aptitud(
            individuo,
            capacidad,
            metodo
        )
    )

    mejor = mejor.copy()

    mejor_aptitud = aptitud(
        mejor,
        capacidad,
        metodo
    )

    generacion_mejor = 0

    for generacion in range(generaciones):

        if metodo == "reparacion":

            poblacion = [
                reparar(individuo, capacidad)
                for individuo in poblacion
            ]

        poblacion.sort(
            key=lambda individuo: aptitud(
                individuo,
                capacidad,
                metodo
            ),
            reverse=True
        )

        actual = poblacion[0]

        actual_aptitud = aptitud(
            actual,
            capacidad,
            metodo
        )

        if actual_aptitud > mejor_aptitud:

            mejor = actual.copy()
            mejor_aptitud = actual_aptitud
            generacion_mejor = generacion

        nueva_poblacion = [
            individuo.copy()
            for individuo in poblacion[:elitismo]
        ]

        while len(nueva_poblacion) < tam_poblacion:

            padre1 = seleccion_torneo(
                poblacion,
                capacidad,
                metodo
            )

            padre2 = seleccion_torneo(
                poblacion,
                capacidad,
                metodo
            )

            hijo = cruzamiento(
                padre1,
                padre2
            )

            hijo = mutacion(
                hijo,
                tasa_mutacion
            )

            if metodo == "reparacion":

                hijo = reparar(
                    hijo,
                    capacidad
                )

            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

    if metodo == "reparacion":

        mejor = reparar(
            mejor,
            capacidad
        )

    peso = calcular_peso(mejor)
    valor = calcular_valor(mejor)

    return (
        mejor,
        peso,
        valor,
        generacion_mejor
    )


def mostrar_resultado(
    individuo,
    peso,
    valor
):
    print("\nObjetos seleccionados:")

    for i in range(len(individuo)):

        if individuo[i] == 1:

            print(
                objetos[i][0],
                "- Peso:",
                objetos[i][1],
                "- Valor:",
                objetos[i][2]
            )

    print("\nPeso total:", peso)
    print("Valor total:", valor)


if __name__ == "__main__":

    if SEMILLA is not None:
        random.seed(SEMILLA)

    (
        mejor,
        peso,
        valor,
        generacion
    ) = algoritmo_genetico(
        CAPACIDAD,
        TAM_POBLACION,
        GENERACIONES,
        TASA_MUTACION,
        ELITISMO,
        METODO
    )

    mostrar_resultado(
        mejor,
        peso,
        valor
    )

    print(
        "Generación:",
        generacion
    )
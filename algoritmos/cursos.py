import random


NUM_CURSOS = 8
NUM_SALAS = 4
NUM_FRANJAS = 5

TAM_POBLACION = 50
GENERACIONES = 500
TASA_MUTACION = 0.10
ELITISMO = 2

SEMILLA = None


# Curso | Estudiantes | Requisitos
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

# Sala | Capacidad | Recursos
salas = [
    ["Sala A", 40, ["PC", "BD", "IA"]],
    ["Sala B", 35, ["PC", "RED", "SO"]],
    ["Sala C", 25, ["PC", "DISENO"]],
    ["Sala D", 50, ["PC", "BD", "RED", "SO", "IA"]]
]


franjas_bloqueadas = [
    (0, 4),
    (3, 0),
    (6, 2)
]


def crear_individuo():

    return [
        (
            random.randrange(NUM_SALAS),
            random.randrange(NUM_FRANJAS)
        )
        for _ in range(NUM_CURSOS)
    ]


def crear_poblacion(tam_poblacion):

    return [
        crear_individuo()
        for _ in range(tam_poblacion)
    ]


def calcular_penalizacion(individuo):

    penalizacion = 0

    # Capacidad y recursos
    for i, (sala, franja) in enumerate(individuo):

        nombre, estudiantes, recursos = cursos[i]
        capacidad = salas[sala][1]
        recursos_sala = salas[sala][2]

        if estudiantes > capacidad:
            penalizacion += (estudiantes - capacidad) * 10

        for recurso in recursos:
            if recurso not in recursos_sala:
                penalizacion += 50

    # Franjas bloqueadas
    for i, (sala, franja) in enumerate(individuo):

        if (i, franja) in franjas_bloqueadas:
            penalizacion += 100

    # Conflictos de sala y horario
    for i in range(NUM_CURSOS):

        sala1, franja1 = individuo[i]

        for j in range(i + 1, NUM_CURSOS):

            sala2, franja2 = individuo[j]

            if sala1 == sala2 and franja1 == franja2:
                penalizacion += 100

    return penalizacion


def seleccion_torneo(
    poblacion,
    tam_torneo=3
):

    participantes = random.sample(
        poblacion,
        min(tam_torneo, len(poblacion))
    )

    return min(
        participantes,
        key=calcular_penalizacion
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


def mutacion(
    individuo,
    tasa_mutacion
):

    individuo = individuo.copy()

    if random.random() < tasa_mutacion:

        posicion = random.randrange(
            len(individuo)
        )

        nueva_sala = random.randrange(
            NUM_SALAS
        )

        nueva_franja = random.randrange(
            NUM_FRANJAS
        )

        individuo[posicion] = (
            nueva_sala,
            nueva_franja
        )

    return individuo


def algoritmo_genetico(
    tam_poblacion=50,
    generaciones=500,
    tasa_mutacion=0.10,
    elitismo=2,
    semilla=None
):

    if semilla is not None:
        random.seed(semilla)

    poblacion = crear_poblacion(
        tam_poblacion
    )

    mejor = min(
        poblacion,
        key=calcular_penalizacion
    )

    mejor = mejor.copy()

    mejor_penalizacion = calcular_penalizacion(
        mejor
    )

    generacion_mejor = 0

    for generacion in range(generaciones):

        poblacion.sort(
            key=calcular_penalizacion
        )

        actual = poblacion[0]

        actual_penalizacion = calcular_penalizacion(
            actual
        )

        if actual_penalizacion < mejor_penalizacion:

            mejor = actual.copy()
            mejor_penalizacion = actual_penalizacion
            generacion_mejor = generacion

        if mejor_penalizacion == 0:
            break

        nueva_poblacion = [
            individuo.copy()
            for individuo in poblacion[:elitismo]
        ]

        while len(nueva_poblacion) < tam_poblacion:

            padre1 = seleccion_torneo(
                poblacion
            )

            padre2 = seleccion_torneo(
                poblacion
            )

            hijo = cruzamiento(
                padre1,
                padre2
            )

            hijo = mutacion(
                hijo,
                tasa_mutacion
            )

            nueva_poblacion.append(hijo)

        poblacion = nueva_poblacion

    return (
        mejor,
        mejor_penalizacion,
        generacion_mejor
    )


def mostrar_horario(solucion):

    print("\nHorario generado:")

    for i, (sala, franja) in enumerate(solucion):

        print(
            cursos[i][0],
            "->",
            salas[sala][0],
            "| Franja:",
            franja
        )


if __name__ == "__main__":

    if SEMILLA is not None:
        random.seed(SEMILLA)

    (
        mejor,
        penalizacion,
        generacion
    ) = algoritmo_genetico(
        TAM_POBLACION,
        GENERACIONES,
        TASA_MUTACION,
        ELITISMO
    )

    mostrar_horario(mejor)

    print(
        "\nPenalización:",
        penalizacion
    )
    
    if penalizacion == 0:
        print("Resultado: SOLUCIÓN VÁLIDA")
    else:
        print("Resultado: SOLUCIÓN INVÁLIDA")
    
    print(
        "Generación:",
        generacion
    )
from flask import Flask, render_template, request

from algoritmos import n_reinas
from algoritmos import tsp_genetico
from algoritmos import knapsack
from algoritmos import cursos


app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/n-reinas", methods=["GET", "POST"])
def n_reinas_page():

    resultado = None

    if request.method == "POST":

        n = int(request.form["n"])
        generaciones = int(
            request.form["generaciones"]
        )

        (
            solucion,
            conflictos,
            generacion,
            historial
        ) = n_reinas.algoritmo_genetico(
            n=n,
            tam_poblacion=50,
            tasa_mutacion=0.1,
            generaciones_max=generaciones,
            elitismo=2
        )

        resultado = {
            "solucion": solucion,
            "conflictos": conflictos,
            "generacion": generacion,
            "tablero": crear_tablero(solucion)
        }

    return render_template(
        "n_reinas.html",
        resultado=resultado
    )


@app.route("/tsp", methods=["GET", "POST"])
def tsp_page():

    resultado = None

    if request.method == "POST":

        ciudades = int(
            request.form["ciudades"]
        )

        generaciones = int(
            request.form["generaciones"]
        )

        matriz = tsp_genetico.crear_matriz_distancias(
            ciudades
        )

        (
            ruta,
            distancia,
            historial
        ) = tsp_genetico.algoritmo_genetico(
            matriz=matriz,
            tam_poblacion=50,
            tasa_mutacion=0.1,
            generaciones=generaciones,
            elitismo=2,
            tam_torneo=3
        )

        resultado = {
            "ruta": ruta + [ruta[0]],
            "distancia": distancia,
            "matriz": matriz
        }

    return render_template(
        "tsp_genetico.html",
        resultado=resultado
    )


@app.route("/knapsack", methods=["GET", "POST"])
def knapsack_page():

    resultado = None

    if request.method == "POST":

        capacidad = int(
            request.form["capacidad"]
        )

        generaciones = int(
            request.form["generaciones"]
        )

        metodo = request.form["metodo"]

        (
            solucion,
            peso,
            valor,
            generacion
        ) = knapsack.algoritmo_genetico(
            capacidad=capacidad,
            tam_poblacion=50,
            generaciones=generaciones,
            tasa_mutacion=0.1,
            elitismo=2,
            metodo=metodo
        )

        objetos_seleccionados = []

        for i, seleccionado in enumerate(solucion):

            if seleccionado == 1:

                objetos_seleccionados.append(
                    knapsack.objetos[i]
                )

        resultado = {
            "solucion": solucion,
            "objetos": objetos_seleccionados,
            "peso": peso,
            "valor": valor,
            "generacion": generacion,
            "metodo": metodo
        }

    return render_template(
        "knapsack.html",
        resultado=resultado
    )


@app.route("/cursos", methods=["GET", "POST"])
def cursos_page():

    resultado = None

    if request.method == "POST":

        generaciones = int(
            request.form["generaciones"]
        )

        (
            solucion,
            penalizacion,
            generacion
        ) = cursos.algoritmo_genetico(
            tam_poblacion=50,
            generaciones=generaciones,
            tasa_mutacion=0.1,
            elitismo=2
        )

        horario = []

        for i, (sala, franja) in enumerate(solucion):

            horario.append({
                "curso": cursos.cursos[i][0],
                "sala": cursos.salas[sala][0],
                "franja": franja
            })

        resultado = {
            "horario": horario,
            "penalizacion": penalizacion,
            "generacion": generacion
        }

    return render_template(
        "cursos.html",
        resultado=resultado
    )


def crear_tablero(solucion):

    n = len(solucion)
    tablero = []

    for fila in range(n):

        linea = []

        for columna in range(n):

            if solucion[columna] == fila:
                linea.append("Q")
            else:
                linea.append(".")

        tablero.append(linea)

    return tablero


if __name__ == "__main__":
    app.run(debug=True)
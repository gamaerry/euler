import time
import tracemalloc
from statistics import median

import matplotlib.pyplot as plt


def estimar_repeticiones(funcion, objetivo_segundos=0.005, max_repeticiones=100_000):
    repeticiones = 1
    resultado = None

    while repeticiones <= max_repeticiones:
        tiempo_inicial = time.process_time()
        for _ in range(repeticiones):
            resultado = funcion()
        tiempo_final = time.process_time()

        if tiempo_final - tiempo_inicial >= objetivo_segundos:
            return repeticiones, resultado

        repeticiones *= 10

    return max_repeticiones, resultado


def medir_tiempo(funcion, corridas=8, repeticiones=None, objetivo_segundos=0.005):
    if repeticiones is None:
        repeticiones, _ = estimar_repeticiones(funcion, objetivo_segundos=objetivo_segundos)

    tiempos = []
    resultados = []

    # Precalentamiento para reducir ruido de primera ejecucion.
    for _ in range(repeticiones):
        funcion()

    for _ in range(corridas):
        tiempo_inicial = time.process_time()
        for _ in range(repeticiones):
            resultado = funcion()
        tiempo_final = time.process_time()

        tiempos.append((tiempo_final - tiempo_inicial) / repeticiones)
        resultados.append(resultado)

    return {
        "resultado": resultados[0] if len(set(resultados)) == 1 else None,
        "consistente": len(set(resultados)) == 1,
        "tiempos": tiempos,
        "repeticiones": repeticiones,
    }


def medir_memoria(funcion, corridas=3):
    memorias = []
    resultados = []

    for _ in range(corridas):
        tracemalloc.start()
        resultado = funcion()
        _, memoria_pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        memorias.append(memoria_pico / 1024)
        resultados.append(resultado)

    return {
        "resultado": resultados[0] if len(set(resultados)) == 1 else None,
        "consistente": len(set(resultados)) == 1,
        "memorias": memorias,
    }


def medir(
    funcion,
    corridas_tiempo=8,
    corridas_memoria=3,
    objetivo_segundos=0.005,
):
    datos_tiempo = medir_tiempo(
        funcion,
        corridas=corridas_tiempo,
        objetivo_segundos=objetivo_segundos,
    )
    datos_memoria = medir_memoria(funcion, corridas=corridas_memoria)

    return {
        "resultado": datos_tiempo["resultado"],
        "consistente": datos_tiempo["consistente"] and datos_memoria["consistente"],
        "tiempos": datos_tiempo["tiempos"],
        "memorias": datos_memoria["memorias"],
        "repeticiones": datos_tiempo["repeticiones"],
    }


def imprimir_resumen(nombre, datos):
    def formatear_tiempo(segundos):
        if segundos >= 0.001:
            return f"{segundos:.6f} s"
        return f"{segundos:.6e} s"

    def formatear_memoria(kb):
        if kb >= 0.01:
            return f"{kb:.2f} KB"
        return f"{kb:.6e} KB"

    print(f"\n--- {nombre} ---")
    print("Resultado:", datos["resultado"])
    print("Consistente:", datos["consistente"])
    print(f"Repeticiones por corrida: {datos['repeticiones']}")
    print(f"Tiempo promedio: {formatear_tiempo(sum(datos['tiempos']) / len(datos['tiempos']))}")
    print(f"Tiempo mediano: {formatear_tiempo(median(datos['tiempos']))}")
    print(f"Tiempo minimo: {formatear_tiempo(min(datos['tiempos']))}")
    print(f"Memoria promedio: {formatear_memoria(sum(datos['memorias']) / len(datos['memorias']))}")
    print(f"Memoria mediana: {formatear_memoria(median(datos['memorias']))}")
    print(f"Memoria maxima: {formatear_memoria(max(datos['memorias']))}")


def graficar_comparacion(comparaciones):
    color_fondo_figura = "#2b2b2b"
    color_fondo_ejes = "#38383d"
    color_texto = "#f1f1f1"
    color_grilla = "#5a5a5f"
    max_corridas_tiempo = max(len(datos["tiempos"]) for datos in comparaciones.values())
    max_corridas_memoria = max(len(datos["memorias"]) for datos in comparaciones.values())
    max_tiempo = max(max(datos["tiempos"]) for datos in comparaciones.values())
    max_memoria = max(max(datos["memorias"]) for datos in comparaciones.values())

    figura_tiempo = plt.figure()
    figura_tiempo.patch.set_facecolor(color_fondo_figura)
    ejes_tiempo = plt.gca()
    ejes_tiempo.set_facecolor(color_fondo_ejes)
    for nombre, datos in comparaciones.items():
        plt.plot(datos["tiempos"], marker="o", label=nombre)
    plt.title("Tiempo por corrida", color=color_texto)
    plt.xlabel("Corrida", color=color_texto)
    plt.ylabel("Segundos", color=color_texto)
    plt.legend(facecolor=color_fondo_ejes, edgecolor=color_grilla, labelcolor=color_texto)
    plt.grid(color=color_grilla, alpha=0.4)
    plt.tick_params(colors=color_texto)
    plt.xlim(left=0, right=max_corridas_tiempo if max_corridas_tiempo > 0 else 1)
    plt.xticks(range(0, max_corridas_tiempo + 1))
    plt.ylim(bottom=0, top=max_tiempo * 1.05 if max_tiempo > 0 else 1)
    for borde in ejes_tiempo.spines.values():
        borde.set_color(color_grilla)

    figura_memoria = plt.figure()
    figura_memoria.patch.set_facecolor(color_fondo_figura)
    ejes_memoria = plt.gca()
    ejes_memoria.set_facecolor(color_fondo_ejes)
    for nombre, datos in comparaciones.items():
        plt.plot(datos["memorias"], marker="o", label=nombre)
    plt.title("Memoria pico por corrida", color=color_texto)
    plt.xlabel("Corrida", color=color_texto)
    plt.ylabel("KB", color=color_texto)
    plt.legend(facecolor=color_fondo_ejes, edgecolor=color_grilla, labelcolor=color_texto)
    plt.grid(color=color_grilla, alpha=0.4)
    plt.tick_params(colors=color_texto)
    plt.xlim(left=0, right=max_corridas_memoria if max_corridas_memoria > 0 else 1)
    plt.xticks(range(0, max_corridas_memoria + 1))
    plt.ylim(bottom=0, top=max_memoria * 1.05 if max_memoria > 0 else 1)
    for borde in ejes_memoria.spines.values():
        borde.set_color(color_grilla)

    plt.show()


def comparar_metodos(
    primer_metodo,
    segundo_metodo,
    nombre_1="Primer intento",
    nombre_2="Optimizacion",
    corridas_tiempo=8,
    corridas_memoria=4,
    objetivo_segundos=0.005,
):
    comparaciones = {
        nombre_1: medir(
            primer_metodo,
            corridas_tiempo=corridas_tiempo,
            corridas_memoria=corridas_memoria,
            objetivo_segundos=objetivo_segundos,
        ),
        nombre_2: medir(
            segundo_metodo,
            corridas_tiempo=corridas_tiempo,
            corridas_memoria=corridas_memoria,
            objetivo_segundos=objetivo_segundos,
        ),
    }

    for nombre, datos in comparaciones.items():
        imprimir_resumen(nombre, datos)

    graficar_comparacion(comparaciones)
    return comparaciones

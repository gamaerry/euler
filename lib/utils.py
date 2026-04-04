import gc
import time
import tracemalloc
from statistics import median, stdev

import matplotlib.pyplot as plt


def _resultados_consistentes(resultados):
    return all(r == resultados[0] for r in resultados[1:])


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

    gc.disable()
    try:
        for _ in range(corridas):
            tiempo_inicial = time.process_time()
            for _ in range(repeticiones):
                resultado = funcion()
            tiempo_final = time.process_time()

            tiempos.append((tiempo_final - tiempo_inicial) / repeticiones)
            resultados.append(resultado)
    finally:
        gc.enable()

    return {
        "resultado": resultados[0] if _resultados_consistentes(resultados) else None,
        "consistente": _resultados_consistentes(resultados),
        "tiempos": tiempos,
        "repeticiones": repeticiones,
    }


def medir_memoria(funcion, corridas=3):
    memorias = []
    asignaciones = []
    resultados = []

    for _ in range(corridas):
        tracemalloc.start()
        memoria_base, _ = tracemalloc.get_traced_memory()
        snapshot_antes = tracemalloc.take_snapshot()
        resultado = funcion()
        snapshot_despues = tracemalloc.take_snapshot()
        _, memoria_pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        memorias.append(max(0, (memoria_pico - memoria_base)) / 1024)
        diferencias = snapshot_despues.compare_to(snapshot_antes, "lineno")
        n_asignaciones = sum(d.count_diff for d in diferencias if d.count_diff > 0)
        asignaciones.append(n_asignaciones)
        resultados.append(resultado)

    return {
        "resultado": resultados[0] if _resultados_consistentes(resultados) else None,
        "consistente": _resultados_consistentes(resultados),
        "memorias": memorias,
        "asignaciones": asignaciones,
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
        "asignaciones": datos_memoria["asignaciones"],
        "repeticiones": datos_tiempo["repeticiones"],
    }


def _formatear_tiempo(segundos):
    if segundos >= 1:
        return f"{segundos:.4f} s"
    if segundos >= 1e-3:
        return f"{segundos * 1e3:.4f} ms"
    if segundos >= 1e-6:
        return f"{segundos * 1e6:.4f} us"
    return f"{segundos * 1e9:.4f} ns"


def _formatear_memoria(kb):
    if kb >= 1024:
        return f"{kb / 1024:.4f} MB"
    if kb >= 1:
        return f"{kb:.4f} KB"
    return f"{kb * 1024:.4f} B"


def imprimir_resumen(nombre, datos):
    tiempos = datos["tiempos"]
    memorias = datos["memorias"]

    t_promedio = sum(tiempos) / len(tiempos)
    t_mediana = median(tiempos)
    t_minimo = min(tiempos)
    t_stdev = stdev(tiempos) if len(tiempos) >= 2 else 0.0
    t_cv = (t_stdev / t_promedio * 100) if t_promedio > 0 else 0.0

    m_promedio = sum(memorias) / len(memorias)
    m_mediana = median(memorias)
    m_maxima = max(memorias)
    m_stdev = stdev(memorias) if len(memorias) >= 2 else 0.0

    print(f"\n--- {nombre} ---")
    print("Resultado:", datos["resultado"])
    print("Consistente:", datos["consistente"])
    print(f"Repeticiones por corrida: {datos['repeticiones']}")
    print(f"Tiempo promedio:  {_formatear_tiempo(t_promedio)}")
    print(f"Tiempo mediano:   {_formatear_tiempo(t_mediana)}")
    print(f"Tiempo minimo:    {_formatear_tiempo(t_minimo)}")
    print(f"Tiempo stdev:     {_formatear_tiempo(t_stdev)}  (CV: {t_cv:.1f}%)")
    print(f"Memoria promedio: {_formatear_memoria(m_promedio)}")
    print(f"Memoria mediana:  {_formatear_memoria(m_mediana)}")
    print(f"Memoria maxima:   {_formatear_memoria(m_maxima)}")
    if m_stdev > 0:
        print(f"Memoria stdev:    {_formatear_memoria(m_stdev)}")

    asignaciones = datos["asignaciones"]
    a_mediana = int(median(asignaciones))
    print(f"Asignaciones (mediana): {a_mediana}")


def _imprimir_comparacion(comparaciones):
    nombres = list(comparaciones.keys())
    d1, d2 = comparaciones[nombres[0]], comparaciones[nombres[1]]

    t1 = median(d1["tiempos"])
    t2 = median(d2["tiempos"])
    m1 = median(d1["memorias"])
    m2 = median(d2["memorias"])
    a1 = int(median(d1["asignaciones"]))
    a2 = int(median(d2["asignaciones"]))

    print("\n=== Comparacion directa ===")

    if t2 > 0 and t1 > 0:
        if t1 >= t2:
            speedup = t1 / t2
            ganador_t = nombres[1]
        else:
            speedup = t2 / t1
            ganador_t = nombres[0]
        print(f"Speedup en tiempo:    {speedup:.2f}x  (gana: {ganador_t})")
    else:
        print("Speedup en tiempo:    N/A")

    if m1 > 0 and m2 > 0:
        if m1 >= m2:
            ratio_m = m1 / m2
            ganador_m = nombres[1]
        else:
            ratio_m = m2 / m1
            ganador_m = nombres[0]
        print(f"Ratio de memoria:     {ratio_m:.2f}x  (gana: {ganador_m})")
    elif m1 == 0 and m2 == 0:
        print("Ratio de memoria:     ambos ~0")
    else:
        ganador_m = nombres[0] if m1 < m2 else nombres[1]
        print(f"Ratio de memoria:     (gana: {ganador_m})")

    if a1 == a2:
        print(f"Ratio asignaciones:   empate ({a1})")
    elif a1 > 0 or a2 > 0:
        if a1 < a2:
            ganador_a = nombres[0]
            ratio_a = a2 / a1 if a1 > 0 else float("inf")
        else:
            ganador_a = nombres[1]
            ratio_a = a1 / a2 if a2 > 0 else float("inf")
        print(f"Ratio asignaciones:   {ratio_a:.2f}x  (gana: {ganador_a})")


def graficar_comparacion(comparaciones):
    color_fondo_figura = "#2b2b2b"
    color_fondo_ejes = "#38383d"
    color_texto = "#f1f1f1"
    color_grilla = "#5a5a5f"
    colores_barras = ["#5dadec", "#f4a261"]

    nombres = list(comparaciones.keys())
    medianas_t = [median(comparaciones[n]["tiempos"]) for n in nombres]
    stdevs_t = [
        stdev(comparaciones[n]["tiempos"]) if len(comparaciones[n]["tiempos"]) >= 2 else 0
        for n in nombres
    ]
    medianas_m = [median(comparaciones[n]["memorias"]) for n in nombres]
    stdevs_m = [
        stdev(comparaciones[n]["memorias"]) if len(comparaciones[n]["memorias"]) >= 2 else 0
        for n in nombres
    ]
    medianas_a = [int(median(comparaciones[n]["asignaciones"])) for n in nombres]

    figura, (ejes_t, ejes_m, ejes_a) = plt.subplots(1, 3, figsize=(14, 4))
    figura.patch.set_facecolor(color_fondo_figura)

    def _estilizar_ejes(ejes):
        ejes.set_facecolor(color_fondo_ejes)
        ejes.tick_params(colors=color_texto)
        ejes.grid(axis="y", color=color_grilla, alpha=0.4)
        for borde in ejes.spines.values():
            borde.set_color(color_grilla)

    # --- Barras de tiempo ---
    _estilizar_ejes(ejes_t)
    barras_t = ejes_t.bar(
        nombres, medianas_t, yerr=stdevs_t,
        color=colores_barras[:len(nombres)], capsize=5, edgecolor="none",
    )
    ejes_t.set_title("Tiempo mediano", color=color_texto)
    ejes_t.set_ylabel("Segundos", color=color_texto)

    for barra, val in zip(barras_t, medianas_t):
        ejes_t.text(
            barra.get_x() + barra.get_width() / 2, barra.get_height(),
            _formatear_tiempo(val), ha="center", va="bottom",
            color=color_texto, fontsize=9,
        )

    # --- Barras de memoria ---
    _estilizar_ejes(ejes_m)
    barras_m = ejes_m.bar(
        nombres, medianas_m, yerr=stdevs_m,
        color=colores_barras[:len(nombres)], capsize=5, edgecolor="none",
    )
    ejes_m.set_title("Memoria mediana (pico neto)", color=color_texto)
    ejes_m.set_ylabel("KB", color=color_texto)

    for barra, val in zip(barras_m, medianas_m):
        ejes_m.text(
            barra.get_x() + barra.get_width() / 2, barra.get_height(),
            _formatear_memoria(val), ha="center", va="bottom",
            color=color_texto, fontsize=9,
        )

    # --- Barras de asignaciones ---
    _estilizar_ejes(ejes_a)
    barras_a = ejes_a.bar(
        nombres, medianas_a,
        color=colores_barras[:len(nombres)], edgecolor="none",
    )
    ejes_a.set_title("Asignaciones de memoria", color=color_texto)
    ejes_a.set_ylabel("Cantidad", color=color_texto)

    for barra, val in zip(barras_a, medianas_a):
        ejes_a.text(
            barra.get_x() + barra.get_width() / 2, barra.get_height(),
            str(val), ha="center", va="bottom",
            color=color_texto, fontsize=9,
        )

    figura.tight_layout()
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

    _imprimir_comparacion(comparaciones)
    graficar_comparacion(comparaciones)
    return comparaciones

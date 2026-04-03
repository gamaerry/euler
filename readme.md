http://localhost:8888/

# Project Euler - Enfoque estructurado

Repositorio personal para resolver problemas de Project Euler con un enfoque disciplinado, modular y matemáticamente fundamentado.

El objetivo es construir una base reusable de algoritmos y documentar el razonamiento detrás de cada solución, basados en:

1. Exploración → notebooks/, tests/
2. Modularización → lib/
3. Comparación → celda de comparación y eficiencia en los mismos notebooks/
4. Formalización → documentación matemática en con Typst en docs/

Este flujo permite separar claramente:
- exploración basada en la comparacion de métodos
- modulos reutilizables
- explicación formal

## Estructura del proyecto
euler/
│
├── docs/
│   └── main.typ
│
├── lib/
│   └── utils.py
│
├── notebooks/
│   ├── p000.ipynb
│   ├── p001.ipynb
│   └── ...
│
├── tests/
│   ├── usos_especiales.py
│   └── ...
│
├── pyproject.toml
└── readme.md

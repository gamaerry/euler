http://localhost:8888/

# Project Euler - Enfoque estructurado

Repositorio personal para resolver problemas de Project Euler con un enfoque disciplinado, modular y matemáticamente fundamentado.

El objetivo es construir una base reusable de algoritmos y documentar el razonamiento detrás de cada solución, basados en:

1. Exploración → notebooks/
2. Modularización → lib/
3. Comparación → celda de comparación y eficiencia
4. Formalización → documentación matemática en Typst

Este flujo permite separar claramente:
- exploración basada en la comparacion de métodos
- modulos reutilizables
- explicación formal

## Estructura del proyecto
euler/
├── lib/
│   └── utils.py
│
├── notebooks/
│   ├── p001.ipynb
│   └── ...
│
├── docs/
│   └── main.typ
│      
├── syntax/
│   └── usos_especiales.py
│
├── tests/
│   └── ...
│
├── pyproject.toml
└── README.md

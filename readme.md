http://localhost:8888/

# Project Euler — Structured Approach

Repositorio personal para resolver problemas de Project Euler con un enfoque disciplinado, modular y matemáticamente fundamentado.

El objetivo es construir una base reusable de algoritmos y documentar el razonamiento detrás de cada solución. Cada problema se aborda en tres capas:

1. Exploración → notebooks (Jupyter)
2. Implementación → código modular reutilizable
3. Formalización → documentación matemática en Typst

Este flujo permite separar claramente:
- intuición
- implementación
- explicación formal

## Estructura del proyecto
euler/
├── eulerlib/
│   ├── primes.py
│   ├── number_theory.py
│   └── utils.py
│
├── notebooks/
│   ├── p001.ipynb
│   └── ...
│
├── problems/
│   ├── p001.py
│   └── ...
│
├── docs/
│   ├── typst/
│   │   ├── main.typ
│   │   └── problems/
│   │       ├── p001.typ
│   │       └── ...
│   └── build/
│
├── tests/
│   └── ...
│
├── pyproject.toml
└── README.md

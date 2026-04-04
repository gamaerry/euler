# walrus operator
Tradicional: n = len(lista); if n > 10: print(n)
Walrus: if (n := len(lista)) > 10: print(n)

# Enumerate
fruits = ['apple', 'banana', 'cherry']
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}") # Output: 1: apple, 2: banana, 3: cherry

# Generator Expressions (regresan un iterador o iterable 'on demand')
sum(i for i in range(1000) if i % 3 == 0 or i % 5 == 0)

# List Comprehensions (se regresa una lista que usa espacio RAM)
numbers = [1, 2, 3, 4, 5]
result = ["Big Even" if n % 2 == 0 else "Big Odd" for n in numbers if n > 2] # Result: ['Big Odd', 'Big Even', 'Big Odd'] 

# lambdas como keys:
students = [('Alice', 'A', 15), ('Bob', 'B', 12), ('Charlie', 'A', 20)] 
sorted_students = sorted(students, key=lambda x: x[2]) # Output: [('Bob', 'B', 12), ('Alice', 'A', 15), ('Charlie', 'A', 20)] 

# multiple iterables dentro del map (con strict=True esto lanzaria un error al ser ambos de distinto tamaño):
list1 = [1, 2, 3] 
list2 = [10, 20, 30, 50] 
result = list(map(lambda x, y: x + y, list1, list2)) # Output: [11, 22, 33] 

# zip para agrupar elementos de listas:
names = ['Alice', 'Bob']
scores = [85, 92]
combined = list(zip(names, scores)) # [('Alice', 85), ('Bob', 92)]
nums = [10, 20, 30, 40] # Comparar elementos adyacentes
pairs = list(zip(nums, nums[1:])) # [(10, 20), (20, 30), (30, 40)]

# any: al menos uno cumple
any(n % 7 == 0 for n in range(10))  # True
# all: todos cumplen
all(n > 0 for n in [1,2,3])         # True

# memorizacion con lru_cache
from functools import lru_cache
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)

# resolución numérica y algebraica de SEL con Symphy
from sympy import Matrix
A = Matrix([[3, -2], [-3, 6]])
print(A.solve(Matrix([2, -2])))
A = Matrix([[1, 1], [1, -1]])
b = Matrix([sqrt(2), pi])
sol = A.solve(b)
print(sol)  # Matrix([(sqrt(2) + pi)/2, (sqrt(2) - pi)/2])
print(sol.evalf())  # Matrix([[2.06...], [-0.57...]])

#DESBLOQUEADOS:
# resolución numérica de SEL
A = numpy.array([[1,-1],[2,-3]])
print(numpy.linalg.solve(A, [10,0]))
# MCD, mcm y prod (desbloqueado en p005)
import math
math.gcd(48, 18, 39)
math.lcm(4, 6, 8, 10)
math.prod([10, 10, 101])
# enésimo numero primo (desbloqueado en p007)
from sympy import sieve, prime
prime(10001)
# primos en rango (desbloqueado en p010)
sieve.extend(2_000_000) # asegura que sieve alcance 2M (no exacto, se sobrepasa)
i = sieve.search(2_000_000)[0] # n-th del primo mas cercano a 2M por la izquierda
sum(sieve[:i+1]) # mas estable
sum(sieve._list[:i]) # ligeramente más optimo, pero menos estable por ser API interna
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

# Uso de lambdas como keys:
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

# memorizacion con lru_cache
from functools import lru_cache
@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)

# Máximo Común Divisor y el Mínimo Común Múltiplo.
import math
print(math.gcd(48, 18)) # 6
print(math.lcm(4, 6))   # 12

# permutations → permutaciones
list(permutations([1, 2, 3], 2)) # [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]
# combinations → combinaciones sin repetición
list(combinations([1, 2, 3], 2)) # [(1,2), (1,3), (2,3)]
# any → al menos uno cumple
any(n % 7 == 0 for n in range(10))  # True
# all → todos cumplen
all(n > 0 for n in [1,2,3])         # True

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Inlaturati elementele duplicate dintr-un array astfel incat fiecare element unic sa apara o singura data si returnati nr de elemente unice. Incercati sa faceti aceasta procesare pe array-ul initial, fara sa creati unul nou.
#
#  ex:
#  Input: nums = [1,1,2]
# Output: 2, nums = [1,2,_]

nums = [1, 1, 2]
i = 0
while i < len(nums) - 1:
    if nums[i] == nums[i + 1]:
        nums.pop(i + 1)
        nums.append("_")
    else:
        i += 1
print("Problema 1:", len([x for x in nums if x != "_"]), nums)

# 2. Folosind lambda expressions extrageti din array-ul urmator elementele pare si apoi afisati rezultatul ridicat la puterea a 2a . (se accepta si alta varianta in afara de lambda expression)
#
# numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
numbers = list(filter(lambda x: x % 2 == 0, numbers))
numbers = list(map(lambda x: x**2, numbers))
print("\nProblema 2:", numbers)

# 3.Pe baza tuplurilor de mai jos calculati urmatoarele:
#
# students = [
#
#     ("Alice", 85, 92, 88),
#
#     ("Bob", 78, 90, 83),
#
#     ("Charlie", 95, 87, 92)
#
# ]
#
# 	a. scorul mediu al fiecarui student
#
# 	b. gasiti studentul cu scorul cel mai mare
#
# 	c. creati o lista noua de tupluri care sa contina numele studentilor si scorul lor cel mai mare
#
students = [
    ("Alice", 85, 92, 88),
    ("Bob", 78, 90, 83),
    ("Charlie", 95, 87, 92)
]

avgScore = {student[0]: sum(student[1:]) / 3 for student in students}
bestStudent = max(avgScore, key=avgScore.get)
# Daca luam studentul care are nota cea mai mare din tot dictionarul
bestStudent2 = max(students, key=lambda x: max(x[1:]))
maxScores = [(student[0], max(student[1:])) for student in students]

print("\nProblema 3 - a:", avgScore)
print("Problema 3 - b:", bestStudent)
print("Problema 3 - b2:", bestStudent2)
print("Problema 3 - c:", maxScores)

# 4. Se dau urmatoarele 2 dictionare:
#
# shopping_cart = {
#
#     "apple": 2,
#
#     "banana": 3,
#
#     "orange": 1
#
# }
#
#
#
# prices = {
#
#     "apple": 0.5,
#
#     "banana": 0.3,
#
#     "orange": 0.7
#
# }
#
# 		a. Calculati costul total al elementelor din dictionar.
#
# 		b. creati un dictionar nou unde cheia este numele produsului iar valoarea este reprezentata de costul total

shopping_cart = {
    "apple": 2,
    "banana": 3,
    "orange": 1
}

prices = {
    "apple": 0.5,
    "banana": 0.3,
    "orange": 0.7
}

total_cost = sum([shopping_cart[product] * prices[product] for product in shopping_cart])
print("\nProblema 4 - a:", total_cost)
totalCost = {product: shopping_cart[product] * prices[product] for product in shopping_cart}
print("Problema 4 - b:", totalCost)

# 5. Pe baza urmatoarelor 2 dictionare, rezolvati cerintele:
#
# sales_data = {
#     'Product': ['A', 'B', 'C'],
#     'Sales': [100, 150, 200]
# }
#
# cost_data = {
#     'Product': ['A', 'B', 'C'],
#     'Cost': [50, 75, 100]
# }
#
# 	a. creati 2 dataframe-uri din cele 2 dictionare
#
# 	b. faceti merge intre ele pe baza coloanei Product
#
# 	c. calculati profitul pt fiecare produs (profitul se va calcula scazand costul)
#
# 	d. creati un bar chart pt a vizualiza profitul pt fiecare produs in parte.
#
# 2pct

sales_data = {
    'Product': ['A', 'B', 'C'],
    'Sales': [100, 150, 200]
}

cost_data = {
    'Product': ['A', 'B', 'C'],
    'Cost': [50, 75, 100]
}

# 5. a
salesDf = pd.DataFrame(sales_data)
costDf = pd.DataFrame(cost_data)

print("Head dataframses")
print("\tSales head:")
print(salesDf.head())
print("\tCost head:")
print(costDf.head())

# 5. b
mergedDf = pd.merge(salesDf, costDf, on="Product")

# 5. c
mergedDf['Profit'] = mergedDf['Sales'] - mergedDf['Cost']

# 5. d
mergedDf.plot(kind='bar', x='Product', y='Profit', legend=False, color='green')
plt.title("Profit per Product")
plt.ylabel("Profit")
plt.xlabel("Product")
plt.show()

# 6. Creati 2 clase in python. Demonstrati cu ajutorul acestora conceptul de mostenire si mai apoi conceptul de polimorfism creand o metoda suprascrisa(ovveride) si apeland aceasta metoda.
class Animal:
    def speak(self):
        print("Animal")

class Dog(Animal):
    def speak(self):
        print("Dog")

animal = Animal()
dog = Dog()
print("\nProblema 6:")
animal.speak()
dog.speak()
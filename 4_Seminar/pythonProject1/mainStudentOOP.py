import csv
import math
from fileinput import filename


class Student:
    def __init__(self, index, name, age, avgGrade):
        self.index = index
        self.name = name
        self.age = age
        self.avgGrade = avgGrade

    def toString(self):
        return "Index: " + str(self.index) + " - " + "Student Name: " + self.name + " - " + str(self.age) + " - " + str(self.avgGrade)

    # To string in py
    def __repr__(self):
        return f"Index: {self.name} - Name: {self.age} - Age: {self.age} - Grade: {self.avgGrade}"

    @staticmethod
    def calculate_indicators(arrayStud):
        sum_of_grades = 0
        for stud in arrayStud:
            sum_of_grades += stud.avgGrade
        mean = round(sum_of_grades / len(arrayStud),2)

        sum_dif_grade_mean = 0
        for stud in arrayStud:
            sum_dif_grade_mean += (stud.avgGrade - mean) ** 2

        standard_deviation = round(math.sqrt(sum_dif_grade_mean / len(arrayStud)),2)

        cov = round(standard_deviation / mean,2)

        return mean, standard_deviation, cov

    # Compare to din Java
    def __lt__(self, other):
        return self.name < other.name

filename = "students.csv"
arrayStud = []

with open(filename, 'r') as csvFile:
    reader = csv.reader(csvFile)
    next(reader)
    for row in reader:
        index = int(row[0])
        name = row[1].strip()
        age = int(row[2])
        avgGrade = float(row[3])

        student = Student(index, name, age, avgGrade)
        arrayStud.append(student)

print("Stundetii din array:")
for stud in arrayStud:
    print(stud)

# Filtrare studenti in functie de varsta
studFiltrati = []
for stud in arrayStud:
    if stud.age > 19:
        studFiltrati.append(stud)

# Metoda 2
def filter_by_age(students, min_age):
    return [student for student in students if student.age > min_age]

print("\nStundeti peste 19 ani:")
for stud in studFiltrati:
    print(stud.toString())


print("Stundeti peste 19 ani --> Metoda 2:")
print(filter_by_age(arrayStud, 19))

print("\nMedia studentilor din fisier: " + str(Student.calculate_indicators(arrayStud)))

# Stundeti sortati dupa nume
print("\nStundeti sortati")
arrayStud.sort()
for stud in arrayStud:
    print(stud.toString())

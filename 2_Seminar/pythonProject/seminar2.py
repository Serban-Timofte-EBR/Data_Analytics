import csv

stundetsFile = open('students.csv', 'r')
lines = stundetsFile.readlines()
stundetsFile.close()

# 0. Create an array of arrays from the dataset
studentsArrofArr = []
for line in lines[1:]: # Sarim peste prima linie
    values = line.strip().split(',')
    lineArr = [
        int(values[0]),
        values[1],
        int(values[2]),
        float(values[3])
    ]
    studentsArrofArr.append(lineArr)

print("Array of arrays with students info:")
print(studentsArrofArr)

# 1. Read the CSV file and create a dictionary where
# the keys are student names and the values are
# tuples containing their age and average grade.

stud_dict = {}

for studArr in studentsArrofArr:
    id = studArr[0]
    name = studArr[1]
    age = studArr[2]
    grade = studArr[3]

    stud_dict[name] = (age, grade)

print("Dictionary of arrays with students info:")
print(stud_dict)

# 2. Given the created dictionary, access the age and average
# grade of a specific student.

def getAgeGradeOfStudent(stundets_dict, student_name):
    try:
        (found_age, found_grade) = stundets_dict[student_name]
        return found_age, found_grade
    except KeyError:
        return None, None

# searched_student = 'Bob John'
searched_student = 'Bob Johnson'
searched_age, searched_grade = getAgeGradeOfStudent(stud_dict, searched_student)
if searched_grade == None or searched_age == None:
    print("Nu exista studentul!")
else:
    print(f"Stundent: {searched_student}, Age: {searched_age}, Grade: {searched_grade}")

# 3. Creating an Array from Dictionary Values

array_from_dic = []

for entry in stud_dict.keys():
    # array_from_dic.append(entry)
    (age, grade) = stud_dict[entry]
    cast_age = int(age)
    cast_grade = float(grade)
    array_from_dic.append(cast_age)
    array_from_dic.append(cast_grade)

print("Array from dict:")
print(array_from_dic)

# 4. Problem: Filter the dictionary to only include students whose
# average grade is above a certain threshold.

def getStudentsDictAboveValue(stud_dict, theshold):
    new_dict = {}
    for entry in stud_dict.keys():
        age = stud_dict[entry][0]
        grade = stud_dict[entry][1]
        if grade > theshold:
            new_dict[entry] = (age, grade)
    return new_dict

students_over_threshold = getStudentsDictAboveValue(stud_dict, 9)
print("Stundents over 9.0:")
print(students_over_threshold)

# ---------------------------Alternative-----------------------------------

# 1. Read the CSV file and create a dictionary where
# the keys are student names and the values are
# tuples containing their age and average grade.

filename = "students.csv"

def create_dict(filename):
    dict = {}
    with open(filename, 'r') as csvFile:
        reader = csv.reader(csvFile)
        next(reader)
        for row in reader:
            dict[row[1]] = (int(row[2]), float(row[3]))
    return dict

# 4. Problem: Filter the dictionary to only include students whose
# average grade is above a certain threshold.

stundets = create_dict(filename)
print("Refactored students:")
print(stundets)

nota = 8
filtered_students = {student: values for student, values in stundets.items() if values[1] > 8}
print("Stundetii filtrati:")
print(filtered_students)



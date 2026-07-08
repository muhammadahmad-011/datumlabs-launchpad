name = "Data Engineer"
age = 20
active_employee = True 
databases = ["PostgreSQL", "MSSQL", "SQLlite"]

print(f"Developer: {name}")
print(f"age: {age}")
print(f"active_employee: {active_employee}")
print(f"databases: {databases}")

for db in databases:
    if db == "PostgreSQL":
        print(f" {db}: Priority")
    else:
        print(f" {db}: Standard")

def calculate_total_records(rows, total_batches):
    return rows * total_batches

record = calculate_total_records(500, 12)
print(f"Total records processed: {record}")


class Student():
    def __init__(self,name,age,dept,marks):
        self.name = name
        self.age = age
        self.dept = dept
        self.marks = marks
        
    def display(self):
        print(f"Student name is {self.name} and age is:{self.age}")
    
    def student_marks(self):
        if self.marks >= 60:
            print("pass")
        else:
            print("fail")
    
s = Student("ali",21,"cs",61)
s1 = Student("ahmad",20,"ds",59)
print(s.name)
print(s.age)
print(s.dept)

print(s1.name)
print(s1.age)
print(s1.dept)

s.display()
s1.display()

s.student_marks()
s1.student_marks()
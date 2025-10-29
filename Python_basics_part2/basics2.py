"""
Comprehensive Python file demonstrating:
- Functions
- Classes and Objects
- Dictionaries
- Modules (imports)
- Packages (simulated structure)
"""

# ========== MODULES AND IMPORTS ==========
import math
import json
from datetime import datetime
from collections import defaultdict

# ========== FUNCTIONS ==========
def calculate_circle_area(radius):
    """Function to calculate area of a circle"""
    return math.pi * radius ** 2

def format_user_data(name, age, city):
    """Function that returns a formatted dictionary"""
    return {
        "name": name.title(),
        "age": age,
        "city": city.title(),
        "timestamp": datetime.now().isoformat()
    }

def process_student_grades(students_dict):
    """Function that processes dictionary of students and their grades"""
    results = {
        "total_students": len(students_dict),
        "average_grade": sum(students_dict.values()) / len(students_dict),
        "top_student": max(students_dict, key=students_dict.get),
        "grades_summary": defaultdict(list)
    }
    
    # Categorize grades
    for student, grade in students_dict.items():
        if grade >= 90:
            results["grades_summary"]["A"].append(student)
        elif grade >= 80:
            results["grades_summary"]["B"].append(student)
        elif grade >= 70:
            results["grades_summary"]["C"].append(student)
        else:
            results["grades_summary"]["D"].append(student)
    
    return results

# ========== CLASSES ==========
class Person:
    """Base class representing a person"""
    
    # Class variable (shared by all instances)
    species = "Homo sapiens"
    total_people = 0
    
    def __init__(self, name, age, email):
        """Constructor - initialize object attributes"""
        self.name = name
        self.age = age
        self.email = email
        self._id = f"P{datetime.now().timestamp()}"  # Private attribute
        Person.total_people += 1
    
    def introduce(self):
        """Instance method"""
        return f"Hello, I'm {self.name}, {self.age} years old."
    
    @classmethod
    def get_total_people(cls):
        """Class method"""
        return f"Total people created: {cls.total_people}"
    
    @staticmethod
    def is_adult(age):
        """Static method"""
        return age >= 18
    
    def __str__(self):
        """String representation"""
        return f"Person(name='{self.name}', age={self.age})"

class Student(Person):
    """Student class inheriting from Person"""
    
    def __init__(self, name, age, email, student_id, major):
        """Constructor with additional attributes"""
        super().__init__(name, age, email)
        self.student_id = student_id
        self.major = major
        self.courses = {}  # Dictionary to store courses and grades
    
    def enroll_course(self, course_name, grade=None):
        """Method to enroll in a course"""
        self.courses[course_name] = grade
        return f"Enrolled in {course_name}"
    
    def calculate_gpa(self):
        """Method to calculate GPA"""
        if not self.courses:
            return 0.0
        
        valid_grades = [grade for grade in self.courses.values() if grade is not None]
        if not valid_grades:
            return 0.0
        
        return sum(valid_grades) / len(valid_grades)
    
    def get_course_info(self):
        """Method returning dictionary of courses"""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "major": self.major,
            "courses_enrolled": len(self.courses),
            "gpa": self.calculate_gpa(),
            "course_details": self.courses
        }

class Classroom:
    """Class representing a classroom"""
    
    def __init__(self, room_number, capacity):
        self.room_number = room_number
        self.capacity = capacity
        self.students = []  # List to store student objects
    
    def add_student(self, student):
        """Add student to classroom"""
        if len(self.students) < self.capacity:
            self.students.append(student)
            return True
        return False
    
    def get_classroom_info(self):
        """Return classroom information as dictionary"""
        return {
            "room_number": self.room_number,
            "capacity": self.capacity,
            "current_students": len(self.students),
            "available_seats": self.capacity - len(self.students),
            "student_list": [student.name for student in self.students]
        }

# ========== DICTIONARY OPERATIONS ==========
def demonstrate_dictionaries():
    """Function to demonstrate various dictionary operations"""
    
    # Creating dictionaries
    student_grades = {
        "Alice": 85,
        "Bob": 92,
        "Charlie": 78,
        "Diana": 96,
        "Eve": 88
    }
    
    # Nested dictionary
    university_data = {
        "university": "Tech University",
        "departments": {
            "CS": {"students": 300, "courses": 45},
            "Math": {"students": 150, "courses": 30},
            "Physics": {"students": 120, "courses": 25}
        },
        "established": 1990
    }
    
    # Dictionary operations
    print("\n" + "="*50)
    print("DICTIONARY DEMONSTRATION")
    print("="*50)
    
    print(f"Original student grades: {student_grades}")
    print(f"Alice's grade: {student_grades.get('Alice', 'Not found')}")
    print(f"All students: {list(student_grades.keys())}")
    print(f"All grades: {list(student_grades.values())}")
    
    # Update dictionary
    student_grades.update({"Frank": 79, "Grace": 91})
    print(f"After update: {student_grades}")
    
    # Process grades using our function
    grade_analysis = process_student_grades(student_grades)
    print(f"Grade analysis: {json.dumps(grade_analysis, indent=2)}")
    
    return student_grades, university_data

# ========== MAIN EXECUTION ==========
def main():
    """Main function to demonstrate all concepts"""
    
    print("PYTHON CONCEPTS DEMONSTRATION")
    print("=" * 50)
    
    # Demonstrate functions
    print("\n1. FUNCTION DEMONSTRATION")
    circle_area = calculate_circle_area(5)
    user_data = format_user_data("john doe", 25, "new york")
    print(f"Circle area with radius 5: {circle_area:.2f}")
    print(f"Formatted user data: {user_data}")
    
    # Demonstrate dictionaries
    student_grades, university_data = demonstrate_dictionaries()
    
    # Demonstrate classes and objects
    print("\n" + "="*50)
    print("CLASSES AND OBJECTS DEMONSTRATION")
    print("="*50)
    
    # Create Person objects
    person1 = Person("Alice Smith", 25, "alice@email.com")
    person2 = Person("Bob Johnson", 17, "bob@email.com")
    
    print(person1.introduce())
    print(person2.introduce())
    print(f"Is Alice adult? {Person.is_adult(person1.age)}")
    print(f"Is Bob adult? {Person.is_adult(person2.age)}")
    
    # Create Student objects
    student1 = Student("Carol Davis", 20, "carol@email.com", "S123", "Computer Science")
    student2 = Student("David Wilson", 22, "david@email.com", "S124", "Mathematics")
    
    # Students enroll in courses
    student1.enroll_course("Python Programming", 95)
    student1.enroll_course("Data Structures", 88)
    student1.enroll_course("Algorithms", 92)
    
    student2.enroll_course("Calculus", 85)
    student2.enroll_course("Linear Algebra", 90)
    student2.enroll_course("Statistics", 87)
    
    print(f"\n{student1.name}'s GPA: {student1.calculate_gpa():.2f}")
    print(f"{student2.name}'s GPA: {student2.calculate_gpa():.2f}")
    
    # Demonstrate student information as dictionary
    student1_info = student1.get_course_info()
    print(f"\nStudent 1 info: {json.dumps(student1_info, indent=2)}")
    
    # Create Classroom object
    classroom = Classroom("Room 101", 30)
    classroom.add_student(student1)
    classroom.add_student(student2)
    
    classroom_info = classroom.get_classroom_info()
    print(f"\nClassroom info: {json.dumps(classroom_info, indent=2)}")
    
    # Demonstrate class method
    print(f"\n{Person.get_total_people()}")
    
    # Complex dictionary with objects
    university_records = {
        "students": {
            student1.student_id: student1.get_course_info(),
            student2.student_id: student2.get_course_info()
        },
        "classrooms": {
            classroom.room_number: classroom.get_classroom_info()
        },
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_students": Person.total_people
        }
    }
    
    print("\n" + "="*50)
    print("COMPREHENSIVE UNIVERSITY RECORDS")
    print("="*50)
    print(json.dumps(university_records, indent=2))



# ========== MODULE CHECK ==========
if __name__ == "__main__":
    main()
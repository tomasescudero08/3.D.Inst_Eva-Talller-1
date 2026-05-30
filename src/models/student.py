from datetime import datetime


class Student:
    """Modelo de estudiante"""

    def __init__(self, student_id, name, age, grade, email):
        self.id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.email = email
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        """Convierte el estudiante a diccionario para JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'grade': self.grade,
            'email': self.email,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un estudiante desde un diccionario"""
        student = cls(
            data['id'],
            data['name'],
            data['age'],
            data['grade'],
            data['email']
        )
        student.created_at = data.get('created_at', datetime.now().isoformat())
        return student

    def __str__(self):
        return f"ID: {self.id} | {self.name} | Edad: {self.age} | Grado: {self.grade} | Email: {self.email}"

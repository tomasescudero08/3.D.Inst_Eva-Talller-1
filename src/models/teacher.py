from datetime import datetime


class Teacher:
    """Modelo de profesor"""

    def __init__(self, teacher_id, name, specialty, email, salary=None):
        self.id = teacher_id
        self.name = name
        self.specialty = specialty  # Materia que enseña (ej: "Matemáticas", "Historia")
        self.email = email
        self.salary = salary
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        """Convierte el profesor a diccionario para JSON"""
        return {
            'id': self.id,
            'name': self.name,
            'specialty': self.specialty,
            'email': self.email,
            'salary': self.salary,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """Crea un profesor desde un diccionario"""
        teacher = cls(
            data['id'],
            data['name'],
            data['specialty'],
            data['email'],
            data.get('salary')
        )
        teacher.created_at = data.get('created_at', datetime.now().isoformat())
        return teacher

    def __str__(self):
        salary_info = f" | Salario: ${self.salary:,.0f}" if self.salary else ""
        return f"ID: {self.id} | {self.name} | Especialidad: {self.specialty} | Email: {self.email}{salary_info}"

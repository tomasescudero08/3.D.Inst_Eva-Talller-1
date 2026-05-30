from ..models.student import Student
from ..storage.json_storage import JSONStorage


class StudentService:
    """Maneja toda la lógica de negocio y operaciones CRUD para estudiantes"""

    def __init__(self, storage=None):
        # Dependency Injection: puedes pasar un storage diferente para testing
        self.storage = storage or JSONStorage()
        self.students = self.storage.load_students()

    def _save_changes(self):
        """Método privado para guardar cambios"""
        return self.storage.save_students(self.students)

    def get_next_id(self):
        """Genera el siguiente ID disponible"""
        if not self.students:
            return 1
        return max(student.id for student in self.students) + 1

    # ========== CREATE ==========
    def add_student(self, name, age, grade, email):
        """Agrega un nuevo estudiante"""
        # Validaciones básicas
        if not name.strip():
            print("❌ El nombre no puede estar vacío")
            return False

        if age < 5 or age > 100:
            print("❌ La edad debe estar entre 5 y 100 años")
            return False

        if not email or '@' not in email:
            print("❌ Email inválido")
            return False

        # Verificar email único
        for student in self.students:
            if student.email.lower() == email.lower():
                print(f"❌ Ya existe un estudiante con el email: {email}")
                return False

        # Crear nuevo estudiante
        new_id = self.get_next_id()
        new_student = Student(new_id, name.strip(), age, grade.strip(), email.strip())
        self.students.append(new_student)

        # Guardar cambios
        if self._save_changes():
            print(f"✅ Estudiante {name} agregado con ID: {new_id}")
            return new_id
        else:
            # Si falla el guardado, remover el estudiante de la lista
            self.students.remove(new_student)
            print("❌ Error al guardar el estudiante")
            return False

    # ========== READ ==========
    def get_all_students(self):
        """Retorna todos los estudiantes"""
        return self.students.copy()  # Retorna una copia para evitar modificaciones externas

    def get_student_by_id(self, student_id):
        """Busca un estudiante por ID"""
        for student in self.students:
            if student.id == student_id:
                return student
        return None

    def get_students_count(self):
        """Retorna el número total de estudiantes"""
        return len(self.students)

    # ========== UPDATE ==========
    def update_student(self, student_id, name=None, age=None, grade=None, email=None):
        """Actualiza un estudiante existente"""
        student = self.get_student_by_id(student_id)
        if not student:
            print(f"❌ No se encontró estudiante con ID: {student_id}")
            return False

        # Guardar datos originales para rollback en caso de error
        original_data = {
            'name': student.name,
            'age': student.age,
            'grade': student.grade,
            'email': student.email
        }

        try:
            # Mostrar datos actuales
            print(f"📋 Datos actuales: {student}")

            # Validar y actualizar campos si se proporcionan
            if name is not None and name.strip():
                student.name = name.strip()

            if age is not None:
                if 5 <= age <= 100:
                    student.age = age
                else:
                    print("❌ La edad debe estar entre 5 y 100 años")
                    return False

            if grade is not None and grade.strip():
                student.grade = grade.strip()

            if email is not None and email.strip():
                if '@' not in email:
                    print("❌ Email inválido")
                    return False

                # Verificar email único (excluyendo el estudiante actual)
                for other_student in self.students:
                    if other_student.id != student_id and other_student.email.lower() == email.strip().lower():
                        print(f"❌ Ya existe otro estudiante con el email: {email}")
                        return False

                student.email = email.strip()

            # Guardar cambios
            if self._save_changes():
                print(f"✅ Estudiante ID {student_id} actualizado correctamente")
                print(f"📋 Nuevos datos: {student}")
                return True
            else:
                # Rollback en caso de error al guardar
                student.name = original_data['name']
                student.age = original_data['age']
                student.grade = original_data['grade']
                student.email = original_data['email']
                print(f"❌ Error al guardar cambios. Datos restaurados.")
                return False

        except Exception as e:
            # Rollback en caso de error
            student.name = original_data['name']
            student.age = original_data['age']
            student.grade = original_data['grade']
            student.email = original_data['email']
            print(f"❌ Error al actualizar estudiante: {e}")
            return False

    # ========== DELETE ==========
    def delete_student(self, student_id):
        """Elimina un estudiante"""
        student = self.get_student_by_id(student_id)
        if not student:
            print(f"❌ No se encontró estudiante con ID: {student_id}")
            return False

        print(f"📋 Estudiante a eliminar: {student}")

        # Remover de la lista
        self.students.remove(student)

        # Guardar cambios
        if self._save_changes():
            print(f"✅ Estudiante ID {student_id} eliminado correctamente")
            return True
        else:
            # Rollback: volver a agregar el estudiante
            self.students.append(student)
            print(f"❌ Error al guardar cambios. Estudiante restaurado.")
            return False

    # ========== SEARCH ==========
    def search_students(self, search_term):
        """Busca estudiantes por nombre, email o grado"""
        if not search_term.strip():
            return []

        search_term = search_term.lower().strip()
        results = []

        for student in self.students:
            if (search_term in student.name.lower() or
                    search_term in student.email.lower() or
                    search_term in student.grade.lower()):
                results.append(student)

        return results

    def search_by_grade(self, grade):
        """Busca estudiantes por grado específico"""
        if not grade.strip():
            return []

        grade_lower = grade.lower().strip()
        return [student for student in self.students if grade_lower in student.grade.lower()]

    def search_by_age_range(self, min_age, max_age):
        """Busca estudiantes en un rango de edad"""
        return [student for student in self.students if min_age <= student.age <= max_age]

    # ========== STATISTICS ==========
    def get_statistics(self):
        """Retorna estadísticas del sistema"""
        if not self.students:
            return {"total": 0}

        ages = [student.age for student in self.students]
        grades = {}

        for student in self.students:
            grades[student.grade] = grades.get(student.grade, 0) + 1

        return {
            "total": len(self.students),
            "avg_age": sum(ages) / len(ages),
            "min_age": min(ages),
            "max_age": max(ages),
            "grades": grades
        }

    # ========== VALIDATION HELPERS ==========
    def validate_email(self, email):
        """Valida formato de email"""
        return email and '@' in email and '.' in email.split('@')[1]

    def validate_age(self, age):
        """Valida rango de edad"""
        return 5 <= age <= 100

    def is_email_unique(self, email, exclude_id=None):
        """Verifica si el email es único"""
        for student in self.students:
            if student.email.lower() == email.lower():
                if exclude_id is None or student.id != exclude_id:
                    return False
        return True

    # ========== UTILITY METHODS ==========
    def reload_students(self):
        """Recarga estudiantes desde el storage"""
        self.students = self.storage.load_students()
        print(f"🔄 Estudiantes recargados. Total: {len(self.students)}")

    def get_storage_info(self):
        """Retorna información sobre el storage"""
        return self.storage.get_file_info()
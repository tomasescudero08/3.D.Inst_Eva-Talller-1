from ..models.teacher import Teacher
from ..storage.json_storage import JSONStorage


class TeacherService:
    """Maneja toda la lógica de negocio y operaciones CRUD para profesores"""

    def __init__(self, storage=None):
        # Dependency Injection: usa storage específico para profesores
        self.storage = storage or JSONStorage("data/teachers.json")
        self.teachers = self.storage.load_students()  # Reutiliza el método load_students

    def _save_changes(self):
        """Método privado para guardar cambios"""
        return self.storage.save_students(self.teachers)  # Reutiliza save_students

    def get_next_id(self):
        """Genera el siguiente ID disponible"""
        if not self.teachers:
            return 1
        return max(teacher.id for teacher in self.teachers) + 1

    # ========== CREATE ==========
    def add_teacher(self, name, specialty, email, salary=None):
        """Agrega un nuevo profesor"""
        # Validaciones básicas
        if not name.strip():
            print("❌ El nombre no puede estar vacío")
            return False

        if not specialty.strip():
            print("❌ La especialidad no puede estar vacía")
            return False

        if not email or '@' not in email:
            print("❌ Email inválido")
            return False

        if salary is not None and salary < 0:
            print("❌ El salario no puede ser negativo")
            return False

        # Verificar email único
        for teacher in self.teachers:
            if teacher.email.lower() == email.lower():
                print(f"❌ Ya existe un profesor con el email: {email}")
                return False

        # Crear nuevo profesor
        new_id = self.get_next_id()
        new_teacher = Teacher(new_id, name.strip(), specialty.strip(), email.strip(), salary)
        self.teachers.append(new_teacher)

        # Guardar cambios
        if self._save_changes():
            print(f"✅ Profesor {name} agregado con ID: {new_id}")
            return new_id
        else:
            # Si falla el guardado, remover el profesor de la lista
            self.teachers.remove(new_teacher)
            print("❌ Error al guardar el profesor")
            return False

    # ========== READ ==========
    def get_all_teachers(self):
        """Retorna todos los profesores"""
        return self.teachers.copy()  # Retorna una copia para evitar modificaciones externas

    def get_teacher_by_id(self, teacher_id):
        """Busca un profesor por ID"""
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher
        return None

    def get_teachers_count(self):
        """Retorna el número total de profesores"""
        return len(self.teachers)

    # ========== UPDATE ==========
    def update_teacher(self, teacher_id, name=None, specialty=None, email=None, salary=None):
        """Actualiza un profesor existente"""
        teacher = self.get_teacher_by_id(teacher_id)
        if not teacher:
            print(f"❌ No se encontró profesor con ID: {teacher_id}")
            return False

        # Guardar datos originales para rollback en caso de error
        original_data = {
            'name': teacher.name,
            'specialty': teacher.specialty,
            'email': teacher.email,
            'salary': teacher.salary
        }

        try:
            # Mostrar datos actuales
            print(f"📋 Datos actuales: {teacher}")

            # Validar y actualizar campos si se proporcionan
            if name is not None and name.strip():
                teacher.name = name.strip()

            if specialty is not None and specialty.strip():
                teacher.specialty = specialty.strip()

            if email is not None and email.strip():
                if '@' not in email:
                    print("❌ Email inválido")
                    return False

                # Verificar email único (excluyendo el profesor actual)
                for other_teacher in self.teachers:
                    if other_teacher.id != teacher_id and other_teacher.email.lower() == email.strip().lower():
                        print(f"❌ Ya existe otro profesor con el email: {email}")
                        return False

                teacher.email = email.strip()

            if salary is not None:
                if salary < 0:
                    print("❌ El salario no puede ser negativo")
                    return False
                teacher.salary = salary

            # Guardar cambios
            if self._save_changes():
                print(f"✅ Profesor ID {teacher_id} actualizado correctamente")
                print(f"📋 Nuevos datos: {teacher}")
                return True
            else:
                # Rollback en caso de error al guardar
                teacher.name = original_data['name']
                teacher.specialty = original_data['specialty']
                teacher.email = original_data['email']
                teacher.salary = original_data['salary']
                print(f"❌ Error al guardar cambios. Datos restaurados.")
                return False

        except Exception as e:
            # Rollback en caso de error
            teacher.name = original_data['name']
            teacher.specialty = original_data['specialty']
            teacher.email = original_data['email']
            teacher.salary = original_data['salary']
            print(f"❌ Error al actualizar profesor: {e}")
            return False

    # ========== DELETE ==========
    def delete_teacher(self, teacher_id):
        """Elimina un profesor"""
        teacher = self.get_teacher_by_id(teacher_id)
        if not teacher:
            print(f"❌ No se encontró profesor con ID: {teacher_id}")
            return False

        print(f"📋 Profesor a eliminar: {teacher}")

        # Remover de la lista
        self.teachers.remove(teacher)

        # Guardar cambios
        if self._save_changes():
            print(f"✅ Profesor ID {teacher_id} eliminado correctamente")
            return True
        else:
            # Rollback: volver a agregar el profesor
            self.teachers.append(teacher)
            print(f"❌ Error al guardar cambios. Profesor restaurado.")
            return False

    # ========== SEARCH ==========
    def search_teachers(self, search_term):
        """Busca profesores por nombre, email o especialidad"""
        if not search_term.strip():
            return []

        search_term = search_term.lower().strip()
        results = []

        for teacher in self.teachers:
            if (search_term in teacher.name.lower() or
                    search_term in teacher.email.lower() or
                    search_term in teacher.specialty.lower()):
                results.append(teacher)

        return results

    def search_by_specialty(self, specialty):
        """Busca profesores por especialidad específica"""
        if not specialty.strip():
            return []

        specialty_lower = specialty.lower().strip()
        return [teacher for teacher in self.teachers if specialty_lower in teacher.specialty.lower()]

    def search_by_salary_range(self, min_salary, max_salary):
        """Busca profesores en un rango de salario"""
        return [teacher for teacher in self.teachers
                if teacher.salary is not None and min_salary <= teacher.salary <= max_salary]

    # ========== STATISTICS ==========
    def get_statistics(self):
        """Retorna estadísticas del sistema"""
        if not self.teachers:
            return {"total": 0}

        salaries = [teacher.salary for teacher in self.teachers if teacher.salary is not None]
        specialties = {}

        for teacher in self.teachers:
            specialties[teacher.specialty] = specialties.get(teacher.specialty, 0) + 1

        stats = {
            "total": len(self.teachers),
            "specialties": specialties,
            "with_salary": len(salaries)
        }

        if salaries:
            stats.update({
                "avg_salary": sum(salaries) / len(salaries),
                "min_salary": min(salaries),
                "max_salary": max(salaries)
            })

        return stats

    # ========== VALIDATION HELPERS ==========
    def validate_email(self, email):
        """Valida formato de email"""
        return email and '@' in email and '.' in email.split('@')[1]

    def validate_salary(self, salary):
        """Valida salario"""
        return salary is None or salary >= 0

    def is_email_unique(self, email, exclude_id=None):
        """Verifica si el email es único"""
        for teacher in self.teachers:
            if teacher.email.lower() == email.lower():
                if exclude_id is None or teacher.id != exclude_id:
                    return False
        return True

    # ========== UTILITY METHODS ==========
    def reload_teachers(self):
        """Recarga profesores desde el storage"""
        self.teachers = self.storage.load_students()  # Reutiliza load_students
        print(f"🔄 Profesores recargados. Total: {len(self.teachers)}")

    def get_storage_info(self):
        """Retorna información sobre el storage"""
        return self.storage.get_file_info()

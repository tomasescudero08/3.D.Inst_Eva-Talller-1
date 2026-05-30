import json
import os
from ..models.student import Student


class JSONStorage:
    """Maneja la persistencia de datos en archivos JSON"""

    def __init__(self, file_path="data/students.json"):
        self.file_path = file_path
        # Crear directorio data si no existe
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        """Crea el directorio data si no existe"""
        data_dir = os.path.dirname(self.file_path)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
            print(f"📂 Directorio {data_dir} creado")

    def load_students(self):
        """Carga estudiantes desde el archivo JSON"""
        if not os.path.exists(self.file_path):
            print(f"📂 Archivo {self.file_path} no existe, creando uno nuevo...")
            return []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                students = [Student.from_dict(student_data) for student_data in data]
                print(f"📂 Cargados {len(students)} estudiantes desde {self.file_path}")
                return students
        except json.JSONDecodeError:
            print(f"❌ Error al leer {self.file_path}, archivo JSON corrupto. Creando archivo nuevo...")
            # Hacer backup del archivo corrupto
            backup_file = f"{self.file_path}.backup"
            try:
                os.rename(self.file_path, backup_file)
                print(f"💾 Archivo corrupto guardado como {backup_file}")
            except:
                pass
            return []
        except Exception as e:
            print(f"❌ Error inesperado al cargar estudiantes: {e}")
            return []

    def save_students(self, students):
        """Guarda lista de estudiantes en el archivo JSON"""
        try:
            # Asegurar que el directorio existe
            self._ensure_data_directory()

            # Convertir estudiantes a diccionarios
            data = [student.to_dict() for student in students]

            # Guardar en JSON con formato bonito
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)

            print(f"💾 {len(students)} estudiantes guardados en {self.file_path}")
            return True
        except Exception as e:
            print(f"❌ Error al guardar estudiantes: {e}")
            return False

    def file_exists(self):
        """Verifica si el archivo JSON existe"""
        return os.path.exists(self.file_path)

    def get_file_info(self):
        """Retorna información sobre el archivo JSON"""
        if not self.file_exists():
            return {"exists": False}

        try:
            stat = os.stat(self.file_path)
            return {
                "exists": True,
                "size": stat.st_size,
                "modified": stat.st_mtime,
                "path": self.file_path
            }
        except Exception as e:
            return {"exists": True, "error": str(e)}
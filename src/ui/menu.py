from ..services.student_service import StudentService


class StudentMenu:
    """Interfaz de usuario para el sistema de estudiantes"""

    def __init__(self, student_service=None):
        # Dependency Injection: puedes pasar un servicio diferente para testing
        self.service = student_service or StudentService()

    def show_menu(self):
        """Muestra el menú principal"""
        print("\n" + "=" * 50)
        print("🎓 SISTEMA DE GESTIÓN DE ESTUDIANTES")
        print("=" * 50)
        print("1️⃣  Ver todos los estudiantes")
        print("2️⃣  Buscar estudiante por ID")
        print("3️⃣  Agregar nuevo estudiante")
        print("4️⃣  Actualizar estudiante")
        print("5️⃣  Eliminar estudiante")
        print("6️⃣  Buscar estudiantes")
        print("7️⃣  Estadísticas")
        print("8️⃣  Búsquedas avanzadas")
        print("9️⃣  Información del sistema")
        print("0️⃣  Salir")
        print("-" * 50)

    def show_advanced_search_menu(self):
        """Muestra el submenú de búsquedas avanzadas"""
        print("\n" + "=" * 40)
        print("🔍 BÚSQUEDAS AVANZADAS")
        print("=" * 40)
        print("1️⃣  Buscar por grado")
        print("2️⃣  Buscar por rango de edad")
        print("3️⃣  Buscar por término general")
        print("0️⃣  Volver al menú principal")
        print("-" * 40)

    def get_input(self, prompt, input_type=str):
        """Obtiene entrada del usuario con validación"""
        while True:
            try:
                value = input(prompt).strip()
                if input_type == int:
                    return int(value)
                elif input_type == str:
                    return value
            except ValueError:
                print("❌ Por favor ingresa un valor válido")
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                exit()

    def get_optional_input(self, prompt, current_value):
        """Obtiene entrada opcional, mostrando valor actual"""
        value = input(f"{prompt} [{current_value}]: ").strip()
        return value if value else None

    def display_students(self, students, title="Estudiantes"):
        """Muestra lista de estudiantes"""
        if not students:
            print(f"❌ No hay {title.lower()} para mostrar")
            return

        print(f"\n📋 {title.upper()}")
        print("📊 Total:", len(students))
        print("-" * 80)
        for student in students:
            print(student)

    def display_student_details(self, student):
        """Muestra detalles completos de un estudiante"""
        if not student:
            print("❌ Estudiante no encontrado")
            return

        print(f"\n👤 DETALLES DEL ESTUDIANTE")
        print("-" * 40)
        print(f"ID: {student.id}")
        print(f"Nombre: {student.name}")
        print(f"Edad: {student.age} años")
        print(f"Grado: {student.grade}")
        print(f"Email: {student.email}")
        print(f"Creado: {student.created_at}")

    def show_statistics(self):
        """Muestra estadísticas del sistema"""
        stats = self.service.get_statistics()

        if stats["total"] == 0:
            print("❌ No hay estudiantes para mostrar estadísticas")
            return

        print(f"\n📊 ESTADÍSTICAS DEL SISTEMA")
        print("-" * 30)
        print(f"Total de estudiantes: {stats['total']}")
        print(f"Edad promedio: {stats['avg_age']:.1f} años")
        print(f"Edad mínima: {stats['min_age']} años")
        print(f"Edad máxima: {stats['max_age']} años")

        print("\n📚 Estudiantes por grado:")
        for grade, count in sorted(stats['grades'].items()):
            print(f"  {grade}: {count} estudiantes")

    def show_system_info(self):
        """Muestra información del sistema"""
        storage_info = self.service.get_storage_info()
        stats = self.service.get_statistics()

        print(f"\n🔧 INFORMACIÓN DEL SISTEMA")
        print("-" * 30)
        print(f"Total de estudiantes: {stats['total']}")

        if storage_info.get('exists'):
            print(f"Archivo de datos: {storage_info.get('path', 'N/A')}")
            print(f"Tamaño del archivo: {storage_info.get('size', 0)} bytes")
        else:
            print("Archivo de datos: No existe aún")

    def confirm_action(self, message):
        """Solicita confirmación del usuario"""
        response = self.get_input(f"⚠️  {message} (s/N): ").lower()
        return response in ['s', 'si', 'sí', 'yes', 'y']

    def pause(self):
        """Pausa la ejecución esperando input del usuario"""
        input("\n⏸️  Presiona Enter para continuar...")

    # ========== OPERACIONES CRUD ==========

    def handle_view_all_students(self):
        """Maneja la opción de ver todos los estudiantes"""
        students = self.service.get_all_students()
        self.display_students(students, "Todos los estudiantes")

    def handle_search_by_id(self):
        """Maneja la búsqueda por ID"""
        student_id = self.get_input("📝 Ingresa el ID del estudiante: ", int)
        student = self.service.get_student_by_id(student_id)
        if student:
            self.display_student_details(student)
        else:
            print(f"❌ No se encontró estudiante con ID: {student_id}")

    def handle_add_student(self):
        """Maneja la creación de nuevo estudiante"""
        print("\n📝 AGREGAR NUEVO ESTUDIANTE")
        print("-" * 30)

        name = self.get_input("Nombre completo: ")
        age = self.get_input("Edad: ", int)
        grade = self.get_input("Grado/Curso: ")
        email = self.get_input("Email: ")

        result = self.service.add_student(name, age, grade, email)
        if result:
            print(f"🎉 ¡Estudiante agregado exitosamente!")

    def handle_update_student(self):
        """Maneja la actualización de estudiante"""
        student_id = self.get_input("📝 ID del estudiante a actualizar: ", int)
        student = self.service.get_student_by_id(student_id)

        if not student:
            print(f"❌ No se encontró estudiante con ID: {student_id}")
            return

        print("\n📝 ACTUALIZAR ESTUDIANTE")
        print("💡 Presiona Enter para mantener el valor actual")
        print("-" * 50)

        # Mostrar datos actuales
        self.display_student_details(student)
        print()

        # Obtener nuevos valores
        name = self.get_optional_input("Nuevo nombre", student.name)

        age_str = self.get_optional_input("Nueva edad", student.age)
        age = int(age_str) if age_str else None

        grade = self.get_optional_input("Nuevo grado", student.grade)
        email = self.get_optional_input("Nuevo email", student.email)

        # Actualizar
        success = self.service.update_student(student_id, name, age, grade, email)
        if success:
            print(f"🎉 ¡Estudiante actualizado exitosamente!")

    def handle_delete_student(self):
        """Maneja la eliminación de estudiante"""
        student_id = self.get_input("📝 ID del estudiante a eliminar: ", int)
        student = self.service.get_student_by_id(student_id)

        if not student:
            print(f"❌ No se encontró estudiante con ID: {student_id}")
            return

        # Mostrar información del estudiante a eliminar
        self.display_student_details(student)

        # Confirmar eliminación
        if self.confirm_action("¿Estás seguro de eliminar este estudiante?"):
            success = self.service.delete_student(student_id)
            if success:
                print(f"🎉 ¡Estudiante eliminado exitosamente!")
        else:
            print("❌ Eliminación cancelada")

    def handle_search_students(self):
        """Maneja la búsqueda general de estudiantes"""
        search_term = self.get_input("📝 Buscar (nombre, email o grado): ")
        results = self.service.search_students(search_term)
        self.display_students(results, f"Resultados de búsqueda: '{search_term}'")

    def handle_advanced_search(self):
        """Maneja el submenú de búsquedas avanzadas"""
        while True:
            self.show_advanced_search_menu()
            option = self.get_input("🔍 Selecciona una opción: ", str)

            if option == "0":
                break
            elif option == "1":
                grade = self.get_input("📝 Ingresa el grado a buscar: ")
                results = self.service.search_by_grade(grade)
                self.display_students(results, f"Estudiantes del grado: {grade}")
            elif option == "2":
                min_age = self.get_input("📝 Edad mínima: ", int)
                max_age = self.get_input("📝 Edad máxima: ", int)
                results = self.service.search_by_age_range(min_age, max_age)
                self.display_students(results, f"Estudiantes entre {min_age} y {max_age} años")
            elif option == "3":
                search_term = self.get_input("📝 Término de búsqueda: ")
                results = self.service.search_students(search_term)
                self.display_students(results, f"Búsqueda: '{search_term}'")
            else:
                print("❌ Opción inválida")

            if option != "0":
                self.pause()

    # ========== LOOP PRINCIPAL ==========

    def run(self):
        """Ejecuta el menú principal"""
        print("🚀 Iniciando Sistema de Gestión de Estudiantes...")

        try:
            while True:
                self.show_menu()
                option = self.get_input("🔍 Selecciona una opción: ", str)

                if option == "0":
                    print("👋 ¡Hasta luego!")
                    break
                elif option == "1":
                    self.handle_view_all_students()
                elif option == "2":
                    self.handle_search_by_id()
                elif option == "3":
                    self.handle_add_student()
                elif option == "4":
                    self.handle_update_student()
                elif option == "5":
                    self.handle_delete_student()
                elif option == "6":
                    self.handle_search_students()
                elif option == "7":
                    self.show_statistics()
                elif option == "8":
                    self.handle_advanced_search()
                elif option == "9":
                    self.show_system_info()
                else:
                    print("❌ Opción inválida. Intenta de nuevo.")

                if option != "0" and option != "8":  # No pausar después de búsquedas avanzadas
                    self.pause()

        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")

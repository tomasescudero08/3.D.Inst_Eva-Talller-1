from ..services.teacher_service import TeacherService


class TeacherMenu:
    """Interfaz de usuario para el sistema de profesores"""

    def __init__(self, teacher_service=None):
        # Dependency Injection: puedes pasar un servicio diferente para testing
        self.service = teacher_service or TeacherService()

    def show_menu(self):
        """Muestra el menú principal de profesores"""
        print("\n" + "=" * 50)
        print("👨‍🏫 GESTIÓN DE PROFESORES")
        print("=" * 50)
        print("1️⃣  Ver todos los profesores")
        print("2️⃣  Buscar profesor por ID")
        print("3️⃣  Agregar nuevo profesor")
        print("4️⃣  Actualizar profesor")
        print("5️⃣  Eliminar profesor")
        print("6️⃣  Buscar profesores")
        print("7️⃣  Estadísticas")
        print("8️⃣  Búsquedas avanzadas")
        print("9️⃣  Información del sistema")
        print("0️⃣  Volver al menú principal")
        print("-" * 50)

    def show_advanced_search_menu(self):
        """Muestra el submenú de búsquedas avanzadas para profesores"""
        print("\n" + "=" * 40)
        print("🔍 BÚSQUEDAS AVANZADAS - PROFESORES")
        print("=" * 40)
        print("1️⃣  Buscar por especialidad")
        print("2️⃣  Buscar por rango de salario")
        print("3️⃣  Buscar por término general")
        print("0️⃣  Volver al menú de profesores")
        print("-" * 40)

    def get_input(self, prompt, input_type=str):
        """Obtiene entrada del usuario con validación"""
        while True:
            try:
                value = input(prompt).strip()
                if input_type == int:
                    return int(value)
                elif input_type == float:
                    return float(value)
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

    def get_optional_float_input(self, prompt, current_value):
        """Obtiene entrada opcional de float, mostrando valor actual"""
        value_str = input(f"{prompt} [{current_value}]: ").strip()
        if not value_str:
            return None
        try:
            return float(value_str)
        except ValueError:
            print("❌ Valor numérico inválido")
            return None

    def display_teachers(self, teachers, title="Profesores"):
        """Muestra lista de profesores"""
        if not teachers:
            print(f"❌ No hay {title.lower()} para mostrar")
            return

        print(f"\n📋 {title.upper()}")
        print("📊 Total:", len(teachers))
        print("-" * 90)
        for teacher in teachers:
            print(teacher)

    def display_teacher_details(self, teacher):
        """Muestra detalles completos de un profesor"""
        if not teacher:
            print("❌ Profesor no encontrado")
            return

        print(f"\n👨‍🏫 DETALLES DEL PROFESOR")
        print("-" * 40)
        print(f"ID: {teacher.id}")
        print(f"Nombre: {teacher.name}")
        print(f"Especialidad: {teacher.specialty}")
        print(f"Email: {teacher.email}")
        print(f"Salario: ${teacher.salary:,.0f}" if teacher.salary else "Salario: No especificado")
        print(f"Creado: {teacher.created_at}")

    def show_statistics(self):
        """Muestra estadísticas del sistema de profesores"""
        stats = self.service.get_statistics()

        if stats["total"] == 0:
            print("❌ No hay profesores para mostrar estadísticas")
            return

        print(f"\n📊 ESTADÍSTICAS DE PROFESORES")
        print("-" * 35)
        print(f"Total de profesores: {stats['total']}")
        print(f"Profesores con salario: {stats['with_salary']}")

        if stats.get('avg_salary'):
            print(f"Salario promedio: ${stats['avg_salary']:,.0f}")
            print(f"Salario mínimo: ${stats['min_salary']:,.0f}")
            print(f"Salario máximo: ${stats['max_salary']:,.0f}")

        print("\n📚 Profesores por especialidad:")
        for specialty, count in sorted(stats['specialties'].items()):
            print(f"  {specialty}: {count} profesores")

    def show_system_info(self):
        """Muestra información del sistema de profesores"""
        storage_info = self.service.get_storage_info()
        stats = self.service.get_statistics()

        print(f"\n🔧 INFORMACIÓN DEL SISTEMA - PROFESORES")
        print("-" * 40)
        print(f"Total de profesores: {stats['total']}")

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

    def handle_view_all_teachers(self):
        """Maneja la opción de ver todos los profesores"""
        teachers = self.service.get_all_teachers()
        self.display_teachers(teachers, "Todos los profesores")

    def handle_search_by_id(self):
        """Maneja la búsqueda por ID"""
        teacher_id = self.get_input("📝 Ingresa el ID del profesor: ", int)
        teacher = self.service.get_teacher_by_id(teacher_id)
        if teacher:
            self.display_teacher_details(teacher)
        else:
            print(f"❌ No se encontró profesor con ID: {teacher_id}")

    def handle_add_teacher(self):
        """Maneja la creación de nuevo profesor"""
        print("\n📝 AGREGAR NUEVO PROFESOR")
        print("-" * 30)

        name = self.get_input("Nombre completo: ")
        specialty = self.get_input("Especialidad/Materia: ")
        email = self.get_input("Email: ")

        # Salario opcional
        salary_str = input("Salario (opcional, presiona Enter para omitir): ").strip()
        salary = None
        if salary_str:
            try:
                salary = float(salary_str)
            except ValueError:
                print("⚠️ Salario inválido, se guardará sin salario")
                salary = None

        result = self.service.add_teacher(name, specialty, email, salary)
        if result:
            print(f"🎉 ¡Profesor agregado exitosamente!")

    def handle_update_teacher(self):
        """Maneja la actualización de profesor"""
        teacher_id = self.get_input("📝 ID del profesor a actualizar: ", int)
        teacher = self.service.get_teacher_by_id(teacher_id)

        if not teacher:
            print(f"❌ No se encontró profesor con ID: {teacher_id}")
            return

        print("\n📝 ACTUALIZAR PROFESOR")
        print("💡 Presiona Enter para mantener el valor actual")
        print("-" * 50)

        # Mostrar datos actuales
        self.display_teacher_details(teacher)
        print()

        # Obtener nuevos valores
        name = self.get_optional_input("Nuevo nombre", teacher.name)
        specialty = self.get_optional_input("Nueva especialidad", teacher.specialty)
        email = self.get_optional_input("Nuevo email", teacher.email)

        # Salario con manejo especial
        current_salary = teacher.salary if teacher.salary else "No especificado"
        salary = self.get_optional_float_input("Nuevo salario", current_salary)

        # Actualizar
        success = self.service.update_teacher(teacher_id, name, specialty, email, salary)
        if success:
            print(f"🎉 ¡Profesor actualizado exitosamente!")

    def handle_delete_teacher(self):
        """Maneja la eliminación de profesor"""
        teacher_id = self.get_input("📝 ID del profesor a eliminar: ", int)
        teacher = self.service.get_teacher_by_id(teacher_id)

        if not teacher:
            print(f"❌ No se encontró profesor con ID: {teacher_id}")
            return

        # Mostrar información del profesor a eliminar
        self.display_teacher_details(teacher)

        # Confirmar eliminación
        if self.confirm_action("¿Estás seguro de eliminar este profesor?"):
            success = self.service.delete_teacher(teacher_id)
            if success:
                print(f"🎉 ¡Profesor eliminado exitosamente!")
        else:
            print("❌ Eliminación cancelada")

    def handle_search_teachers(self):
        """Maneja la búsqueda general de profesores"""
        search_term = self.get_input("📝 Buscar (nombre, email o especialidad): ")
        results = self.service.search_teachers(search_term)
        self.display_teachers(results, f"Resultados de búsqueda: '{search_term}'")

    def handle_advanced_search(self):
        """Maneja el submenú de búsquedas avanzadas"""
        while True:
            self.show_advanced_search_menu()
            option = self.get_input("🔍 Selecciona una opción: ", str)

            if option == "0":
                break
            elif option == "1":
                specialty = self.get_input("📝 Ingresa la especialidad a buscar: ")
                results = self.service.search_by_specialty(specialty)
                self.display_teachers(results, f"Profesores de especialidad: {specialty}")
            elif option == "2":
                min_salary = self.get_input("📝 Salario mínimo: ", float)
                max_salary = self.get_input("📝 Salario máximo: ", float)
                results = self.service.search_by_salary_range(min_salary, max_salary)
                self.display_teachers(results, f"Profesores con salario entre ${min_salary:,.0f} y ${max_salary:,.0f}")
            elif option == "3":
                search_term = self.get_input("📝 Término de búsqueda: ")
                results = self.service.search_teachers(search_term)
                self.display_teachers(results, f"Búsqueda: '{search_term}'")
            else:
                print("❌ Opción inválida")

            if option != "0":
                self.pause()

    # ========== LOOP PRINCIPAL ==========

    def run(self):
        """Ejecuta el menú principal de profesores"""
        print("🚀 Iniciando Sistema de Gestión de Profesores...")

        try:
            while True:
                self.show_menu()
                option = self.get_input("🔍 Selecciona una opción: ", str)

                if option == "0":
                    print("👋 Volviendo al menú principal...")
                    break
                elif option == "1":
                    self.handle_view_all_teachers()
                elif option == "2":
                    self.handle_search_by_id()
                elif option == "3":
                    self.handle_add_teacher()
                elif option == "4":
                    self.handle_update_teacher()
                elif option == "5":
                    self.handle_delete_teacher()
                elif option == "6":
                    self.handle_search_teachers()
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
            print("\n\n👋 Volviendo al menú principal...")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")

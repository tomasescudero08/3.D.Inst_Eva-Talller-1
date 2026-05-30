"""
Sistema Académico - Gestión de Estudiantes y Profesores
Punto de entrada principal del sistema

Versión: 2.0
Funcionalidades: Estudiantes + Profesores
"""

from src.ui.menu import StudentMenu
from src.ui.teacher_menu import TeacherMenu


class AcademicSystemMenu:
    """Menú principal del sistema académico"""

    def __init__(self):
        self.student_menu = StudentMenu()
        self.teacher_menu = TeacherMenu()

    def show_main_menu(self):
        """Muestra el menú principal del sistema"""
        print("\n" + "=" * 60)
        print("🏫 SISTEMA ACADÉMICO - GESTIÓN INTEGRAL")
        print("=" * 60)
        print("📚 Selecciona el módulo que deseas gestionar:")
        print()
        print("1️⃣  🎓 Gestión de Estudiantes")
        print("2️⃣  👨‍🏫 Gestión de Profesores")
        print("3️⃣  📊 Estadísticas Generales")
        print("4️⃣  ℹ️  Información del Sistema")
        print("0️⃣  🚪 Salir del Sistema")
        print("-" * 60)

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

    def show_general_statistics(self):
        """Muestra estadísticas generales del sistema"""
        print("\n📊 ESTADÍSTICAS GENERALES DEL SISTEMA")
        print("=" * 50)

        # Estadísticas de estudiantes
        try:
            student_stats = self.student_menu.service.get_statistics()
            print(f"🎓 ESTUDIANTES:")
            print(f"   Total de estudiantes: {student_stats.get('total', 0)}")
            if student_stats.get('total', 0) > 0:
                print(f"   Edad promedio: {student_stats.get('avg_age', 0):.1f} años")
                print(f"   Grados activos: {len(student_stats.get('grades', {}))}")
        except Exception as e:
            print(f"   ❌ Error al obtener estadísticas de estudiantes: {e}")

        print()

        # Estadísticas de profesores
        try:
            teacher_stats = self.teacher_menu.service.get_statistics()
            print(f"👨‍🏫 PROFESORES:")
            print(f"   Total de profesores: {teacher_stats.get('total', 0)}")
            if teacher_stats.get('total', 0) > 0:
                if teacher_stats.get('avg_salary'):
                    print(f"   Salario promedio: ${teacher_stats.get('avg_salary', 0):,.0f}")
                print(f"   Especialidades: {len(teacher_stats.get('specialties', {}))}")
        except Exception as e:
            print(f"   ❌ Error al obtener estadísticas de profesores: {e}")

        print()
        print("💡 Para estadísticas detalladas, accede a cada módulo específico")

    def show_system_info(self):
        """Muestra información general del sistema"""
        print("\n🔧 INFORMACIÓN DEL SISTEMA ACADÉMICO")
        print("=" * 45)
        print("📋 Módulos disponibles:")
        print("   ✅ Gestión de Estudiantes")
        print("   ✅ Gestión de Profesores")
        print("   🔲 Gestión de Materias (Próximamente)")
        print("   🔲 Gestión de Notas (Próximamente)")
        print()
        print("💾 Almacenamiento:")

        # Info de estudiantes
        try:
            student_storage_info = self.student_menu.service.get_storage_info()
            if student_storage_info.get('exists'):
                print(f"   📁 students.json: {student_storage_info.get('size', 0)} bytes")
            else:
                print("   📁 students.json: No existe")
        except:
            print("   📁 students.json: Error al acceder")

        # Info de profesores
        try:
            teacher_storage_info = self.teacher_menu.service.get_storage_info()
            if teacher_storage_info.get('exists'):
                print(f"   📁 teachers.json: {teacher_storage_info.get('size', 0)} bytes")
            else:
                print("   📁 teachers.json: No existe")
        except:
            print("   📁 teachers.json: Error al acceder")

        print()
        print("🚀 Sistema en funcionamiento desde:", "2024")
        print("📧 Para soporte técnico, consulta la documentación")

    def pause(self):
        """Pausa la ejecución esperando input del usuario"""
        input("\n⏸️  Presiona Enter para continuar...")

    def run(self):
        """Ejecuta el menú principal del sistema"""
        print("🚀 Iniciando Sistema Académico...")
        print("📚 Cargando módulos...")

        try:
            while True:
                self.show_main_menu()
                option = self.get_input("🔍 Selecciona una opción: ", str)

                if option == "0":
                    print("\n" + "=" * 50)
                    print("👋 ¡Gracias por usar el Sistema Académico!")
                    print("🔐 Cerrando aplicación...")
                    print("=" * 50)
                    break

                elif option == "1":
                    print("\n🎓 Accediendo al módulo de Estudiantes...")
                    try:
                        self.student_menu.run()
                    except Exception as e:
                        print(f"❌ Error en el módulo de estudiantes: {e}")
                        self.pause()

                elif option == "2":
                    print("\n👨‍🏫 Accediendo al módulo de Profesores...")
                    try:
                        self.teacher_menu.run()
                    except Exception as e:
                        print(f"❌ Error en el módulo de profesores: {e}")
                        self.pause()

                elif option == "3":
                    self.show_general_statistics()
                    self.pause()

                elif option == "4":
                    self.show_system_info()
                    self.pause()

                else:
                    print("❌ Opción inválida. Por favor selecciona una opción del 0 al 4.")
                    self.pause()

        except KeyboardInterrupt:
            print("\n\n👋 Sistema interrumpido por el usuario")
            print("🔐 Cerrando aplicación...")
        except Exception as e:
            print(f"\n❌ Error inesperado en el sistema: {e}")
            print("🔐 Cerrando aplicación por seguridad...")


def main():
    """
    Función principal que inicia el sistema académico
    """
    try:
        # Crear e iniciar el sistema académico
        academic_system = AcademicSystemMenu()
        academic_system.run()

    except KeyboardInterrupt:
        print("\n👋 Sistema interrumpido por el usuario")
    except ImportError as e:
        print(f"❌ Error al importar módulos: {e}")
        print("💡 Asegúrate de que la estructura de carpetas esté correcta:")
        print("   - src/ui/menu.py (estudiantes)")
        print("   - src/ui/teacher_menu.py (profesores)")
    except Exception as e:
        print(f"❌ Error inesperado al iniciar el sistema: {e}")
        print("💡 Contacta al soporte técnico si el problema persiste")


if __name__ == "__main__":
    main()

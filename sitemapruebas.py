class ErrorAcademico(Exception):
    """Clase base para excepciones personalizadas."""
    pass

class MateriaNoEncontradaError(ErrorAcademico):
    pass

class EstudianteNoEncontradoError(ErrorAcademico):
    pass

class HorarioConflictError(ErrorAcademico):
    """Excepción para conflictos de horario."""
    pass

class CalificacionInvalidaError(ErrorAcademico):
    """Excepción para calificaciones fuera del rango permitido."""
    pass

class MateriaAsignadaError(ErrorAcademico):
    """Excepción cuando una materia ya está asignada a un profesor."""
    pass

class SalonNoDisponibleError(ErrorAcademico):
    """Excepción para conflictos de horarios en el salón."""
    pass

class ProfesorNoEncontradoError(ErrorAcademico):
    pass

class Estudiante:


    def __init__(self, id_estudiante, nombre, apellido):
        self.id_estudiante = id_estudiante
        self.nombre = nombre
        self.apellido = apellido
        self.materias = []
        self.calificaciones = {}

    def asignar_calificacion(self, id_materia, calificacion):
        if id_materia not in [m.id_materia for m in self.materias]:
            raise MateriaNoEncontradaError(f"La materia ID '{id_materia}' no está inscrita para este estudiante.")
        self.calificaciones[id_materia] = calificacion


    def promedio_calificaciones(self):
        if not self.calificaciones:
            return 0
        return sum(self.calificaciones.values()) / len(self.calificaciones)

    def __str__(self):
        materias_nombres = ', '.join([m.nombre for m in self.materias]) if self.materias else "Ninguna"
        return f"{self.id_estudiante} - {self.nombre} {self.apellido} (Materias: {materias_nombres})"
    
class GestionAcademica:
    def __init__(self):
        self.estudiantes = []
        self.profesores = []
        self.materias = []
        self.salones = []
        self._crear_datos_por_defecto()

    def asignar_salon_a_materia(self):
        materia = self.listar_materias()
        salon = self.listar_salones()
        try:
            materia.asignar_salon(salon)
            print(f"Salón '{salon.nombre}' asignado a la materia '{materia.nombre}'.")
        except SalonNoDisponibleError as e:
            print(f"Error: {e}")

    def _crear_datos_por_defecto(self):
        # Crear materias
        self.crear_materia("MAT001", "Matemáticas", 4)
        self.crear_materia("FIS001", "Física", 3)
        self.crear_materia("QUI001", "Química", 3)

        # Crear estudiantes
        self.crear_estudiante("EST001", "Juan", "Pérez")
        self.crear_estudiante("EST002", "Ana", "López")
        self.crear_estudiante("EST003", "Carlos", "Gómez")

        # Crear profesores
        self.crear_profesor("PRO001", "María", "García")
        self.crear_profesor("PRO002", "Luis", "Martínez")
        

        #Crear salones
        self.crear_salon("SAL001", "Aula 101", 30)
        self.crear_salon("SAL002", "Aula 102", 20)
        self.crear_salon("SAL003", "Laboratorio 201", 15)

    def crear_materia(self, id_materia, nombre, creditos):
        materia = Materia(id_materia, nombre, creditos)
        self.materias.append(materia)

    def crear_estudiante(self, id_estudiante, nombre, apellido):
        estudiante = Estudiante(id_estudiante, nombre, apellido)
        self.estudiantes.append(estudiante)

    def crear_profesor(self, id_profesor, nombre, apellido):
        profesor = Profesor(id_profesor, nombre, apellido)
        self.profesores.append(profesor)

    def crear_salon(self, id_salon, nombre, capacidad):
        salon = Salon(id_salon, nombre, capacidad)
        self.salones.append(salon)

    def eliminar_materia(self, id_materia):
        for materia in self.materias:
            if materia.id_materia == id_materia:
                self.materias.remove(materia)
                return f"Materia '{materia.nombre}' eliminada."
        raise MateriaNoEncontradaError(f"Materia ID '{id_materia}' no encontrada.")
    
    def eliminar_estudiante(self, id_estudiante):
        for estudiante in self.estudiantes:
            if estudiante.id_estudiante == id_estudiante:
                self.estudiantes.remove(estudiante)
                return f"Estudiante '{estudiante.nombre} {estudiante.apellido}' eliminado."
        raise EstudianteNoEncontradoError(f"Estudiante ID '{id_estudiante}' no encontrado.")
    
    def eliminar_profesor(self, id_profesor):
        for profesor in self.profesores:
            if profesor.id_profesor == id_profesor:
                self.profesores.remove(profesor)
                return f"Profesor '{profesor.nombre} {profesor.apellido}' eliminado."
        raise ProfesorNoEncontradoError(f"Profesor ID '{id_profesor}' no encontrado.")

    def asignar_horario_a_materia(self):
        materia = self.listar_materias()
        dia = input("Día de la semana: ")
        hora_inicio = input("Hora de inicio (HH:MM): ")
        hora_fin = input("Hora de fin (HH:MM): ")
        materia.asignar_horario(dia, hora_inicio, hora_fin)
        print(f"Horario asignado a la materia '{materia.nombre}': {materia.horario}")

    def inscribir_materia_a_estudiante(self):
        estudiante = self.listar_estudiantes()
        materia = self.listar_materias()
        try:
            materia.inscribir_estudiante(estudiante)
            print(f"Estudiante '{estudiante.nombre} {estudiante.apellido}' inscrito en materia '{materia.nombre}'.")
        except HorarioConflictError as e:
            print(f"Error: {e}")

    def asignar_calificacion(self):
        estudiante = self.listar_estudiantes()
        materia = self.listar_materias()
        try:
            calificacion = float(input(f"Ingrese la calificación (0-5) para '{materia.nombre}': "))
            materia.registrar_calificacion(estudiante.id_estudiante, calificacion)
            estudiante.asignar_calificacion(materia.id_materia, calificacion)
            print(f"Calificación {calificacion} asignada a '{estudiante.nombre} {estudiante.apellido}' en '{materia.nombre}'.")
        except CalificacionInvalidaError as e:
            print(f"Error: {e}")


    def asignar_materia_a_profesor(self):
        profesor = self.listar_profesores()
        materia = self.listar_materias()
        try:
            profesor.asignar_materia(materia)
            print(f"Materia '{materia.nombre}' asignada a profesor '{profesor.nombre} {profesor.apellido}'.")
        except MateriaAsignadaError as e:
            print(f"Error: {e}")

    def mostrar_horario_estudiante(self):
        estudiante = self.listar_estudiantes()
        print(f"Horario de {estudiante.nombre} {estudiante.apellido}:")
        for materia in estudiante.materias:
            print(f"- {materia.nombre}: {materia.horario}")

    def mostrar_horario_profesor(self):
        profesor = self.listar_profesores()
        print(f"Horario de {profesor.nombre} {profesor.apellido}:")
        for materia in profesor.materias:
            print(f"- {materia.nombre}: {materia.horario}")

    def reportes_globales(self):
        print("\nReporte Global de Materias:")
        for materia in self.materias:
            print(f"- {materia.nombre}: Estudiantes Inscritos: {len(materia.estudiantes_inscritos)}, "
                  f"Promedio de Calificaciones: {materia.promedio_calificaciones():.2f}")

        print("\nReporte Global de Estudiantes:")
        for estudiante in self.estudiantes:
            promedio = estudiante.promedio_calificaciones()
            estado = "Aprobado" if promedio >= 3 else "Reprobado"
            print(f"- {estudiante.nombre} {estudiante.apellido}: Promedio: {promedio:.2f}, Estado: {estado}")

    def listar_estudiantes(self):
        for idx, estudiante in enumerate(self.estudiantes, start=1):
            print(f"{idx}. {estudiante}")
        seleccion = int(input("Seleccione un estudiante: ")) - 1
        if seleccion < 0 or seleccion >= len(self.estudiantes):
            raise IndexError("Selección inválida.")
        return self.estudiantes[seleccion]

    def listar_materias(self):
        for idx, materia in enumerate(self.materias, start=1):
            print(f"{idx}. {materia}")
        seleccion = int(input("Seleccione una materia: ")) - 1
        if seleccion < 0 or seleccion >= len(self.materias):
            raise IndexError("Selección inválida.")
        return self.materias[seleccion]

    def listar_profesores(self):
        for idx, profesor in enumerate(self.profesores, start=1):
            print(f"{idx}. {profesor}")
        seleccion = int(input("Seleccione un profesor: ")) - 1
        if seleccion < 0 or seleccion >= len(self.profesores):
            raise IndexError("Selección inválida.")
        return self.profesores[seleccion]
    
    def listar_salones(self):
        for idx, salon in enumerate(self.salones, start=1):
            print(f"{idx}. {salon}")
        seleccion = int(input("Seleccione un salón: ")) - 1
        if seleccion < 0 or seleccion >= len(self.salones):
            raise IndexError("Selección inválida.")
        return self.salones[seleccion]    

class Materia:
    def __init__(self, id_materia, nombre, creditos):
        self.id_materia = id_materia
        self.nombre = nombre
        self.creditos = creditos
        self.estudiantes_inscritos = []
        self.calificaciones = {}
        self.horario = None
        self.profesor = None
        self.salon = None
        self.cupos = None

    def asignar_horario(self, dia, hora_inicio, hora_fin):
        self.horario = Horario(dia, hora_inicio, hora_fin)

    def asignar_salon(self, salon):
        """Asigna un salón a la materia, verificando conflictos de horario."""
        if not self.horario:
            raise ValueError(f"La materia '{self.nombre}' no tiene horario asignado.")
        salon.asignar_horario(self.horario)
        self.salon = salon
        self.cupos = salon.capacidad - len(self.estudiantes_inscritos)

    def inscribir_estudiante(self, estudiante):
        if self.salon and self.cupos ==0 :
            raise ValueError(f"La materia '{self.nombre}' no tiene mas cupos.")
        for materia in estudiante.materias:
            if materia.horario and self.horario and self.horario.hay_conflicto(materia.horario):
                raise HorarioConflictError(
                    f"Conflicto de horario entre '{self.nombre}' y '{materia.nombre}' en el día {self.horario.dia}."
                )
        self.estudiantes_inscritos.append(estudiante)
        self.cupos -= 1 
        estudiante.materias.append(self)

    def asignar_profesor(self, profesor):
        if self.profesor:
            raise MateriaAsignadaError(f"La materia '{self.nombre}' ya tiene un profesor asignado.")
        self.profesor = profesor
        profesor.materias.append(self)

    def registrar_calificacion(self, id_estudiante, calificacion):
        if not (0 <= calificacion <= 5):
            raise CalificacionInvalidaError("La calificación debe estar entre 0 y 5.")
        self.calificaciones[id_estudiante] = calificacion

    def promedio_calificaciones(self):
        if not self.calificaciones:
            return 0
        return sum(self.calificaciones.values()) / len(self.calificaciones)

    def __str__(self):
        horario_str = str(self.horario) if self.horario else "Sin horario asignado"
        profesor_str = f"Profesor: {self.profesor.nombre} {self.profesor.apellido}" if self.profesor else "Sin profesor asignado"
        salon_str = f"Salón: {self.salon.nombre}" if self.salon else "Sin salón asignado"
        cupos_str = f"Cupos: {self.cupos}" if self.cupos is not None else "Sin cupos asignados"
        return f"{self.id_materia} - {self.nombre} (Créditos: {self.creditos},{cupos_str}, {profesor_str}, {horario_str}, {salon_str})"

class Profesor:
    def __init__(self, id_profesor, nombre, apellido):
        self.id_profesor = id_profesor
        self.nombre = nombre
        self.apellido = apellido
        self.materias = []

    def asignar_materia(self, materia):
        self.materias.append(materia)
        materia.asignar_profesor(self)

    def promedio_calificaciones(self):
        calificaciones = []
        for materia in self.materias:
            calificaciones.extend(materia.calificaciones.values())
        if not calificaciones:
            return 0
        return sum(calificaciones) / len(calificaciones)

    def __str__(self):
        materias_nombres = ', '.join([m.nombre for m in self.materias])
        return f"{self.id_profesor} - {self.nombre} {self.apellido} (Materias: {materias_nombres})"

class Horario:
    def __init__(self, dia, hora_inicio, hora_fin):
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def __str__(self):
        return f"{self.dia} de {self.hora_inicio} a {self.hora_fin}"

    def hay_conflicto(self, otro_horario):
        """Verifica si hay un conflicto de horario con otro horario."""
        return (
            self.dia == otro_horario.dia and
            not (self.hora_fin <= otro_horario.hora_inicio or self.hora_inicio >= otro_horario.hora_fin)
        )

class Salon:
    def __init__(self, id_salon, nombre, capacidad):
        self.id_salon = id_salon
        self.nombre = nombre
        self.capacidad = capacidad
        self.horarios_ocupados = []

    def asignar_horario(self, horario):
        """Asigna un horario al salón si no hay conflictos."""
        for horario_existente in self.horarios_ocupados:
            if horario.hay_conflicto(horario_existente):
                raise SalonNoDisponibleError(
                    f"El salón '{self.nombre}' ya está ocupado el {horario.dia} de {horario.hora_inicio} a {horario.hora_fin}."
                )
        self.horarios_ocupados.append(horario)

    def __str__(self):
        return f"Salón {self.id_salon} - {self.nombre} (Capacidad: {self.capacidad})"

def menu():
    gestion = GestionAcademica()

    while True:
        try:
            print("\n==================================================")
            print("Gestión Académica")
            print("1. Listar Estudiantes, Profesores, Materias y Salones")
            print("2. Crear Materia")
            print("3. Crear Estudiante")
            print("4. Crear Profesor")
            print("5. Crear Salón")
            print("6. Asignar Horario a Materia")
            print("7. Asignar Salón a Materia")
            print("8. Inscribir Materia a Estudiante")
            print("9. Asignar Calificación")
            print("10. Cancelar Materia")
            print("11. Asignar Materia a Profesor")
            print("12. Mostrar Horario de Estudiante")
            print("13. Mostrar Horario de Profesor")
            print("14. Reportes Globales")
            print("0. Salir")

            opcion = input("Seleccione una opción: ")
            print("==================================================")
            print("\nSalida del sistema: ")

            if opcion == "1":
                print("\nEstudiantes:")
                for estudiante in gestion.estudiantes:
                    print(estudiante)
                print("\nProfesores:")
                for profesor in gestion.profesores:
                    print(profesor)
                print("\nMaterias:")
                for materia in gestion.materias:
                    print(materia)
                print("\nSalones:")
                for salon in gestion.salones:
                    print(salon)

            elif opcion == "2":
                id_materia = input("ID de la Materia: ")
                nombre = input("Nombre de la Materia: ")
                creditos = int(input("Créditos de la Materia: "))
                gestion.crear_materia(id_materia, nombre, creditos)

            elif opcion == "3":
                id_estudiante = input("ID del Estudiante: ")
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                gestion.crear_estudiante(id_estudiante, nombre, apellido)

            elif opcion == "4":
                id_profesor = input("ID del Profesor: ")
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                gestion.crear_profesor(id_profesor, nombre, apellido)

            elif opcion == "5":
                id_salon = input("ID del Salón: ")
                nombre = input("Nombre del Salón: ")
                capacidad = int(input("Capacidad del Salón: "))
                gestion.crear_salon(id_salon, nombre, capacidad)

            elif opcion == "6":
                gestion.asignar_horario_a_materia()

            elif opcion == "7":
                gestion.asignar_salon_a_materia()

            elif opcion == "8":
                gestion.inscribir_materia_a_estudiante()

            elif opcion == "9":
                gestion.asignar_calificacion()

            elif opcion == "10":
                gestion.cancelar_materia()

            elif opcion == "11":
                gestion.asignar_materia_a_profesor()

            elif opcion == "12":
                gestion.mostrar_horario_estudiante()

            elif opcion == "13":
                gestion.mostrar_horario_profesor()

            elif opcion == "14":
                gestion.reportes_globales()

            elif opcion == "0":
                print("Saliendo del sistema.")
                break

            else:
                print("Opción no válida, intente de nuevo.")

        except ErrorAcademico as e:
            print(f"Error: {e}")
        except IndexError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error de Valor: {e}")
        except Exception as e:
            print(f"Error Inesperado: {e}")


if __name__ == "__main__":
    menu()

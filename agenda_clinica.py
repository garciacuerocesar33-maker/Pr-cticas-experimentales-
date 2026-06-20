"""
Agenda de Turnos de Pacientes de una Clínica
Guía de Práctica #01 - Estructura de Datos
Universidad Estatal Amazónica
Autor: [Nombre del Estudiante]
Período Académico: 2026-2026
"""

from datetime import datetime


# =============================================
# ESTRUCTURAS DE DATOS (usando listas/vectores)
# =============================================

class Paciente:
    """Clase que representa a un paciente de la clínica."""

    def __init__(self, cedula: str, nombre: str, apellido: str,
                 telefono: str, fecha_nacimiento: str):
        self.cedula = cedula
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento  # formato: DD/MM/AAAA

    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    def __str__(self) -> str:
        return (f"Cédula: {self.cedula} | Nombre: {self.nombre_completo()} | "
                f"Tel: {self.telefono} | Nac: {self.fecha_nacimiento}")


class Turno:
    """Clase que representa un turno médico asignado."""

    ESTADOS = ["Pendiente", "Confirmado", "Cancelado", "Atendido"]

    def __init__(self, id_turno: int, cedula_paciente: str,
                 medico: str, especialidad: str,
                 fecha: str, hora: str):
        self.id_turno = id_turno
        self.cedula_paciente = cedula_paciente
        self.medico = medico
        self.especialidad = especialidad
        self.fecha = fecha          # formato: DD/MM/AAAA
        self.hora = hora            # formato: HH:MM
        self.estado = "Pendiente"

    def __str__(self) -> str:
        return (f"ID: {self.id_turno:03d} | Paciente: {self.cedula_paciente} | "
                f"Dr. {self.medico} ({self.especialidad}) | "
                f"{self.fecha} {self.hora} | Estado: {self.estado}")


class AgendaClinica:
    """
    Clase principal que gestiona la agenda de la clínica.
    Emplea:
      - Vector (lista) de Pacientes
      - Vector (lista) de Turnos
      - Matriz para el resumen diario de turnos por médico
    """

    def __init__(self, nombre_clinica: str):
        self.nombre_clinica = nombre_clinica
        self.pacientes: list[Paciente] = []      # Vector de pacientes
        self.turnos: list[Turno] = []            # Vector de turnos
        self._contador_turnos: int = 1

    # ------------------------------------------
    # MÉTODOS DE PACIENTES
    # ------------------------------------------

    def registrar_paciente(self, cedula: str, nombre: str, apellido: str,
                           telefono: str, fecha_nacimiento: str) -> bool:
        """Registra un nuevo paciente. Retorna False si la cédula ya existe."""
        if self.buscar_paciente_por_cedula(cedula):
            print(f"  [!] Paciente con cédula {cedula} ya está registrado.")
            return False
        p = Paciente(cedula, nombre, apellido, telefono, fecha_nacimiento)
        self.pacientes.append(p)
        print(f"  [OK] Paciente '{p.nombre_completo()}' registrado exitosamente.")
        return True

    def buscar_paciente_por_cedula(self, cedula: str) -> Paciente | None:
        """Búsqueda lineal en el vector de pacientes."""
        for p in self.pacientes:
            if p.cedula == cedula:
                return p
        return None

    def buscar_pacientes_por_nombre(self, nombre: str) -> list[Paciente]:
        """Filtra pacientes cuyo nombre o apellido contiene la cadena dada."""
        nombre_lower = nombre.lower()
        return [p for p in self.pacientes
                if nombre_lower in p.nombre.lower() or nombre_lower in p.apellido.lower()]

    def listar_pacientes(self) -> None:
        """Muestra todos los pacientes registrados."""
        print(f"\n{'='*70}")
        print(f"  PACIENTES REGISTRADOS — {self.nombre_clinica}")
        print(f"{'='*70}")
        if not self.pacientes:
            print("  Sin pacientes registrados.")
        else:
            for i, p in enumerate(self.pacientes, 1):
                print(f"  {i:02d}. {p}")
        print(f"{'='*70}\n")

    # ------------------------------------------
    # MÉTODOS DE TURNOS
    # ------------------------------------------

    def agendar_turno(self, cedula_paciente: str, medico: str,
                      especialidad: str, fecha: str, hora: str) -> bool:
        """Agenda un turno para un paciente existente."""
        paciente = self.buscar_paciente_por_cedula(cedula_paciente)
        if not paciente:
            print(f"  [!] No existe paciente con cédula {cedula_paciente}.")
            return False

        # Verificar conflicto de horario para el mismo médico
        for t in self.turnos:
            if (t.medico == medico and t.fecha == fecha
                    and t.hora == hora and t.estado != "Cancelado"):
                print(f"  [!] El Dr. {medico} ya tiene turno el {fecha} a las {hora}.")
                return False

        turno = Turno(self._contador_turnos, cedula_paciente,
                      medico, especialidad, fecha, hora)
        self.turnos.append(turno)
        self._contador_turnos += 1
        print(f"  [OK] Turno #{turno.id_turno:03d} agendado para "
              f"'{paciente.nombre_completo()}' con Dr. {medico} el {fecha} a las {hora}.")
        return True

    def cambiar_estado_turno(self, id_turno: int, nuevo_estado: str) -> bool:
        """Actualiza el estado de un turno existente."""
        if nuevo_estado not in Turno.ESTADOS:
            print(f"  [!] Estado inválido. Opciones: {Turno.ESTADOS}")
            return False
        turno = self._buscar_turno(id_turno)
        if not turno:
            print(f"  [!] No existe turno con ID {id_turno}.")
            return False
        turno.estado = nuevo_estado
        print(f"  [OK] Turno #{id_turno:03d} actualizado a estado '{nuevo_estado}'.")
        return True

    def _buscar_turno(self, id_turno: int) -> Turno | None:
        for t in self.turnos:
            if t.id_turno == id_turno:
                return t
        return None

    def listar_turnos(self, solo_estado: str = None) -> None:
        """Lista todos los turnos o filtra por estado."""
        titulo = f"TURNOS — {self.nombre_clinica}"
        if solo_estado:
            titulo += f" (Estado: {solo_estado})"
        print(f"\n{'='*70}")
        print(f"  {titulo}")
        print(f"{'='*70}")
        turnos_filtrados = (
            [t for t in self.turnos if t.estado == solo_estado]
            if solo_estado else self.turnos
        )
        if not turnos_filtrados:
            print("  Sin turnos en esta categoría.")
        else:
            for t in turnos_filtrados:
                paciente = self.buscar_paciente_por_cedula(t.cedula_paciente)
                nombre_pac = paciente.nombre_completo() if paciente else "N/A"
                print(f"  {t}  | Nombre: {nombre_pac}")
        print(f"{'='*70}\n")

    def buscar_turnos_por_paciente(self, cedula: str) -> None:
        """Muestra los turnos asociados a un paciente."""
        paciente = self.buscar_paciente_por_cedula(cedula)
        if not paciente:
            print(f"  [!] Paciente con cédula {cedula} no encontrado.")
            return
        turnos_pac = [t for t in self.turnos if t.cedula_paciente == cedula]
        print(f"\n  Turnos de: {paciente.nombre_completo()} (C.I.: {cedula})")
        print(f"  {'─'*60}")
        if not turnos_pac:
            print("  Sin turnos registrados.")
        else:
            for t in turnos_pac:
                print(f"  {t}")

    # ------------------------------------------
    # REPORTERÍA CON MATRIZ
    # ------------------------------------------

    def reporte_turnos_por_medico(self) -> None:
        """
        Genera una MATRIZ (lista de listas) donde:
          - Filas = médicos únicos
          - Columnas = conteos por estado
        """
        medicos_unicos: list[str] = []
        for t in self.turnos:
            if t.medico not in medicos_unicos:
                medicos_unicos.append(t.medico)

        estados = Turno.ESTADOS  # ["Pendiente","Confirmado","Cancelado","Atendido"]
        n_medicos = len(medicos_unicos)
        n_estados = len(estados)

        # Inicializar matriz n_medicos × n_estados con ceros
        matriz: list[list[int]] = [[0] * n_estados for _ in range(n_medicos)]

        # Poblar la matriz contando turnos
        for t in self.turnos:
            fila = medicos_unicos.index(t.medico)
            col = estados.index(t.estado)
            matriz[fila][col] += 1

        # Imprimir reporte tabular
        print(f"\n{'='*70}")
        print(f"  REPORTE MATRICIAL — TURNOS POR MÉDICO Y ESTADO")
        print(f"{'='*70}")
        col_w = 12
        med_w = 22
        encabezado = f"  {'Médico':<{med_w}}" + "".join(f"{e:^{col_w}}" for e in estados) + f"{'TOTAL':^{col_w}}"
        print(encabezado)
        print(f"  {'─'*60}")
        for i, medico in enumerate(medicos_unicos):
            fila = matriz[i]
            total = sum(fila)
            linea = f"  {medico:<{med_w}}" + "".join(f"{v:^{col_w}}" for v in fila) + f"{total:^{col_w}}"
            print(linea)
        print(f"{'='*70}\n")

    def estadisticas_generales(self) -> None:
        """Muestra un resumen estadístico del sistema."""
        total_turnos = len(self.turnos)
        conteo = {e: 0 for e in Turno.ESTADOS}
        for t in self.turnos:
            conteo[t.estado] += 1

        print(f"\n  ── ESTADÍSTICAS GENERALES ──")
        print(f"  Total de pacientes : {len(self.pacientes)}")
        print(f"  Total de turnos    : {total_turnos}")
        for estado, cant in conteo.items():
            pct = (cant / total_turnos * 100) if total_turnos else 0
            print(f"    {estado:<12}: {cant:>3} ({pct:5.1f}%)")


# =============================================
# FUNCIÓN PRINCIPAL — DEMOSTRACIÓN DEL SISTEMA
# =============================================

def separador(titulo: str = "") -> None:
    print(f"\n{'━'*70}")
    if titulo:
        print(f"  >>> {titulo}")
    print(f"{'━'*70}")


def main():
    print("\n" + "="*70)
    print("   SISTEMA DE AGENDA DE TURNOS — CLÍNICA AMAZÓNICA")
    print("   Guía de Práctica #01 | Estructura de Datos | UEA")
    print("="*70)

    clinica = AgendaClinica("Clínica Amazónica")

    # ── 1. REGISTRO DE PACIENTES (Vector) ──────────────────────────────────
    separador("REGISTRO DE PACIENTES")
    clinica.registrar_paciente("1722334455", "María",   "Pérez",    "0991234567", "15/03/1990")
    clinica.registrar_paciente("0987654321", "Juan",    "Quispe",   "0976543210", "22/07/1985")
    clinica.registrar_paciente("1312345678", "Sofía",   "Andrade",  "0965432109", "08/11/2000")
    clinica.registrar_paciente("0512345678", "Carlos",  "Morales",  "0954321098", "30/01/1978")
    clinica.registrar_paciente("1722334455", "María",   "Pérez",    "0991234567", "15/03/1990")  # duplicado

    # ── 2. LISTADO DE PACIENTES ─────────────────────────────────────────────
    clinica.listar_pacientes()

    # ── 3. AGENDAMIENTO DE TURNOS (Vector + validación) ────────────────────
    separador("AGENDAMIENTO DE TURNOS")
    clinica.agendar_turno("1722334455", "García",   "Medicina General", "20/06/2026", "09:00")
    clinica.agendar_turno("0987654321", "García",   "Medicina General", "20/06/2026", "09:30")
    clinica.agendar_turno("1312345678", "Torres",   "Pediatría",        "20/06/2026", "10:00")
    clinica.agendar_turno("0512345678", "Torres",   "Pediatría",        "21/06/2026", "08:00")
    clinica.agendar_turno("1722334455", "Ramírez",  "Cardiología",      "22/06/2026", "11:00")
    clinica.agendar_turno("0987654321", "García",   "Medicina General", "20/06/2026", "09:30")  # conflicto
    clinica.agendar_turno("9999999999", "García",   "Medicina General", "23/06/2026", "08:00")  # paciente inexistente

    # ── 4. CAMBIO DE ESTADOS ────────────────────────────────────────────────
    separador("ACTUALIZACIÓN DE ESTADOS")
    clinica.cambiar_estado_turno(1, "Confirmado")
    clinica.cambiar_estado_turno(2, "Atendido")
    clinica.cambiar_estado_turno(3, "Cancelado")
    clinica.cambiar_estado_turno(99, "Confirmado")  # inexistente

    # ── 5. LISTADO GENERAL DE TURNOS ────────────────────────────────────────
    clinica.listar_turnos()

    # ── 6. BÚSQUEDA POR PACIENTE ────────────────────────────────────────────
    separador("BÚSQUEDA DE TURNOS POR PACIENTE")
    clinica.buscar_turnos_por_paciente("1722334455")

    # ── 7. FILTRO POR ESTADO ────────────────────────────────────────────────
    separador("TURNOS PENDIENTES")
    clinica.listar_turnos(solo_estado="Pendiente")

    # ── 8. BÚSQUEDA DE PACIENTE POR NOMBRE ─────────────────────────────────
    separador("BÚSQUEDA DE PACIENTES POR NOMBRE")
    resultados = clinica.buscar_pacientes_por_nombre("ar")
    print(f"  Resultados para 'ar': {len(resultados)} encontrado(s)")
    for p in resultados:
        print(f"    → {p}")

    # ── 9. REPORTE MATRICIAL ────────────────────────────────────────────────
    separador("REPORTE MATRICIAL (Estructura: Matriz 2D)")
    clinica.reporte_turnos_por_medico()

    # ── 10. ESTADÍSTICAS ────────────────────────────────────────────────────
    separador("ESTADÍSTICAS GENERALES")
    clinica.estadisticas_generales()

    print(f"\n{'='*70}")
    print("  Sistema ejecutado correctamente.")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()

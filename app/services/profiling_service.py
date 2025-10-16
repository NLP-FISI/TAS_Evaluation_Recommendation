"""
Servicio para el manejo de perfilamiento de usuarios (versión simplificada sin DB).
"""
from app.schemas.profiling_schemas import ProfilingRequest, ProfilingResponse


class ProfilingService:
    @staticmethod
    def create_profile(data: ProfilingRequest) -> ProfilingResponse:
        """
        Lógica de negocio para crear el perfil inicial de un estudiante.
        Versión simplificada que simula el guardado sin base de datos.
        """
        
        # Validaciones básicas
        if not (2 <= data.grade_level <= 6):
            return ProfilingResponse(
                student_id=data.student_id,
                profile_created=False,
                message="Error: El grado debe estar entre 2do y 6to."
            )
        
        if len(data.preferences) == 0:
            return ProfilingResponse(
                student_id=data.student_id,
                profile_created=False,
                message="Error: Debe seleccionar al menos una preferencia."
            )
        
        # Simulación de guardado exitoso
        print(f"Perfil recibido para el estudiante: {data.student_id}")
        print(f"Grado: {data.grade_level}")
        print(f"Preferencias: {data.preferences}")
        print(f"Avatar: {data.avatar.dict() if data.avatar else 'No configurado'}")
        
        # Simulación de una operación exitosa
        return ProfilingResponse(
            student_id=data.student_id,
            profile_created=True,
            message="Perfil de usuario creado exitosamente (simulado)."
        )


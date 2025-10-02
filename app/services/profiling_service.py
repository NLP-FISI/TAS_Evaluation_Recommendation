"""
Servicio para el manejo de perfilamiento de usuarios.
"""
from app.schemas.profiling_schemas import ProfilingRequest, ProfilingResponse


class ProfilingService:
    @staticmethod
    def create_profile(data: ProfilingRequest) -> ProfilingResponse:
        """
        Lógica de negocio para crear el perfil inicial de un estudiante.
        Aquí se conectarían con la base de datos para guardar la información.
        """
        
        # --- Lógica de Base de Datos (Simulada) ---
        # En un caso real, aquí guardarías los datos en la base de datos.
        # Por ejemplo:
        # user_profile = ProfileModel(
        #     student_id=data.student_id,
        #     grade_level=data.grade_level,
        #     preferences=data.preferences,
        #     avatar_config=data.avatar.dict()
        # )
        # db.add(user_profile)
        # db.commit()
        
        print(f"Perfil recibido para el estudiante: {data.student_id}")
        print(f"Grado: {data.grade_level}")
        print(f"Preferencias: {data.preferences}")
        print(f"Avatar: {data.avatar.dict()}")
        
        # Simulación de una operación exitosa
        profile_saved_successfully = True

        if profile_saved_successfully:
            return ProfilingResponse(
                student_id=data.student_id,
                profile_created=True,
                message="Perfil de usuario creado exitosamente."
            )
        else:
            # En caso de error en la base de datos
            return ProfilingResponse(
                student_id=data.student_id,
                profile_created=False,
                message="Error al crear el perfil de usuario."
            )
"""
Servicio para el manejo de perfilamiento de usuarios.
"""
# Importamos los modelos de Pydantic y SQLAlchemy
from app.schemas.profiling_schemas import ProfilingRequest, ProfilingResponse
from app.models.user_profile import Usuario, Tematica, Grado
# File: app/services/profiling_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status




class ProfilingService:

    @staticmethod
    def create_user_profile(db: Session, data: ProfilingRequest) -> ProfilingResponse:
        """
        Lógica de negocio para crear o actualizar el perfil de un estudiante.
        Ahora se conecta y guarda la información en la base de datos.
        """
        # 1. Buscar si el usuario ya existe. Si no, crea uno nuevo.
        #    (Asumimos que student_id es un identificador único, como 'nombre_usuario')
        db_user = db.query(Usuario).filter(Usuario.nombre_usuario == data.student_id).first()

        if not db_user:
            db_user = Usuario(nombre_usuario=data.student_id)
            # Aquí podrías añadir otros campos por defecto si los tuvieras
            db.add(db_user)
            # Hacemos un "pre-commit" para que el usuario exista antes de añadir relaciones
            db.flush() 

        # 2. Buscar las temáticas (preferencias) en la base de datos
        db_tematicas = db.query(Tematica).filter(Tematica.nombre_tematica.in_(data.preferences)).all()
        
        # Validación: Asegurarse de que todas las preferencias enviadas existen en la BD
        if len(db_tematicas) != len(data.preferences):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Una o más preferencias no se encontraron en la base de datos."
            )

        # 3. Asignar las preferencias al usuario
        db_user.preferencias = db_tematicas

        # 4. Asignar el grado
        db_grado = db.query(Grado).filter(Grado.id_grado == data.grade_level).first()
        if not db_grado:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El grado con id {data.grade_level} no fue encontrado."
            )
        db_user.id_grado = db_grado.id_grado


        # 5. Guardar la configuración del avatar (convirtiendo el modelo Pydantic a un dict)
        db_user.configuracion_avatar = data.avatar.dict()

        # 6. Confirmar todos los cambios en la base de datos
        db.commit()
        db.refresh(db_user)

        # 7. Devolver una respuesta exitosa
        return ProfilingResponse(
            student_id=db_user.nombre_usuario,
            message=f"Perfil para {db_user.nombre_usuario} ha sido creado/actualizado exitosamente."
        )


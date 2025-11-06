"""
Servicio para el manejo de perfilamiento de usuarios.
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.schemas.profiling_schemas import ProfilingRequest, ProfilingResponse
from app.models.usuario import Usuario
from app.models.grado import Grado
from app.models.tematica import Tematica


class ProfilingService:
    @staticmethod
    def create_profile(data: ProfilingRequest, db: Session) -> ProfilingResponse:
        """
        Lógica de negocio para crear el perfil inicial de un estudiante.
        Se conecta a la base de datos PostgreSQL para guardar la información.
        """
        
        try:
            # 1. Verificar que el grado escolar existe (o crearlo si no existe)
            db_grade = db.query(Grado).filter(Grado.id_grado == data.grade_level).first()
            if not db_grade:
                # Crear el grado si no existe
                db_grade = Grado(id_grado=data.grade_level, nombre_grado=f"Grado {data.grade_level}")
                db.add(db_grade)
                db.flush()
            
            # 2. Verificar que las temáticas existen por ID
            db_preferences = []
            for tematica_id in data.preferences:
                db_pref = db.query(Tematica).filter(Tematica.id_tematica == tematica_id).first()
                if not db_pref:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Temática con ID {tematica_id} no encontrada. Las temáticas deben existir previamente en la base de datos."
                    )
                db_preferences.append(db_pref)
            
            # 3. Buscar o crear el usuario por student_id (string)
            db_user = db.query(Usuario).filter(Usuario.student_id == data.student_id).first()
            if db_user:
                # Actualizar usuario existente
                db_user.id_grado = db_grade.id_grado
                db_user.preferencias = db_preferences
                message = "Perfil de usuario actualizado exitosamente."
            else:
                # Crear nuevo usuario
                db_user = Usuario(
                    student_id=data.student_id,  # Usar student_id como string
                    nombre_usuario=f"Usuario_{data.student_id}",
                    apellido_usuario=f"Apellido_{data.student_id}",  # Agregar apellido requerido
                    contrasena=f"password_{data.student_id}",  # Contraseña por defecto requerida
                    email=f"user_{data.student_id}@example.com",
                    id_grado=db_grade.id_grado
                )
                db_user.preferencias = db_preferences
                db.add(db_user)
                message = "Perfil de usuario creado exitosamente."
            
            # 4. Confirmar cambios
            db.commit()
            db.refresh(db_user)
            
            return ProfilingResponse(
                student_id=data.student_id,
                profile_created=True,
                message=message
            )
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al conectar con la base de datos: {str(e)}"
            )


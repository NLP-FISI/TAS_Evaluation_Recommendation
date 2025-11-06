from app.models.usuario import Usuario


class RecommendationInputService:
    """
    Servicio que genera textos de prueba de entrada (fase 1 y fase 2)
    de forma temporal (hardcodeado).
    """

    @staticmethod
    def get_input_texts(id_usuario: int, db):
        # Buscar usuario
        usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
        if not usuario:
            return {"mensaje": "Usuario no encontrado"}

        # Obtener datos relevantes
        edad = usuario.edad
        grado = usuario.grado.nombre_grado if usuario.grado else "Sin grado"
        preferencias = [t.nombre_tematica for t in usuario.preferencias] if usuario.preferencias else ["General"]

        # Generar textos hardcodeados
        fase_1 = {
            "fase": "Fase 1",
            "descripcion": "Preguntas literal e inferencial básica",
            "textos_obtenidos": 1,
            "textos": [
                {
                    "id_texto": 66,
                    "titulo": "La gran aventura de Carlos en el bosque",
                    "contenido": (
                        "Carlos vive en un pueblo cerca de la selva. Un día, su abuelo le dijo: "
                        "'Carlos, vamos a explorar'. Carlos llevó su mochila y una linterna. "
                        "Caminaron mucho. De pronto, vieron un río. '¿Cómo pasamos?', preguntó Carlos. "
                        "'Con cuidado', dijo el abuelo. Cruzaron unas piedras. En el bosque, encontraron un pájaro herido. "
                        "'Lo ayudaremos', dijo Carlos. Lo llevaron a casa. El pájaro mejoró. ¡Estaban felices!"
                    ),
                    "preguntas": [
                        {
                            "id_pregunta": 305,
                            "contenido": "¿Qué llevó Carlos al bosque?",
                            "id_dificultad": 1,
                            "id_tipo_pregunta": 1,
                            "alternativas": [
                                {"id_alternativa": 1189, "contenido": "Una mochila y una linterna"},
                                {"id_alternativa": 1190, "contenido": "Un paraguas"},
                                {"id_alternativa": 1191, "contenido": "Un balde"},
                                {"id_alternativa": 1192, "contenido": "Un juguete"}
                            ]
                        },
                        {
                            "id_pregunta": 306,
                            "contenido": "¿Qué encontraron en el bosque?",
                            "id_dificultad": 2,
                            "id_tipo_pregunta": 2,
                            "alternativas": [
                                {"id_alternativa": 1193, "contenido": "Un pájaro herido"},
                                {"id_alternativa": 1194, "contenido": "Una flor grande"},
                                {"id_alternativa": 1195, "contenido": "Una piedra brillante"},
                                {"id_alternativa": 1196, "contenido": "Un río seco"}
                            ]
                        },
                        {
                            "id_pregunta": 307,
                            "contenido": "¿Por qué Carlos y su abuelo ayudaron al pájaro?",
                            "id_dificultad": 3,
                            "id_tipo_pregunta": 3,
                            "alternativas": [
                                {"id_alternativa": 1197, "contenido": "Porque querían cuidarlo"},
                                {"id_alternativa": 1198, "contenido": "Porque el pájaro les dio comida"},
                                {"id_alternativa": 1199, "contenido": "Porque era un pájaro mágico"},
                                {"id_alternativa": 1200, "contenido": "Porque el pájaro les cantó"}
                            ]
                        },
                        {
                            "id_pregunta": 308,
                            "contenido": "¿Cómo cruzaron el río?",
                            "id_dificultad": 4,
                            "id_tipo_pregunta": 1,
                            "alternativas": [
                                {"id_alternativa": 1201, "contenido": "Con cuidado, usando piedras"},
                                {"id_alternativa": 1202, "contenido": "Nadando rápido"},
                                {"id_alternativa": 1203, "contenido": "Con un puente de madera"},
                                {"id_alternativa": 1204, "contenido": "Saltando desde la orilla"}
                            ]
                        },
                        {
                            "id_pregunta": 309,
                            "contenido": "¿Qué sintió Carlos al final de la aventura?",
                            "id_dificultad": 5,
                            "id_tipo_pregunta": 2,
                            "alternativas": [
                                {"id_alternativa": 1205, "contenido": "Feliz"},
                                {"id_alternativa": 1206, "contenido": "Cansado"},
                                {"id_alternativa": 1207, "contenido": "Enojado"},
                                {"id_alternativa": 1208, "contenido": "Asustado"}
                            ]
                        }
                    ]
                }
            ]
        }

        fase_2 = {
            "fase": "Fase 2",
            "descripcion": "Preguntas literal, inferencial intermedio y crítica",
            "textos_obtenidos": 1,
            "textos": [
                {
                    "id_texto": 67,
                    "titulo": "El nuevo parque del barrio",
                    "contenido": (
                        "El alcalde inauguró un nuevo parque en el barrio. Los niños estaban emocionados. "
                        "Tenía juegos, áreas verdes y una fuente. Sin embargo, algunos vecinos pensaron que "
                        "debieron plantar más árboles. Al final, todos acordaron cuidarlo entre todos."
                    ),
                    "preguntas": [
                        {
                            "id_pregunta": 401,
                            "contenido": "¿Qué inauguró el alcalde?",
                            "id_dificultad": 1,
                            "id_tipo_pregunta": 1,
                            "alternativas": [
                                {"id_alternativa": 1301, "contenido": "Un parque"},
                                {"id_alternativa": 1302, "contenido": "Una escuela"},
                                {"id_alternativa": 1303, "contenido": "Una calle"},
                                {"id_alternativa": 1304, "contenido": "Una biblioteca"}
                            ]
                        },
                        {
                            "id_pregunta": 402,
                            "contenido": "¿Por qué algunos vecinos no estaban totalmente contentos?",
                            "id_dificultad": 2,
                            "id_tipo_pregunta": 2,
                            "alternativas": [
                                {"id_alternativa": 1305, "contenido": "Porque querían más árboles"},
                                {"id_alternativa": 1306, "contenido": "Porque no había juegos"},
                                {"id_alternativa": 1307, "contenido": "Porque el parque era pequeño"},
                                {"id_alternativa": 1308, "contenido": "Porque no asistieron"}
                            ]
                        },
                        {
                            "id_pregunta": 403,
                            "contenido": "¿Qué enseña este texto sobre la convivencia vecinal?",
                            "id_dificultad": 3,
                            "id_tipo_pregunta": 3,
                            "alternativas": [
                                {"id_alternativa": 1309, "contenido": "Que todos deben colaborar"},
                                {"id_alternativa": 1310, "contenido": "Que los niños deben jugar solos"},
                                {"id_alternativa": 1311, "contenido": "Que el alcalde decide todo"},
                                {"id_alternativa": 1312, "contenido": "Que el parque no sirve"}
                            ]
                        }
                    ]
                }
            ]
        }

        # Armar la respuesta final
        return {
            "usuario": {
                "id_usuario": usuario.id_usuario,
                "nombre": f"{usuario.nombre_usuario} {usuario.apellido_usuario}",
                "edad": edad,
                "grado": grado,
                "preferencias": preferencias
            },
            "recomendaciones": [fase_1, fase_2]
        }


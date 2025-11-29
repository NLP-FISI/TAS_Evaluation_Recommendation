"""Script para actualizar el contenido del texto ID 2"""
from app.core.database import SessionLocal
from app.models.texto import Texto

# Contenido del texto 2
CONTENIDO_TEXTO_2 = """¡Miles de animales NUNCA más regresarán a su hogar!

Secuestrado
Guacamayo escarlata, 2 años
Fue visto por última vez en uno de los bosques del distrito de Iñapari, en la región Madre de Dios.

Secuestrado
Mono Fraile, 6 meses
Fue visto por última vez en el valle del Bajo Huallaga, en la región San Martín.

Entre los años 2000 y 2016, se han rescatado cerca de 67000 animales vivos.

Se rescataron 1897 ranas gigantes del lago Titicaca. Estas son una de las especies más traficadas. Solo en el año 2017, 10000 animales vivos fueron rescatados, entre aves, mamíferos, reptiles y otras especies.

Puno, Ucayali, Lima y Loreto son las regiones con el mayor número de animales rescatados.

¡Luchemos juntos contra el tráfico ilegal de animales silvestres!

El tráfico de animales consiste en comprar o vender un animal silvestre. Ocurre principalmente porque algunas personas creen que estos animales se pueden tener como mascotas. Otras razones menos frecuentes son el uso de estos animales como amuletos de la suerte o, incluso, como insumos para preparar comida exótica. Lo que muchos no saben es que los traficantes los sacan de sus lugares de origen y los transportan en condiciones que ponen en riesgo sus vidas.

Para conocer animales silvestres, visita áreas protegidas como el Parque Nacional Tingo María o la Reserva Nacional de Tambopata.

¿Quieres saber más sobre el tráfico ilegal de animales silvestres?
Ingresa a www.sicompraserescomplice.pe

Si conoces algún caso, avisa a las autoridades en la página web www.serfor.gob.pe/denunciasserfor/ o llama al 947588269

SERFOR
Servicio Nacional Forestal y de Fauna Silvestre"""

def main():
    db = SessionLocal()
    try:
        # Buscar el texto con ID 2
        texto = db.query(Texto).filter(Texto.id_texto == 2).first()
        
        if texto:
            print(f"✓ Texto encontrado: ID={texto.id_texto}")
            print(f"  Título actual: {texto.titulo}")
            print(f"  Contenido actual (primeros 100 chars): {texto.contenido[:100] if texto.contenido else 'VACÍO'}...")
            
            # Actualizar contenido
            texto.contenido = CONTENIDO_TEXTO_2
            
            # Si el título está vacío, actualizarlo también
            if not texto.titulo or texto.titulo.strip() == "":
                texto.titulo = "Tráfico de animales silvestres"
                print(f"  ✓ Título actualizado a: {texto.titulo}")
            
            db.commit()
            print(f"\n✓ Contenido del texto ID 2 actualizado exitosamente")
            print(f"  Nuevo contenido (primeros 150 chars): {texto.contenido[:150]}...")
            
        else:
            print(f"✗ No se encontró el texto con ID 2")
            print("  Textos disponibles:")
            textos = db.query(Texto).all()
            for t in textos:
                print(f"    - ID {t.id_texto}: {t.titulo}")
    
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()

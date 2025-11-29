import sys
sys.path.insert(0, 'd:/GitHub- Proyectos/TAS_Evaluation_Recommendation')

from app.core.database import SessionLocal
from app.models.texto import Texto

# Contenido del texto 2 en formato HTML (similar al afiche de la imagen)
CONTENIDO_HTML = """<div class="afiche-animales">
  <h1 class="titulo-principal">¡Miles de animales <span class="destacado">NUNCA</span> más regresarán a su hogar!</h1>
  
  <div class="seccion-secuestrados">
    <div class="animal-card">
      <h3 class="etiqueta-secuestrado">Secuestrado</h3>
      <p class="animal-info"><strong>Guacamayo escarlata, 2 años</strong></p>
      <p class="animal-descripcion">Fue visto por última vez en uno de los bosques del distrito de Iñapari, en la región Madre de Dios.</p>
    </div>
    
    <div class="animal-card">
      <h3 class="etiqueta-secuestrado">Secuestrado</h3>
      <p class="animal-info"><strong>Mono Fraile, 6 meses</strong></p>
      <p class="animal-descripcion">Fue visto por última vez en el valle del Bajo Huallaga, en la región San Martín.</p>
    </div>
  </div>
  
  <div class="estadisticas destacado-verde">
    <p><strong>Entre los años 2000 y 2016, se han rescatado cerca de 67 000 animales vivos.</strong></p>
    <p>Se rescataron <strong>1897 ranas gigantes</strong> del lago Titicaca. Estas son una de las especies más traficadas. Solo en el año 2017, <strong>10 000 animales vivos</strong> fueron rescatados, entre aves, mamíferos, reptiles y otras especies.</p>
  </div>
  
  <p class="regiones"><strong>Puno, Ucayali, Lima y Loreto</strong> son las regiones con el mayor número de animales rescatados.</p>
  
  <h2 class="llamado-accion">¡Luchemos juntos contra el tráfico ilegal de animales silvestres!</h2>
  
  <div class="definicion">
    <p>El tráfico de animales consiste en <strong>comprar o vender un animal silvestre</strong>. Ocurre principalmente porque algunas personas creen que estos animales se pueden tener como mascotas. Otras razones menos frecuentes son el uso de estos animales como amuletos de la suerte o, incluso, como insumos para preparar comida exótica. Lo que muchos no saben es que <strong>los traficantes los sacan de sus lugares de origen y los transportan en condiciones que ponen en riesgo sus vidas</strong>.</p>
  </div>
  
  <div class="recomendacion">
    <p>Para conocer animales silvestres, visita áreas protegidas como el <strong>Parque Nacional Tingo María</strong> o la <strong>Reserva Nacional de Tambopata</strong>.</p>
  </div>
  
  <div class="informacion-contacto">
    <h3>¿Quieres saber más sobre el tráfico ilegal de animales silvestres?</h3>
    <p>Ingresa a <a href="http://www.sicompraserescomplice.pe" target="_blank">www.sicompraserescomplice.pe</a></p>
    
    <p>Si conoces algún caso, avisa a las autoridades en la página web <a href="http://www.serfor.gob.pe/denunciasserfor/" target="_blank">www.serfor.gob.pe/denunciasserfor/</a> o llama al <strong>947588269</strong></p>
    
    <div class="logo-serfor">
      <p><strong>SERFOR</strong></p>
      <p class="subtitulo">Servicio Nacional Forestal<br>y de Fauna Silvestre</p>
    </div>
  </div>
</div>

<style>
.afiche-animales {
  font-family: Arial, sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  line-height: 1.6;
}

.titulo-principal {
  font-size: 28px;
  font-weight: bold;
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.destacado {
  background-color: #000;
  color: #fff;
  padding: 2px 8px;
}

.seccion-secuestrados {
  display: flex;
  gap: 20px;
  margin: 20px 0;
  flex-wrap: wrap;
}

.animal-card {
  flex: 1;
  min-width: 250px;
  border: 2px solid #ddd;
  padding: 15px;
  background: #f9f9f9;
}

.etiqueta-secuestrado {
  background-color: #fff;
  border: 2px solid #000;
  padding: 5px 10px;
  display: inline-block;
  font-weight: bold;
  margin-bottom: 10px;
}

.animal-info {
  font-weight: bold;
  margin: 10px 0;
}

.animal-descripcion {
  color: #555;
  font-size: 14px;
}

.estadisticas {
  background-color: #90EE90;
  padding: 15px;
  margin: 20px 0;
  border-left: 4px solid #2d862d;
}

.destacado-verde {
  background-color: #90EE90;
}

.regiones {
  margin: 15px 0;
  padding: 10px;
  background: #f0f0f0;
}

.llamado-accion {
  font-size: 20px;
  font-weight: bold;
  color: #c00;
  text-align: center;
  margin: 20px 0;
}

.definicion, .recomendacion {
  margin: 15px 0;
  padding: 15px;
  background: #fafafa;
  border-left: 3px solid #666;
}

.informacion-contacto {
  margin-top: 30px;
  padding: 20px;
  background: #e8f4f8;
  border: 2px solid #0066cc;
}

.informacion-contacto h3 {
  color: #0066cc;
  margin-bottom: 10px;
}

.informacion-contacto a {
  color: #0066cc;
  text-decoration: underline;
}

.logo-serfor {
  margin-top: 15px;
  padding: 15px;
  background: #fff;
  border: 2px solid #2d862d;
  text-align: center;
}

.logo-serfor strong {
  font-size: 24px;
  color: #2d862d;
  display: block;
  margin-bottom: 5px;
}

.subtitulo {
  font-size: 12px;
  color: #666;
}
</style>"""

db = SessionLocal()
try:
    texto = db.query(Texto).filter(Texto.id_texto == 2).first()
    if texto:
        texto.contenido = CONTENIDO_HTML
        if not texto.titulo:
            texto.titulo = "Tráfico de animales silvestres"
        db.commit()
        print("✓ Texto actualizado con formato HTML")
        print(f"  ID: {texto.id_texto}")
        print(f"  Título: {texto.titulo}")
        print(f"  Longitud del contenido: {len(texto.contenido)} caracteres")
    else:
        print("✗ Texto no encontrado")
        textos = db.query(Texto).all()
        print("Textos disponibles:")
        for t in textos:
            print(f"  - ID {t.id_texto}: {t.titulo}")
except Exception as e:
    print(f"✗ Error: {e}")
    db.rollback()
finally:
    db.close()

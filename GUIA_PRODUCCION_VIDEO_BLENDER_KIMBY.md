# 🎬 GUÍA DE PRODUCCIÓN AUDIOVISUAL, MODELADO 3D (BLENDER / HIXFIELD MCP) Y GUION TÉCNICO

**Proyecto:** Sistema de Control de Calidad OCR y Trazabilidad en Línea  
**Empresa:** Embutidos Kimby (Caso 1 de Estudio Industrial)  
**Entorno de Trabajo:** `d:\III Pacial 4to Año\kimby_qc_app\`  

---

## 📦 1. RESUMEN DE LOS RECURSOS GENERADOS

Para que puedas realizar tu video híbrido (grabación física con la App SCADA en tu teléfono + animación 3D de la planta en Blender con Hixfield MCP), se han creado las siguientes herramientas listas para usar:

### A. Estudio & Generador Interactivo de Etiquetas Web (`generador.html`)
- **Acceso:** Puedes abrir directamente con doble clic [`generador.html`](file:///d:/III%20Pacial%204to%20A%C3%B1o/kimby_qc_app/generador.html) en tu navegador o mediante el servidor local en `http://localhost:8000/generador.html` (o `http://192.168.1.68:8000/generador.html` en el celular).
- **Capacidades:**
  1. **Edición en tiempo real:** Cambia el producto (*Salchichas Tradicionales*, *Jamón Cocido*, *Mortadela*), lote (*KMB-2026-A01*), fecha de caducidad y turno.
  2. **Simuladores de fallas industriales:**
     - *Desgaste térmico / Borrosidad:* Slider de 0 a 10 px de desenfoque.
     - *Pines quemados del cabezal:* Genera líneas blancas horizontales que rompen los caracteres.
     - *Desvanecimiento de tinta:* Control de contraste de 30% a 100%.
     - *Arruga y reflejo especular:* Añade pliegues plásticos y brillos reales de funda termoformada al vacío.
  3. **Descarga en 1 clic:** Botón para bajar el PNG en resolución HD ($1200 \times 800\text{ px}$) o botón dorado para **Descargar el Lote Completo (las 8 etiquetas juntas)**.

### B. Pack de 8 Texturas HD Pre-generadas para Blender (`etiquetas_blender/`)
Ubicadas en [`d:\III Pacial 4to Año\kimby_qc_app\etiquetas_blender\`](file:///d:/III%20Pacial%204to%20A%C3%B1o/kimby_qc_app/etiquetas_blender):
1. `01_conforme_salchicha_viena.png` (Lote: `KMB-2026-A01`, Venc: `15/12/2026` - Aprobada ✔)
2. `02_conforme_jamon_cocido.png` (Lote: `KMB-2026-B14`, Venc: `20/01/2027` - Aprobada ✔)
3. `03_conforme_mortadela_familiar.png` (Lote: `KMB-2026-C08`, Venc: `05/02/2027` - Aprobada ✔)
4. `04_falla_cabezal_pines_rotos.png` (Simula pines térmicos quemados, corta las letras KMB - Rechazada ✖)
5. `05_falla_impresion_borrosa_frotada.png` (Falla térmica del caso Kimby, texto borroso - Rechazada ✖)
6. `06_falla_producto_vencido.png` (Lote legible pero fecha caducada `10/01/2023` - Rechazada ✖)
7. `07_falla_codigo_trunco_ilegible.png` (Lote incompleto `KM-26`, falta KMB y longitud - Rechazada ✖)
8. `08_falla_arruga_y_reflejo_luz.png` (Reflejo plástico y arruga de empaque al vacío - Rechazada ✖)

### C. Script de Automatización Total en Blender (`setup_blender_scene.py`)
- Ubicado en [`setup_blender_scene.py`](file:///d:/III%20Pacial%204to%20A%C3%B1o/kimby_qc_app/setup_blender_scene.py).
- Solo debes abrir Blender -> Pestaña **Scripting** -> Pegar el código y pulsar **Run Script**. Construye toda la banda, pórtico de cámara, pistón neumático, empaques con etiquetas UV y animación pre-cocinada.

---

## 🛠️ 2. GUÍA DE ESCENA EN BLENDER & PROMPTS PARA HIXFIELD MCP

### Arquitectura de la Escena 3D
| Componente | Objeto en Blender | Dimensiones / Propiedades |
| :--- | :--- | :--- |
| **Cinta Transportadora** | `Conveyor_Belt` + `Conveyor_Frame` | Ancho 0.6 m, Largo 6.0 m. Acero inox satinado + banda negra o azul sanitaria. |
| **Pórtico de Visión** | `Vision_Post` + `Vision_Arm` | Altura 1.0 m, en aluminio estructural Bosch Rexroth. |
| **Cámara Industrial** | `Industrial_Camera_Body` + Lente | Carcasa naranja/amarilla (estilo Cognex/Basler) a 25 cm sobre la banda. |
| **Iluminación Estroboscópica** | `LED_Ring_Light` + `Strobe_Inspection_Flash` | Anillo blanco cenital. Emite flash de 350W al paso de cada paquete. |
| **Actuador Neumático** | `Pneumatic_Cylinder` + `Pneumatic_Pusher_Plate` | Cilindro de aluminio a 90° con zapata de polietileno azul (POM). Ubicado a 85 cm de la cámara. |
| **Rampa de Descarte** | `Reject_Merma_Bin` | Tolva metálica roja inclinada en el lado opuesto de la cinta. |
| **Paquetes de Salchichas** | `Kimby_Pack_X` | Cubo termoformado con bordes suaves ($36 \times 24 \times 4.5\text{ cm}$) mapeado con la textura de la etiqueta. |

### Prompts Listos para alimentar a Hixfield MCP
Si vas a conectar Blender mediante el protocolo MCP a Hixfield, utiliza los siguientes prompts por bloques:

#### Prompt 1: Construcción de Escena y Materiales
> *"Hixfield, crea una línea de envasado industrial en Blender para Embutidos Kimby. Debe incluir una cinta transportadora de acero inoxidable de 6 metros, un pórtico de inspección con una cámara de visión artificial cenital y un anillo de luces LED estroboscópicas. A 85 cm de la cámara, coloca un cilindro neumático FESTO perpendicular a la banda con una zapata de empuje plástica y una rampa de descarte al otro lado. Aplica materiales PBR realistas de grado alimenticio (acero inox AISI 304 con rugosidad 0.25 y banda plástica sanitaria)."*

#### Prompt 2: Texturizado de Paquetes
> *"Hixfield, crea 4 paquetes de salchichas al vacío sobre la cinta transportadora separados por 1 metro cada uno. Configura sus materiales Principled BSDF cargando las texturas PNG de la carpeta 'd:\III Pacial 4to Año\kimby_qc_app\etiquetas_blender\'. El paquete 1 y 2 deben tener las etiquetas conformes '01_conforme_salchicha_viena.png' y '02_conforme_jamon_cocido.png'. El paquete 3 debe tener la etiqueta defectuosa con texto borroso '05_falla_impresion_borrosa_frotada.png'. El paquete 4 debe tener la falla de pines rotos '04_falla_cabezal_pines_rotos.png'."*

#### Prompt 3: Animación de Inspección y Rechazo Neumático
> *"Hixfield, anima la escena a 30 FPS durante 240 fotogramas (8 segundos). Los paquetes deben avanzar a una velocidad constante de 0.6 m/s a lo largo de la cinta. Cuando cada paquete cruza debajo de la cámara de visión artificial, anima la energía de la luz estroboscópica para producir un destello de flash de 1 fotograma. Cuando el paquete 3 (defectuoso) llegue frente al pistón neumático, activa el pistón con una curva de animación rápida (Fast Out): el pistón debe dispararse violentamente expulsando el paquete defectuoso fuera de la cinta hacia el contenedor de mermas, y luego retraerse suavemente a su posición de reposo."*

#### Prompt 4: Cámara Cinematográfica
> *"Hixfield, configura una cámara cinematográfica con lente de 45mm. Inicia con un plano general orbital mostrando el flujo de producción, luego haz un acercamiento dinámico al cabezal de la cámara mientras ocurre el destello del flash sobre el paquete defectuoso, y termina con un plano medio en cámara lenta capturando el impacto del pistón neumático eyectando el producto descartado."*

---

## 📽️ 3. GUION TÉCNICO CINEMATOGRÁFICO (VIDEO HÍBRIDO FÍSICO + 3D)

**Duración Total Estimada:** 2 minutos y 30 segundos  
**Estilo:** Documental técnico de ingeniería / Caso de éxito industrial  
**Voz en Off sugerida:** Tono seguro, profesional, ritmo dinámico.  

```
=============================================================================================
ESCENA 1: EL DESAFÍO INDUSTRIAL (0:00 - 0:25)
=============================================================================================
TIPO DE TOMA:   Física (Grabación con cámara / Smartphone).
VISUAL:         Primer plano de una bandeja o paquete de salchichas real con una etiqueta 
                impresa borrosa (usar la plantilla defectuosa impresa o en pantalla). 
                La cámara hace un zoom lento mostrando el lote ilegible.
AUDIO / VOZ:    "En la industria de alimentos, un solo segundo de descuido puede costar millones.
                En Embutidos Kimby, una microfalla en los cabezales térmicos provocó que un lote
                completo saliera al mercado con la fecha de caducidad ilegible. El resultado:
                devoluciones masivas, sanciones sanitarias y pérdida de confianza del cliente."
SFX:            Sonido ambiente de fábrica distante, tono de advertencia grave (bips de error).

=============================================================================================
ESCENA 2: LA ARQUITECTURA DE LA SOLUCIÓN (0:25 - 0:50)
=============================================================================================
TIPO DE TOMA:   Híbrida (Captura de pantalla de la App SCADA Kimby + Diagrama de arquitectura).
VISUAL:         Transición rápida a la interfaz móvil de la App Kimby QC. Muestra el estado
                'SISTEMA EN LÍNEA' en verde, el recuadro de preprocesamiento de visión
                (escala de grises, contraste, binarización Otsu) y los paneles de telemetría.
AUDIO / VOZ:    "Para solucionar este problema de raíz sin incurrir en equipos costosos de
                decenas de miles de dólares, diseñamos un sistema de inspección automatizada en línea.
                Utilizando visión por computadora local y una red neuronal LSTM con Tesseract.js,
                el sistema procesa cada empaque en milisegundos directamente en el borde,
                100% offline, validando el prefijo KMB, la integridad del lote y la caducidad."
SFX:            Sonido de tecleo suave y pulso digital de sincronización de datos.

=============================================================================================
ESCENA 3: DEMOSTRACIÓN FÍSICA EN VIVO (0:50 - 1:35)
=============================================================================================
TIPO DE TOMA:   Física (Grabación directa con teléfono escaneando las etiquetas de prueba).
VISUAL:         
  - Toma 3.1:   El usuario apunta la cámara del teléfono hacia la 'Etiqueta 1 Conforme' 
                (en la pantalla de la PC o recortada en papel). 
                La app detecta 'KMB-2026-A01', marca el banner verde 'LOTE CONFORME',
                suena el chime melodioso y se registra el timestamp en la bitácora.
  - Toma 3.2:   El usuario mueve la cámara hacia la 'Etiqueta 2: Falla de Cabezal' o 'Etiqueta 4: Pines Rotos'.
                Instantáneamente la pantalla parpadea en rojo estroboscópico, la alarma industrial
                suena fuertemente, el indicador del brazo neumático cambia a ROJO 'ACTIVADO'
                y en pantalla se lee: 'RECHAZADO: Cabezal térmico degradado / Ilegible'.
  - Toma 3.3:   Prueba con la 'Etiqueta de Producto Vencido'. El sistema lee el texto pero bloquea
                por regla de inocuidad alimentaria.
AUDIO / VOZ:    "Veámoslo en acción. Al escanear una etiqueta conforme, el OCR valida los caracteres,
                confirma que la fecha es futura y otorga pase libre. Pero si un cabezal térmico
                pierde pines o la tinta se corre... ¡el sistema lo detecta en tiempo real!
                Inmediatamente dispara una alarma óptica, una sirena sonora y envía un pulso
                de 24 voltios al actuador neumático de descarte."
SFX:            Chime positivo agradable (ding ✔) -> Luego Buzzer industrial estridente (BZZZZT ✖)
                y clic de relé.

=============================================================================================
ESCENA 4: SIMULACIÓN 3D EN PLANTA (BLENDER + HIXFIELD MCP) (1:35 - 2:15)
=============================================================================================
TIPO DE TOMA:   Animación 3D Fotorrealista (Render de Blender / Hixfield MCP).
VISUAL:         
  - Toma 4.1:   (Plano general orbital): La cinta transportadora de acero inoxidable avanza suavemente.
                Los paquetes de salchichas Kimby se desplazan en fila hacia el pórtico de inspección.
  - Toma 4.2:   (Primer plano cenital): Un paquete conforme pasa bajo la cámara. El anillo LED emite
                un flash estroboscópico de alta velocidad. El paquete continúa su camino hacia encartonado.
  - Toma 4.3:   (Cámara lenta lateral): Llega el paquete con la etiqueta borrosa (textura con falla).
                El flash se dispara. A 85 cm de distancia, el pistón neumático FESTO se extiende
                a toda velocidad con un disparo de aire a presión, empujando con la zapata azul el
                paquete defectuoso hacia la rampa roja de mermas. El pistón se retrae en 0.2 segundos.
AUDIO / VOZ:    "En la línea de producción real, recreada aquí en nuestra simulación 3D de alta
                fidelidad, cada paquete cruza la estación de inspección a 1.2 metros por segundo.
                La iluminación estroboscópica congela el movimiento evitando cualquier desenfoque.
                Al identificarse el empaque defectuoso, el cilindro neumático ejecuta una eyección
                precisa a 90 grados, desviándolo hacia la tolva de mermas sin detener jamás el flujo
                de la planta."
SFX:            Zumbido de motor eléctrico continuo, doble 'clic-flash' estroboscópico,
                fuerte escape de aire neumático comprimido (PFFFT-KLANK!) al golpear el paquete.

=============================================================================================
ESCENA 5: IMPACTO Y RETORNO DE INVERSIÓN (2:15 - 2:30)
=============================================================================================
TIPO DE TOMA:   Gráficos en pantalla / Motion Graphics + Cierre con la app.
VISUAL:         La tabla de auditoría en la app descargando el reporte CSV con todas las piezas
                inspeccionadas. Aparecen tres métricas clave:
                - 100% Trazabilidad automatizada
                - 0% Devoluciones de producto por lote ilegible
                - < $50 USD costo de hardware (usando Edge Vision / Dispositivo existente)
AUDIO / VOZ:    "Con esta solución de visión artificial accesible y robusta, Embutidos Kimby
                elimina el 100% de las devoluciones por errores de impresión, protege la salud
                del consumidor y garantiza la máxima trazabilidad en cada bocado.
                Calidad garantizada, de la fábrica a tu mesa."
SFX:            Música corporativa de cierre ascendente y logotipo final de Kimby.
=============================================================================================
```

---

## 🚀 4. PASO A PASO PARA EJECUTAR EL PROYECTO HOY

1. **Generar o personalizar más etiquetas:**
   - Abre [`generador.html`](file:///d:/III%20Pacial%204to%20A%C3%B1o/kimby_qc_app/generador.html) en tu navegador.
   - Si quieres una etiqueta con un nombre o fecha específica, cámbiala y dale clic a **Descargar Esta Etiqueta (PNG)**.
   - O pulsa **Descargar Lote Completo (8 Etiquetas)** para tenerlas todas en tu carpeta de descargas.

2. **Cargar la escena en Blender:**
   - Abre Blender.
   - Pestaña superior **Scripting** -> **Open** (o pega el contenido de [`setup_blender_scene.py`](file:///d:/III%20Pacial%204to%20A%C3%B1o/kimby_qc_app/setup_blender_scene.py)).
   - Pulsa **Run Script**. Verás cómo se crea automáticamente toda la planta con las texturas aplicadas y la animación lista para reproducir con la barra espaciadora.
   - Si usas Hixfield MCP, pásale los prompts de la Sección 2 para afinar la iluminación en Cycles o Eevee y exportar el video final.

3. **Grabar la parte física:**
   - Inicia el servidor con [`iniciar_app.bat`](file:///d:/III%20Pacial%204to%20A%C3%B1o/kimby_qc_app/iniciar_app.bat).
   - Abre en tu celular `http://192.168.1.68:8000` (o usa la cámara de la computadora).
   - Apunta a las etiquetas y graba la pantalla o la interacción en vivo para las escenas 1, 2 y 3 del guion.

#!/usr/bin/env python3
"""
Generador del Informe Oficial ULSA 2026 - Caso de Estudio: Embutidos Kimby
========================================================================
Asignatura: Control de Calidad / Visión Artificial / Automatización Industrial
Formato: Normas APA 7ma Edición (Márgenes 2.54 cm, Interlineado 1.5, Texto 100% Negro)
Autor: Emilio Rafael Rojas Molinares
Docente: Ing. Fimvark Guzmán Orozco
Enfoque: Explicación amplia en texto, sin fórmulas innecesarias, respondiendo
         directamente a las 5 tareas solicitadas por el profesor, respaldado con
         las capturas completas de la aplicación de escritorio y móvil.
"""

import os
import zipfile
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx2pdf import convert

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOTX_PATH = os.path.join(BASE_DIR, "Plantilla Word ULSA 2026 (14).dotx")
TEMP_DOCX = os.path.join(BASE_DIR, "plantilla_convertida.docx")
FINAL_DOCX = os.path.join(BASE_DIR, "INFORME_TECNICO_KIMBY_QC_ULSA_2026.docx")
FINAL_PDF = os.path.join(BASE_DIR, "INFORME_TECNICO_KIMBY_QC_ULSA_2026.pdf")

# 1. Preparar la plantilla ULSA cambiando el Content-Type de .dotx a .docx
print("[1/5] Preparando plantilla base ULSA 2026...")
with zipfile.ZipFile(DOTX_PATH, 'r') as zin:
    with zipfile.ZipFile(TEMP_DOCX, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == '[Content_Types].xml':
                data_str = data.decode('utf-8')
                data_str = data_str.replace(
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.template.main+xml',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'
                )
                data = data_str.encode('utf-8')
            zout.writestr(item, data)

doc = docx.Document(TEMP_DOCX)

# Configurar Márgenes APA 7ma Edición (2.54 cm / 1.0 pulgada en todos los bordes)
section = doc.sections[0]
section.top_margin = Inches(1.0)
section.bottom_margin = Inches(1.0)
section.left_margin = Inches(1.0)
section.right_margin = Inches(1.0)

# 2. Configurar la Portada Oficial Institucional (Todo en Negro Puro)
print("[2/5] Personalizando Portada Oficial ULSA...")
BLACK = RGBColor(0, 0, 0)
FONT_NAME = "Arial"
FONT_SIZE = Pt(11)
LINE_SPACING = 1.5

for p_idx in [4, 5]:
    if p_idx < len(doc.paragraphs):
        for run in doc.paragraphs[p_idx].runs:
            run.font.color.rgb = BLACK

p8 = doc.paragraphs[8]
p8.text = "FACULTAD DE INGENIERÍA • INGENIERÍA MECATRÓNICA"
p8.runs[0].font.bold = True
p8.runs[0].font.name = FONT_NAME
p8.runs[0].font.size = Pt(13)
p8.runs[0].font.color.rgb = BLACK

p9 = doc.paragraphs[9]
p9.text = "RESOLUCIÓN DE CASO DE ESTUDIO: SISTEMA AUTOMATIZADO DE INSPECCIÓN EN LÍNEA Y CONTROL DE CALIDAD POR VISIÓN ARTIFICIAL (EMBUTIDOS KIMBY)"
p9.runs[0].font.bold = True
p9.runs[0].font.name = FONT_NAME
p9.runs[0].font.size = Pt(14)
p9.runs[0].font.color.rgb = BLACK

p15 = doc.paragraphs[15]
p15.text = "Presentado por:"
p15.runs[0].font.bold = True
p15.runs[0].font.name = FONT_NAME
p15.runs[0].font.color.rgb = BLACK

p16 = doc.paragraphs[16]
p16.text = "Emilio Rafael Rojas Molinares"
p16.runs[0].font.bold = False
p16.runs[0].font.name = FONT_NAME
p16.runs[0].font.size = Pt(12)
p16.runs[0].font.color.rgb = BLACK

for idx in [17, 18]:
    doc.paragraphs[idx].text = ""

p19 = doc.paragraphs[19]
p19.text = "Revisado por:"
p19.runs[0].font.bold = True
p19.runs[0].font.name = FONT_NAME
p19.runs[0].font.color.rgb = BLACK

p20 = doc.paragraphs[20]
p20.text = "Ing. Fimvark Guzmán Orozco"
p20.runs[0].font.bold = False
p20.runs[0].font.name = FONT_NAME
p20.runs[0].font.size = Pt(12)
p20.runs[0].font.color.rgb = BLACK

for idx in [21, 22, 23, 24]:
    doc.paragraphs[idx].text = ""

p25 = doc.paragraphs[25]
p25.text = "León, Nicaragua — Octubre de 2026"
p25.runs[0].font.italic = True
p25.runs[0].font.name = FONT_NAME
p25.runs[0].font.color.rgb = BLACK

# Encabezado institucional de páginas siguientes (100% negro)
header = doc.sections[0].header
if len(header.paragraphs) >= 2:
    header.paragraphs[1].text = " CONTROL DE CALIDAD Y TRAZABILIDAD OCR - EMBUTIDOS KIMBY"
    header.paragraphs[1].runs[0].font.name = FONT_NAME
    header.paragraphs[1].runs[0].font.size = Pt(8.5)
    header.paragraphs[1].runs[0].font.color.rgb = BLACK

# Eliminar contenido de relleno de la plantilla (a partir de P26)
for p in list(doc.paragraphs[26:]):
    p._p.getparent().remove(p._p)

for t in list(doc.tables):
    t._element.getparent().remove(t._element)

# Iniciar contenido formal en la siguiente página
doc.add_page_break()

# -------------------------------------------------------------
# HELPERS DE FORMATO APA 7ma EDICIÓN (100% NEGRO)
# -------------------------------------------------------------
def add_apa_heading(title, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    
    r = p.add_run(title)
    r.font.name = FONT_NAME
    r.bold = True
    r.font.color.rgb = BLACK
    
    if level == 1:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r.font.size = Pt(13)
    elif level == 2:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r.font.size = Pt(12)
    elif level == 3:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r.font.size = Pt(11)
        r.italic = True
    return p

def add_apa_body(text, bold_prefix=None, space_after=6, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = LINE_SPACING
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = FONT_NAME
        r_pre.font.size = FONT_SIZE
        r_pre.font.color.rgb = BLACK
    r = p.add_run(text)
    r.font.name = FONT_NAME
    r.font.size = FONT_SIZE
    r.font.color.rgb = BLACK
    if italic:
        r.italic = True
    return p

def add_apa_bullet(bold_label, text):
    p = doc.add_paragraph(style='List Paragraph')
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = LINE_SPACING
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r1 = p.add_run(f"• {bold_label}: ")
    r1.bold = True
    r1.font.name = FONT_NAME
    r1.font.size = FONT_SIZE
    r1.font.color.rgb = BLACK
    r2 = p.add_run(text)
    r2.font.name = FONT_NAME
    r2.font.size = FONT_SIZE
    r2.font.color.rgb = BLACK
    return p

def add_apa_table(table_num_str, title_str, headers, rows_data, note_str=None, col_widths=None):
    p_num = doc.add_paragraph()
    p_num.paragraph_format.space_before = Pt(12)
    p_num.paragraph_format.space_after = Pt(2)
    p_num.paragraph_format.keep_with_next = True
    r_num = p_num.add_run(f"Tabla {table_num_str}")
    r_num.bold = True
    r_num.font.name = FONT_NAME
    r_num.font.size = Pt(10.5)
    r_num.font.color.rgb = BLACK

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_after = Pt(6)
    p_title.paragraph_format.keep_with_next = True
    r_title = p_title.add_run(title_str)
    r_title.italic = True
    r_title.font.name = FONT_NAME
    r_title.font.size = Pt(10.5)
    r_title.font.color.rgb = BLACK

    t = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = t._tbl.tblPr
    
    borders_elm = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        f'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="000000"/>'
        f'<w:insideH w:val="none"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders_elm)

    hdr_row = t.rows[0]
    for i, h_text in enumerate(headers):
        cell = hdr_row.cells[i]
        cell.text = h_text
        tcPr = cell._tc.get_or_add_tcPr()
        b_bottom = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/></w:tcBorders>')
        tcPr.append(b_bottom)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.bold = True
            r.font.name = FONT_NAME
            r.font.size = Pt(9.5)
            r.font.color.rgb = BLACK

    for r_idx, row_vals in enumerate(rows_data):
        row_cells = t.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_vals):
            row_cells[c_idx].text = str(val)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx > 0 else WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = FONT_NAME
                r.font.size = Pt(9)
                r.font.color.rgb = BLACK

    if col_widths:
        for row in t.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    if note_str:
        p_note = doc.add_paragraph()
        p_note.paragraph_format.space_before = Pt(4)
        p_note.paragraph_format.space_after = Pt(10)
        p_note.paragraph_format.line_spacing = 1.15
        r_n_tag = p_note.add_run("Nota. ")
        r_n_tag.italic = True
        r_n_tag.font.name = FONT_NAME
        r_n_tag.font.size = Pt(9)
        r_n_tag.font.color.rgb = BLACK
        r_n_text = p_note.add_run(note_str)
        r_n_text.font.name = FONT_NAME
        r_n_text.font.size = Pt(9)
        r_n_text.font.color.rgb = BLACK

    return t

def add_apa_figure(fig_num_str, title_str, img_path, note_str=None, width_inches=5.5):
    full_path = os.path.join(BASE_DIR, img_path)
    if os.path.exists(full_path):
        p_num = doc.add_paragraph()
        p_num.paragraph_format.space_before = Pt(12)
        p_num.paragraph_format.space_after = Pt(2)
        p_num.paragraph_format.keep_with_next = True
        r_num = p_num.add_run(f"Figura {fig_num_str}")
        r_num.bold = True
        r_num.font.name = FONT_NAME
        r_num.font.size = Pt(10.5)
        r_num.font.color.rgb = BLACK

        p_title = doc.add_paragraph()
        p_title.paragraph_format.space_after = Pt(6)
        p_title.paragraph_format.keep_with_next = True
        r_title = p_title.add_run(title_str)
        r_title.italic = True
        r_title.font.name = FONT_NAME
        r_title.font.size = Pt(10.5)
        r_title.font.color.rgb = BLACK

        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(4)
        doc.add_picture(full_path, width=Inches(width_inches))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

        if note_str:
            p_note = doc.add_paragraph()
            p_note.paragraph_format.space_before = Pt(4)
            p_note.paragraph_format.space_after = Pt(10)
            p_note.paragraph_format.line_spacing = 1.15
            r_n_tag = p_note.add_run("Nota. ")
            r_n_tag.italic = True
            r_n_tag.font.name = FONT_NAME
            r_n_tag.font.size = Pt(9)
            r_n_tag.font.color.rgb = BLACK
            r_n_text = p_note.add_run(note_str)
            r_n_text.font.name = FONT_NAME
            r_n_text.font.size = Pt(9)
            r_n_text.font.color.rgb = BLACK

def add_apa_equation(omml_content, eq_num_str):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = tbl._tbl.tblPr
    borders = parse_xml(f'<w:tblBorders {nsdecls("w")}><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/></w:tblBorders>')
    tblPr.append(borders)
    
    c1 = tbl.rows[0].cells[0]
    c1.width = Inches(5.8)
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(4)
    p1.paragraph_format.space_after = Pt(4)
    
    omml_wrapper = f'<m:oMath xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">{omml_content}</m:oMath>'
    p1._p.append(parse_xml(omml_wrapper))
    
    c2 = tbl.rows[0].cells[1]
    c2.width = Inches(0.7)
    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p2.paragraph_format.space_before = Pt(6)
    p2.paragraph_format.space_after = Pt(4)
    r2 = p2.add_run(f"({eq_num_str})")
    r2.font.size = Pt(10.5)
    r2.font.name = "Cambria Math"
    r2.font.color.rgb = BLACK

print("[3/5] Redactando las tareas requeridas por el docente con explicaciones detalladas...")

# -------------------------------------------------------------
# 1. INTRODUCCIÓN AL CASO DE ESTUDIO
# -------------------------------------------------------------
add_apa_heading("1. Introducción al Caso de Estudio: Embutidos Kimby", level=1)

add_apa_body(
    "En la industria moderna de alimentos y procesamiento cárnico, la correcta identificación y la trazabilidad de los productos "
    "no constituyen únicamente un estándar de calidad interna, sino un requisito legal y sanitario estricto regulado por las autoridades "
    "de salud pública y normativas internacionales como el CODEX Alimentarius. La impresión de la fecha de vencimiento y el número de lote "
    "sobre el empaque plástico garantiza que el consumidor final adquiera un producto seguro y permite a la empresa rastrear de inmediato "
    "el turno de fabricación, la materia prima empleada y la línea de envasado en caso de cualquier eventualidad sanitaria."
)

add_apa_body(
    "Embutidos Kimby cuenta con una línea de producción continua donde imprime automáticamente, mediante cabezales de transferencia térmica, "
    "la codificación alfanumérica sobre el film plástico retráctil de cada paquete antes de su encartonado. Recientemente, la empresa enfrentó "
    "un grave problema operativo: una falla menor en los cabezales de impresión térmica provocó que un lote completo saliera al mercado con la fecha "
    "de vencimiento borrosa e ilegible. Esta situación derivó en devoluciones masivas y costosas por parte de las cadenas distribuidoras y supermercados, "
    "generando pérdidas económicas por mermas y una severa advertencia de los organismos de control de calidad."
)

add_apa_body(
    "Para dar una solución definitiva y viable a este problema, la empresa requiere la implementación de un sistema de inspección automatizada en línea "
    "basado en una cámara inteligente y económica que capture la etiqueta en pleno movimiento, realice la lectura óptica de caracteres (OCR) en tiempo real, "
    "valide los datos contra las reglas de producción y accione un brazo neumático de descarte para expulsar de inmediato cualquier empaque con impresión defectuosa, "
    "código incompleto o fecha vencida. A continuación, se da respuesta detallada y justificada a cada una de las tareas asignadas."
)

# -------------------------------------------------------------
# 2. TAREA 1: RESTRICCIONES DE VELOCIDAD EN TIEMPO REAL
# -------------------------------------------------------------
add_apa_heading("2. Tarea 1: Análisis de Restricciones de Velocidad en Tiempo Real", level=1)

add_apa_body(
    "Uno de los desafíos técnicos más importantes en la automatización industrial es comprender la diferencia fundamental que existe entre "
    "el procesamiento de imágenes estáticas (como el escaneo de documentos en una oficina) y la visión por computadora aplicada en tiempo real "
    "sobre una línea de producción en movimiento continuo. Mientras que en un entorno administrativo un escáner puede tomarse entre 5 y 15 segundos "
    "para digitalizar una hoja de papel sin ninguna consecuencia negativa, en una línea de empaque industrial los productos no esperan; "
    "el tiempo disponible para capturar, procesar y decidir es extremadamente reducido y está delimitado de forma estricta por la cinemática de la banda transportadora."
)

add_apa_body(
    "En la línea de Embutidos Kimby, los paquetes se desplazan a una velocidad lineal típica de 1.0 a 1.2 metros por segundo, con una cadencia "
    "de producción de hasta 100 a 120 paquetes por minuto. Esto significa que cada producto tarda únicamente entre 500 y 600 milisegundos en pasar "
    "frente a una estación de trabajo determinada. Más crítico aún: desde el momento exacto en que la cámara toma la fotografía de la etiqueta hasta "
    "que el paquete alcanza físicamente la posición del brazo neumático de descarte (ubicado a escasos 80 centímetros de distancia), transcurren apenas "
    "unos 650 a 700 milisegundos. Dentro de esa estrecha ventana temporal, el sistema debe haber concluido todo el ciclo de adquisición, recorte, "
    "preprocesamiento, inferencia OCR y envío de la señal eléctrica al PLC."
)

add_apa_body(
    "Por esta razón, la fase de preprocesamiento de imagen debe ser sumamente rápida, ligera y optimizada. Si el algoritmo de visión intentara "
    "aplicar filtros digitales pesados (como convoluciones gaussianas profundas, múltiples pasadas morfológicas, transformadas de Hough complejas "
    "o redes neuronales densas de segmentación semántica), el tiempo de procesamiento superaría los 300 o 400 milisegundos. Esto causaría dos fallas críticas: "
    "en primer lugar, se produciría un desbordamiento en el buffer de memoria del procesador (congelamiento del sistema o pérdida de fotogramas); "
    "en segundo lugar, para cuando el sistema determine que el producto tenía la fecha defectuosa, el paquete ya habrá pasado de largo por delante del brazo "
    "neumático, impidiendo su rechazo físico y permitiendo que la pieza defectuosa continúe hacia el embalaje final."
)

add_apa_body(
    "Otro fenómeno físico determinante derivado de la velocidad es el desenfoque por movimiento (conocido en visión artificial como Motion Blur). "
    "Cuando un objeto se desplaza mientras el obturador de la cámara permanece expuesto a la luz, la imagen proyectada sobre el sensor se corre, "
    "generando un barrido que hace que los caracteres individuales se fusionen unos con otros, volviéndolos completamente ilegibles para cualquier motor OCR. "
    "La magnitud física de este desenfoque se rige por la relación directa entre la velocidad de la banda y el tiempo de exposición de la cámara, "
    "expresada mediante la Ecuación 1:"
)

# Ecuación 1 OMML
eq1_omml = '<m:r><m:t>B = v · </m:t></m:r><m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>exp</m:t></m:r></m:sub></m:sSub>'
add_apa_equation(eq1_omml, "1")

add_apa_body(
    "Donde B representa el corrimiento físico en milímetros, v es la velocidad de avance de la banda transportadora (1.2 m/s) y t_exp es el tiempo "
    "de exposición del sensor óptico. Si se utilizara una cámara web o una cámara convencional de video con exposición estándar de 1/30 de segundo (33.3 ms), "
    "el paquete se desplazaría 40 milímetros (4 centímetros completos) mientras la foto está siendo tomada, destruyendo por completo la nitidez del texto. "
    "En cambio, la solución en tiempo real exige combinar un sensor con obturación global (Global Shutter) y un destello de iluminación estroboscópica LED "
    "con un tiempo de exposición ultrarrápido de 1/2000 de segundo (0.5 ms o 500 microsegundos). Con este valor, el desenfoque residual se reduce a apenas 0.6 mm, "
    "lo cual equivale a menos de 3 píxeles, logrando congelar ópticamente la etiqueta en movimiento sin requerir ningún algoritmo pesado de desvanecimiento."
)

add_apa_body(
    "Por consiguiente, el preprocesamiento ligero industrial se diseña bajo tres principios de máxima eficiencia computacional: 1) Recorte directo de una "
    "Región de Interés (ROI) fija donde se ubica el fechador, descartando de inmediato el 85% restante de la imagen para no procesar píxeles innecesarios; "
    "2) Conversión directa a escala de grises mediante operaciones lineales básicas en memoria; y 3) Binarización adaptativa mediante el algoritmo de Otsu, "
    "el cual calcula el umbral óptimo a partir del histograma con una carga de cómputo casi nula. Esta estrategia permite ejecutar todo el preprocesamiento "
    "en menos de 25 milisegundos, dejando tiempo de sobra para la lectura del texto y garantizando un control en tiempo real robusto y estable."
)

# -------------------------------------------------------------
# 3. TAREA 2: DIAGNÓSTICO DEL PROBLEMA ACTUAL EN KIMBY
# -------------------------------------------------------------
add_apa_heading("3. Tarea 2: Diagnóstico Detallado del Problema en Embutidos Kimby", level=1)

add_apa_body(
    "Para entender el origen de la crisis de calidad sufrida por Embutidos Kimby, es necesario analizar las causas profundas que provocaron que un lote "
    "completo con fechas ilegibles saliera de la fábrica y llegara a las bodegas de los distribuidores sin haber sido detectado a tiempo. "
    "El diagnóstico del sistema actual evidencia fallas críticas en tres dimensiones fundamentales de la ingeniería de producción: "
    "el control de calidad, la eficiencia operativa y la escalabilidad de la planta."
)

add_apa_heading("3.1 Falla en el Control de Calidad", level=2)
add_apa_body(
    "El sistema que operaba en la planta dependía casi exclusivamente de la inspección visual manual realizada por operarios de forma periódica o aleatoria "
    "(tomando, por ejemplo, una muestra de un paquete cada 50 o 100 unidades producidas). La inspección humana presenta limitaciones fisiológicas insalvables: "
    "en jornadas de 8 horas, la fatiga ocular, la monotonía y el parpadeo inevitable impiden que un ser humano mantenga una atención constante sobre objetos "
    "que se mueven a más de un metro por segundo. Si un cabezal de impresión térmica sufre un problema justo después de una revisión manual, pueden transcurrir "
    "30, 40 o más minutos antes de que el operario vuelva a tomar otra muestra, lapso durante el cual se habrán empaquetado y sellado miles de productos defectuosos."
)
add_apa_body(
    "Asimismo, la tecnología de impresión térmica (TIJ/TTO) es susceptible a modos de falla progresivos pero silenciosos: 1) Pines térmicos rotos o quemados "
    "en la regleta resistiva del cabezal, los cuales provocan líneas horizontales blancas continuas que cortan la parte media de letras y números (impidiendo "
    "distinguir, por ejemplo, un 8 de un 3 o un 0); 2) Suciedad y acumulación de cera o grasa sobre la superficie de transferencia, lo que atenúa la temperatura "
    "y genera una impresión difusa, pálida y desvanecida; y 3) Tinta fresca que se frota o corre por contacto mecánico inmediato si el secado no es instantáneo. "
    "Al no contar con un sensor automático que verifique el 100% de los empaques de manera ininterrumpida, el sistema de control de calidad era ciego ante estas fallas."
)

add_apa_heading("3.2 Falla en la Eficiencia Operativa y Costos", level=2)
add_apa_body(
    "La eficiencia de cualquier proceso de manufactura se basa en el principio de detección temprana: entre más cerca de la causa raíz se detecte un defecto, "
    "menor será el costo de corregirlo. En Embutidos Kimby ocurrió el peor escenario posible: el defecto no se detectó en la línea de empaque, ni en el control "
    "de almacén, sino cuando el producto ya se encontraba en los camiones de reparto y en los andenes de recepción de las cadenas de supermercados."
)
add_apa_body(
    "Esto desencadenó un impacto económico severo que incluyó: costos de logística inversa (flete de retorno del producto rechazado), costo de mano de obra "
    "para abrir paquetes y reinspeccionar embutidos, pérdida total de empaques plásticos al vacío por necesidad de descarte sanitario, merma de producto por pérdida "
    "de cadena de frío durante el transporte, y penalizaciones comerciales impuestas por las cadenas mayoristas. Si la empresa hubiese contado con un sistema "
    "de visión en línea, la falla térmica se habría detectado en el primer paquete defectuoso, alertando al operador en menos de 5 segundos para limpiar o "
    "reemplazar el cabezal, reduciendo la merma a una sola unidad en lugar de un lote entero."
)

add_apa_heading("3.3 Falla en la Escalabilidad", level=2)
add_apa_body(
    "Un sistema de control dependiente del ojo humano o de controles esporádicos es completamente inescalable. Si la gerencia de Kimby decide modernizar "
    "la planta, incorporar una nueva envasadora de mayor rendimiento o aumentar la velocidad de la banda transportadora para abastecer la temporada navideña, "
    "el método de control colapsa. No es técnica ni económicamente factible colocar a dos o tres personas adicionales únicamente para mirar fijamente cómo pasan "
    "las salchichas por una cinta a alta velocidad. La falta de automatización se convierte en el cuello de botella que frena el crecimiento y la competitividad de la empresa."
)

# -------------------------------------------------------------
# 4. TAREA 3: PROPUESTA TECNOLÓGICA INTEGRAL E IMPLEMENTACIÓN
# -------------------------------------------------------------
add_apa_heading("4. Tarea 3: Propuesta Tecnológica Integral y Justificación", level=1)

add_apa_body(
    "Para resolver el problema de Embutidos Kimby de manera definitiva sin recurrir a equipos de visión artificial de altísima gama cuyos costos superan "
    "los 10,000 a 15,000 dólares, se estructuró una propuesta tecnológica basada en componentes industriales estándar, accesibles, de código abierto "
    "y arquitectura en el borde (Edge Computing). Esta solución garantiza alta fiabilidad industrial manteniendo los costos de adquisición al mínimo."
)

add_apa_bullet(
    "Sensor Óptico (Cámara Inteligente Económica con Global Shutter)",
    "Se selecciona un módulo de cámara CMOS de 1.58 MP (sensor Sony IMX296 o equivalente) con obturación global (Global Shutter) y lente de distancia "
    "focal de 8 mm con montura C/CS. A diferencia de las cámaras comerciales comunes que utilizan Rolling Shutter (las cuales leen la imagen línea por línea "
    "y distorsionan los objetos en movimiento), el Global Shutter expone la totalidad de la matriz de píxeles al mismo microsegundo exacto. Esto garantiza "
    "imágenes perfectamente nítidas y sin deformaciones geométricas del texto por un costo inferior a los $60 USD."
)

add_apa_bullet(
    "Iluminación Estroboscópica LED Difusa Cenital",
    "La visión artificial es 70% iluminación y 30% algoritmo. Los empaques plásticos de embutidos al vacío presentan arrugas y superficies muy reflectivas. "
    "Para evitar reflejos parásitos que cieguen la cámara, se integra un anillo de luz LED blanca difusa polarizada con ángulo cenital, gobernado por un "
    "driver estroboscópico de disparo rápido. El destello dura únicamente 500 microsegundos y se sincroniza con el paso exacto del paquete, logrando congelar "
    "el movimiento y haciendo que el fondo blanco de la etiqueta resalte con máximo contraste respecto a la tinta negra."
)

add_apa_bullet(
    "Unidad de Procesamiento en el Borde (Edge Computing Local)",
    "En lugar de depender de servicios de visión en la nube (como Google Cloud Vision o AWS Rekognition), los cuales exigen conexión constante a internet, "
    "tienen latencias impredecibles de 400 a 1200 ms y cobran tarifas por cada imagen analizada, se implementa una unidad de cómputo local (Mini PC industrial "
    "o microcomputadora tipo Raspberry Pi 5 / procesador Intel N100). Todo el procesamiento se realiza dentro de la fábrica de forma 100% desconectada, "
    "garantizando tiempos de respuesta deterministas menores a 180 ms y cero costos mensuales recurrentes."
)

add_apa_bullet(
    "Motor OCR y Software de Supervisión SCADA",
    "Se utiliza una arquitectura de software basada en el motor de reconocimiento neuronal Tesseract OCR optimizado y compilado en WebAssembly (WASM). "
    "Este motor aplica redes neuronales recurrentes (LSTM) especializadas en fuentes matriciales e industriales de cabezales térmicos. El sistema cuenta con "
    "una interfaz de usuario interactiva tipo SCADA que muestra el video del sensor en vivo, el encuadre de la etiqueta, la telemetría en tiempo real, alarmas "
    "acústicas diferenciadas (chime de confirmación para producto conforme y buzzer de 85 dB para rechazo) y una bitácora de auditoría exportable a CSV."
)

add_apa_bullet(
    "Módulo Actuador Neumático de Descarte",
    "Consiste en un cilindro neumático guiado de doble efecto (marca FESTO o similar, carrera de 100 mm y diámetro de 25 mm) montado perpendicularmente a la banda. "
    "Está accionado por una electroválvula solenoide 5/2 de 24V DC conectada al módulo de salidas digitales del controlador. La neumática es la tecnología ideal para "
    "ambientes cárnicos debido a su alta velocidad (tiempo de respuesta menor a 20 ms), inmunidad a la humedad, gran fuerza de empuje para desviar el empaque "
    "hacia la tolva de merma y bajo costo de mantenimiento."
)

# Tabla 1 APA 7
t1_headers = ["Elemento del Sistema", "Tecnología Seleccionada", "Función en la Línea", "Justificación Técnica"]
t1_rows = [
    ["Sensor Óptico", "Cámara CMOS Global Shutter ($55 USD)", "Captura fotograma instantáneo", "Evita distorsión por movimiento sin pagar miles por cámaras Cognex."],
    ["Iluminación", "Anillo LED Estroboscópico Difuso", "Flash cenital sincronizado (500 μs)", "Elimina reflejos sobre el plástico al vacío y congela el movimiento."],
    ["Unidad de Cómputo", "Mini PC Edge Computing Offline", "Procesamiento local de visión y OCR", "Cero latencia de red, 100% de disponibilidad y sin cobros por API."],
    ["Software / OCR", "Tesseract WASM + SCADA Industrial", "Lectura de texto y toma de decisión", "Motor neuronal entrenado para fuentes de cabezal térmico."],
    ["Actuador de Rechazo", "Cilindro Neumático + Válvula 24V", "Expulsión física de paquetes malos", "Accionamiento rápido (< 20 ms), higiénico y apto para planta cárnica."]
]
add_apa_table("1", "Resumen de la Propuesta Tecnológica para el Control de Calidad en Embutidos Kimby", t1_headers, t1_rows, "Componentes seleccionados para máxima eficiencia operativa a bajo costo.")

# -------------------------------------------------------------
# 5. TAREA 4: FLUJO LÓGICO Y ALGORITMO DE DECISIONES
# -------------------------------------------------------------
add_apa_heading("5. Tarea 4: Diseño del Flujo Lógico del Proceso y Algoritmo de Decisión", level=1)

add_apa_body(
    "El funcionamiento del sistema se diseñó bajo una lógica secuencial determinista gobernada por estados, asegurando que cada empaque que atraviese "
    "la zona de inspección sea procesado de forma individual y sincronizada con el avance mecánico de la línea. A continuación, se detalla el paso a paso "
    "del flujo lógico:"
)

add_apa_bullet("Paso 1: Detección Física de Entrada (Trigger)", "El empaque avanza sobre la banda y su borde delantero interrumpe el haz de un sensor fotoeléctrico reflectivo. Este evento genera una señal de disparo (interrupción de hardware) inmediata hacia el controlador.")
add_apa_bullet("Paso 2: Disparo Estroboscópico y Captura", "Al recibir el pulso del sensor, el controlador activa simultáneamente el driver de iluminación LED y el obturador de la cámara por exactamente 500 microsegundos, congelando la imagen de la etiqueta sobre el fondo de la banda.")
add_apa_bullet("Paso 3: Recorte de ROI y Preprocesamiento Rápido", "El algoritmo extrae automáticamente las coordenadas fijas de la Región de Interés (ROI de 60x25 mm) donde se encuentra el fechador térmico. Convierte los píxeles a escala de grises y aplica binarización de Otsu, aislando la tinta negra del plástico blanco.")
add_apa_bullet("Paso 4: Extracción de Caracteres por OCR", "El motor neuronal procesa la imagen binarizada y devuelve la cadena de texto leída junto con una matriz de niveles de confianza individual por cada carácter reconocido.")
add_apa_bullet("Paso 5: Evaluación de Reglas de Calidad y Negocio", "El texto obtenido se somete a una serie de validaciones lógicas obligatorias:")
add_apa_body(
    "a) Regla de Identificador: ¿Contiene obligatoriamente el prefijo de lote de la empresa 'KMB'?\n"
    "b) Regla de Longitud de Lote: ¿Tiene el código al menos 10 caracteres válidos (formato KMB-YYYY-XXX)?\n"
    "c) Regla de Fecha de Vencimiento: ¿Es la fecha legible, tiene formato DD/MM/AAAA y es estrictamente posterior al día de fabricación actual?\n"
    "d) Regla de Legibilidad General: ¿El promedio de confianza del OCR supera el umbral mínimo del 65%?",
    space_after=4
)
add_apa_bullet("Paso 6A: Rama de Aprobación (Producto Conforme)", "Si las 4 condiciones se cumplen al 100%: El sistema emite veredicto 'APROBADO', enciende la luz verde en la pantalla SCADA, reproduce un chime acústico melodioso de confirmación, guarda el registro en la bitácora de auditoría y permite que el paquete continúe su tránsito libre hacia la estación de encartonado.")
add_apa_bullet("Paso 6B: Rama de Rechazo (Producto Defectuoso)", "Si falla cualquiera de las 4 condiciones (falta el prefijo KMB, el lote está incompleto, la fecha está borrosa o caducada, o la confianza es baja): El sistema emite veredicto 'RECHAZADO'. Se calcula el retardo cinemático exacto en función de la velocidad de la banda (t = d / v). En el milisegundo exacto en que el paquete defectuoso se alinea frente al pistón neumático, se activa un pulso de 24V DC hacia la electroválvula. El vástago del cilindro se extiende expulsando el empaque fuera de la línea hacia la tolva de merma, se enciende la alarma roja visual y suena una sirena industrial de advertencia.")

# Tabla 2 APA 7
t2_headers = ["Condición Detectada", "Texto Extraído por OCR", "Nivel de Confianza", "Veredicto", "Acción Física del Sistema"]
t2_rows = [
    ["Etiqueta nítida y completa", "LOTE: KMB-2026-A01 | VENC: 15/12/2026", "96% (Excelente)", "APROBADO", "Libre tránsito hacia encartonado."],
    ["Líneas blancas (pines rotos)", "LOTE: KM -202 -A0  | VENC: 15/--/----", "38% (Muy bajo)", "RECHAZADO", "Disparo neumático 24V a tolva de merma."],
    ["Tinta frotada o borrosa", "LOTE: [Ilegible]  | VENC: [Ilegible]", "41% (Insuficiente)", "RECHAZADO", "Disparo neumático 24V y alarma acústica."],
    ["Fecha vencida o antigua", "LOTE: KMB-2026-A01 | VENC: 10/01/2023", "92% (Texto claro)", "RECHAZADO", "Rechazo por violación de caducidad sanitaria."],
    ["Falta prefijo 'KMB'", "LOTE: 2026-A01     | VENC: 15/12/2026", "55% (Incompleto)", "RECHAZADO", "Disparo neumático a tolva de merma."]
]
add_apa_table("2", "Matriz de Decisión Lógica del Algoritmo de Calidad Kimby", t2_headers, t2_rows, "Criterios booleanos aplicados a cada fotograma capturado.")

# -------------------------------------------------------------
# 6. TAREA 5: MITIGACIÓN DE ERRORES Y TOLERANCIAS
# -------------------------------------------------------------
add_apa_heading("6. Tarea 5: Mitigación de Errores y Ajuste de Tolerancias", level=1)

add_apa_body(
    "En cualquier sistema de inspección automatizada por visión artificial existe la posibilidad de que ocurran discrepancias entre la realidad física "
    "del producto y la interpretación del algoritmo. Responder a la pregunta planteada en el caso de estudio exige analizar con seriedad técnica qué sucede "
    "en los dos escenarios posibles de error (falsos positivos vs. falsos negativos) y cómo se deben calibrar los umbrales de tolerancia de la planta."
)

add_apa_heading("6.1 Escenario A: Aceptar un Producto Malo (Falso Negativo)", level=2)
add_apa_body(
    "Ocurre cuando el sistema comete el error de calificar como 'APROBADO' un paquete cuya fecha está borrosa, mutilada o vencida. En la industria alimentaria, "
    "este es el fallo más crítico y peligroso que puede cometer un sistema de calidad. Si una salchicha con fecha ilegible o caducada llega al consumidor final, "
    "las consecuencias son devastadoras: 1) Riesgo directo a la salud de la población; 2) Clausuras y multas severas por parte del Ministerio de Salud (MINSA); "
    "3) Devolución masiva de pedidos enteros por parte de las cadenas de supermercados; y 4) Pérdida de contratos comerciales y destrucción de la confianza "
    "en la marca Embutidos Kimby. Por tanto, en términos de ingeniería de calidad, la tasa admisible para este tipo de error es estrictamente 0.0%."
)

add_apa_heading("6.2 Escenario B: Rechazar un Producto Bueno (Falso Positivo)", level=2)
add_apa_body(
    "Ocurre cuando una etiqueta perfectamente impresa sufre una arruga en el film plástico al momento del sellado al vacío, o una sombra momentánea, "
    "provocando que el OCR confunda un carácter (por ejemplo, leyendo una 'B' como un '8') y decida expulsar el paquete a la tolva de merma. "
    "Aunque el descarte de una pieza buena representa una pérdida menor, sus consecuencias operativas son perfectamente manejables: los paquetes rechazados "
    "caen suavemente en una tolva acolchada junto a la línea. Al finalizar el turno o cada 30 minutos, un operario recoge estos paquetes, revisa visualmente "
    "los que están nítidos y los vuelve a colocar manualmente en la banda transportadora o los reetiqueta en segundos. El costo de esta reinspección "
    "es prácticamente insignificante (centavos de dólar) en comparación con el costo de una devolución comercial."
)

add_apa_heading("6.3 Política de Calidad y Calibración de Umbrales de Confianza", level=2)
add_apa_body(
    "Ante este panorama, la regla de oro en el diseño del sistema es adoptar una política de 'Cero Tolerancia Sanitaria': es infinitamente preferible asumir "
    "una tasa de falsos rechazos del 0.3% en la línea (que se resuelve con una simple revisión manual de la tolva) antes que arriesgarse a dejar pasar un solo "
    "producto con fecha borrosa hacia el mercado. Para lograr este balance óptimo sin provocar rechazos excesivos por arrugas normales del plástico, se implementan "
    "las siguientes medidas técnicas de mitigación:"
)

add_apa_bullet(
    "Ajuste del Umbral de Confianza (65% - 70%)",
    "El algoritmo no exige un 100% de confianza matemática en cada carácter para aprobar la pieza (lo que causaría rechazos masivos por cualquier micro-arruga), "
    "pero sí exige un 100% de legibilidad estructural en los campos críticos: la presencia obligatoria de las letras 'KMB' y que los dígitos numéricos de la fecha "
    "coincidan con un día y mes válidos del calendario."
)

add_apa_bullet(
    "Mitigación Física Mediante Iluminación Polarizada Difusa",
    "El problema de las arrugas no se combate relajando el software, sino eliminando la sombra física que la arruga proyecta. Al utilizar una fuente de luz LED "
    "cenital con difusor opalino y filtro polarizador cruzado con el lente de la cámara, los reflejos especulares de los pliegues plásticos se neutralizan, "
    "permitiendo que el sensor capture la tinta negra sin importar la deformación de la superficie."
)

add_apa_bullet(
    "Binarización Adaptativa Local (Otsu Dinámico)",
    "En lugar de aplicar un umbral de corte fijo a toda la etiqueta (lo que haría que las zonas más iluminadas borren texto), el algoritmo de Otsu divide el cálculo "
    "en función del contraste relativo entre la tinta térmica y el sustrato inmediato, garantizando una segmentación limpia incluso sobre plásticos arrugados."
)

# -------------------------------------------------------------
# 7. EVIDENCIA Y VALIDACIÓN DEL SISTEMA DESARROLLADO
# -------------------------------------------------------------
add_apa_heading("7. Evidencia y Validación Experimental del Sistema Desarrollado", level=1)

add_apa_body(
    "Para verificar en la práctica la efectividad de las soluciones planteadas y dar cumplimiento total al caso de estudio, se construyó y puso a punto "
    "una plataforma interactiva de inspección en tiempo real (PWA SCADA) capaz de ejecutarse tanto en monitores táctiles industriales de escritorio "
    "como en teléfonos móviles de supervisión técnica sobre Android Chrome. A continuación, se presentan las evidencias directas del software desarrollado:"
)

# Figura 1: Desktop Aprobado
add_apa_figure(
    "1",
    "Interfaz Completa de la Aplicación de Escritorio - Caso Producto Aprobado",
    "fig_desktop_aprobado.png",
    "Visualización panorámica mostrando el sensor óptico en vivo, encuadre de la etiqueta Kimby conforme, banner verde de APROBADO, "
    "telemetría con lectura del lote KMB-2026-A01, bitácora de eventos y actuador neumático en estado LISTO.",
    width_inches=5.8
)

add_apa_body(
    "Como se aprecia en la Figura 1, cuando la cámara captura una etiqueta conforme con caracteres térmicos nítidos, el sistema extrae con éxito el código "
    "de lote KMB-2026-A01 y la fecha de caducidad vigente, desplegando el banner verde de aprobación, emitiendo el tono positivo de confirmación y registrando "
    "el suceso en la bitácora sin activar el pistón de rechazo."
)

# Figura 2: Desktop Rechazado
add_apa_figure(
    "2",
    "Interfaz Completa de la Aplicación de Escritorio - Caso Producto Rechazado",
    "fig_desktop_rechazado.png",
    "Detección de falla por cabezal térmico con pines quemados, despliegue del banner rojo de DESCARTADO, activación del pulso PLC a 24V hacia el pistón "
    "neumático, telemetría indicando no detección y registro del motivo de descarte en bitácora.",
    width_inches=5.8
)

add_apa_body(
    "En la Figura 2 se observa la respuesta del sistema ante una etiqueta defectuosa con líneas blancas y pérdida de caracteres por pines quemados en el cabezal. "
    "El algoritmo detecta de inmediato que el texto no es 100% legible y que falta el código de lote completo, ordenando el disparo eléctrico de 24V hacia "
    "la electroválvula del actuador neumático para eyectar el empaque hacia la tolva de merma, salvaguardando a la empresa de cualquier reclamo."
)

# Figura 3: Mobile Sensor
add_apa_figure(
    "3",
    "Interfaz Móvil en Android Chrome - Sección de Sensor Óptico y Encuadre Completo",
    "fig_mobile_pantalla1_sensor.png",
    "Captura íntegra sin cortes laterales en pantalla de teléfono móvil, demostrando el encuadre exacto del empaque Kimby, controles táctiles y panel de reglas.",
    width_inches=3.2
)

# Figura 4: Mobile Rechazo
add_apa_figure(
    "4",
    "Interfaz Móvil en Android Chrome - Sección de Alarma de Rechazo y Disparo Neumático",
    "fig_mobile_pantalla2_rechazo.png",
    "Pantalla móvil mostrando el banner de rechazo por texto borroso, activación de disparo al pistón neumático y telemetría de auditoría.",
    width_inches=3.2
)

add_apa_body(
    "Las Figuras 3 y 4 demuestran la adaptabilidad total del software a pantallas de dispositivos móviles Android Chrome. Se corrigieron todos los problemas "
    "de desbordamiento visual previos, logrando que el operador o supervisor de planta pueda monitorear la cámara, ver el encuadre completo de la etiqueta "
    "y recibir las alarmas de descarte en la palma de su mano con perfecta legibilidad."
)

# Figura 5: Generador
add_apa_figure(
    "5",
    "Estudio Web Interactivo de Generación y Simulación de Defectos (generador.html)",
    "fig_generador_estudio.png",
    "Entorno web desarrollado para crear variantes de etiquetas Kimby, ajustar sliders de desenfoque, pérdida de pines térmicos y pliegues al vacío, "
    "permitiendo la descarga de texturas en alta resolución para pruebas físicas y animación 3D.",
    width_inches=5.8
)

add_apa_body(
    "Finalmente, la Figura 5 muestra el Estudio Web de Etiquetas (`generador.html`) programado para facilitar las pruebas del sistema. Este generador permite "
    "a los técnicos simular en tiempo real cualquier condición de falla (desenfoque de tinta, líneas de pines quemados, fechas antiguas o deformaciones plásticas) "
    "y descargar las imágenes en alta resolución, sirviendo como insumo directo tanto para calibrar el sensor físico como para texturizar la escena animada en Blender."
)

# -------------------------------------------------------------
# 8. CONCLUSIONES
# -------------------------------------------------------------
add_apa_heading("8. Conclusiones", level=1)

add_apa_body(
    "1. La problemática de legibilidad de fechas en Embutidos Kimby encuentra una solución técnica totalmente viable y económica mediante la implementación "
    "de visión artificial en el borde (Edge OCR), utilizando una cámara CMOS con Global Shutter de bajo costo ($55 USD) y procesamiento local sin depender de la nube."
)
add_apa_body(
    "2. Las restricciones cinemáticas de una línea continua de 1.2 m/s exigen que el preprocesamiento de imagen sea ultraligero (recorte de ROI, escala de grises "
    "y binarización Otsu directa) para ejecutar la inspección en menos de 180 ms, mientras que el desenfoque por movimiento se resuelve físicamente mediante "
    "un destello estroboscópico de 500 microsegundos."
)
add_apa_body(
    "3. La política de calidad de 'Cero Tolerancia Sanitaria' garantiza que ningún empaque con fecha borrosa, alterada o vencida salga jamás hacia los supermercados, "
    "eliminando de raíz las multas sanitarias y devoluciones masivas, mientras que los eventuales falsos descartes por arrugas plásticas se gestionan de forma "
    "segura y económica en la tolva de merma mediante reinspección manual periódica."
)

# -------------------------------------------------------------
# 9. REFERENCIAS BIBLIOGRÁFICAS APA 7
# -------------------------------------------------------------
add_apa_heading("Referencias", level=1)

def add_apa_reference(ref_text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = LINE_SPACING
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.5)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r = p.add_run(ref_text)
    r.font.name = FONT_NAME
    r.font.size = Pt(10)
    r.font.color.rgb = BLACK

add_apa_reference("CODEX ALIMENTARIUS. (2018). Norma General para el Etiquetado de los Alimentos Preenvasados (CODEX STAN 1-1985, Rev. 1-1991). Organización de las Naciones Unidas para la Alimentación y la Agricultura (FAO / OMS). https://www.fao.org/fao-who-codexalimentarius/")
add_apa_reference("Gonzalez, R. C., & Woods, R. E. (2018). Digital image processing (4th ed.). Pearson Education.")
add_apa_reference("International Organization for Standardization. (2007). Traceability in the feed and food chain — General principles and basic requirements for system design and implementation (ISO Standard No. 22005:2007). https://www.iso.org/standard/36224.html")
add_apa_reference("Otsu, N. (1979). A threshold selection method from gray-level histograms. IEEE Transactions on Systems, Man, and Cybernetics, 9(1), 62–66. https://doi.org/10.1109/TSMC.1979.4310076")
add_apa_reference("Smith, R. (2007). An overview of the Tesseract OCR engine. En Proceedings of the Ninth International Conference on Document Analysis and Recognition (ICDAR 2007) (Vol. 2, pp. 629–633). IEEE Computer Society. https://doi.org/10.1109/ICDAR.2007.4378789")

# 4. Guardar archivo DOCX final
print(f"[4/5] Guardando archivo Word final en: {FINAL_DOCX}...")
doc.save(FINAL_DOCX)
print("¡Documento DOCX generado exitosamente!")

# 5. Convertir a PDF utilizando docx2pdf
print(f"[5/5] Convirtiendo a PDF institucional en: {FINAL_PDF}...")
convert(FINAL_DOCX, FINAL_PDF)

if os.path.exists(FINAL_PDF):
    size_mb = os.path.getsize(FINAL_PDF) / (1024 * 1024)
    print(f"============================================================")
    print(f"¡ÉXITO ROTUNDO! El PDF ha sido generado correctamente.")
    print(f"Archivo: {FINAL_PDF}")
    print(f"Tamaño: {size_mb:.2f} MB")
    print(f"============================================================")
else:
    print("ADVERTENCIA: No se pudo verificar la existencia del archivo PDF final.")

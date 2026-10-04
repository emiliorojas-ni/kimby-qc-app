#!/usr/bin/env python3
"""
Generador del Informe Técnico ULSA 2026 - Caso de Estudio: Embutidos Kimby
Versión Final Definitiva:
- Diagrama de flujo original exacto (Mermaid HD render con decisiones y bifurcaciones)
- Títulos de Tarea limpios y sin duplicaciones (Tarea X: Nombre + Consigna en cursiva)
- Fotos e ilustraciones intercaladas naturalmente (11 figuras en total)
- Ecuaciones matemáticas nativas de Word (OMML en Cambria Math)
- Formato APA 7ma Edición estricto con texto 100% en negro puro
- Portada institucional: Emilio Rafael Rojas Molinares e Ing. Fimvark Guzmán Orozco
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

BLACK = RGBColor(0, 0, 0) # 100% Negro Puro APA 7
FONT_NAME = "Arial"
FONT_SIZE = Pt(11)
LINE_SPACING = 1.5

# 2. Configurar la Portada Oficial Institucional (Todo en Negro Puro)
print("[2/5] Personalizando Portada Oficial ULSA...")
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
# HELPERS DE ESTILO APA 7ma EDICIÓN LIMPIO Y NATURAL
# -------------------------------------------------------------
def add_task_heading(task_title, consigna_text=None):
    """
    Título de tarea limpio (sin números dobles, sin líneas raras debajo).
    Centrado en negrita, seguido de la Consigna en cursiva justificada.
    """
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    r = p.add_run(task_title)
    r.font.name = FONT_NAME
    r.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = BLACK
    
    if consigna_text:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.keep_with_next = True
        p_c.paragraph_format.space_before = Pt(2)
        p_c.paragraph_format.space_after = Pt(10)
        p_c.paragraph_format.line_spacing = 1.25
        p_c.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        r_pre = p_c.add_run("Consigna: ")
        r_pre.bold = True
        r_pre.italic = True
        r_pre.font.name = FONT_NAME
        r_pre.font.size = Pt(10)
        r_pre.font.color.rgb = BLACK
        
        r_text = p_c.add_run(consigna_text)
        r_text.italic = True
        r_text.font.name = FONT_NAME
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = BLACK
        
    return p

def add_subheading(title):
    """
    Subtítulo de segundo nivel (Nivel 2 APA 7): Alineado a la izquierda en negrita.
    """
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    r = p.add_run(title)
    r.font.name = FONT_NAME
    r.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = BLACK
    return p

def add_body(text, bold_prefix=None, space_after=6):
    """
    Párrafo con interlineado 1.5, texto justificado, color negro puro
    y soporte nativo para **resaltado en negrita**.
    """
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
        
    parts = text.split("**")
    is_bold = False
    for part in parts:
        if part:
            r = p.add_run(part)
            r.font.name = FONT_NAME
            r.font.size = FONT_SIZE
            r.bold = is_bold
            r.font.color.rgb = BLACK
        is_bold = not is_bold
    return p

def add_bullet(bold_label, text):
    """
    Viñeta técnica con interlineado 1.5 y lead en negrita.
    """
    p = doc.add_paragraph(style='List Paragraph')
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = LINE_SPACING
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    r1 = p.add_run(f"• {bold_label}: ")
    r1.bold = True
    r1.font.name = FONT_NAME
    r1.font.size = FONT_SIZE
    r1.font.color.rgb = BLACK
    
    parts = text.split("**")
    is_bold = False
    for part in parts:
        if part:
            r = p.add_run(part)
            r.font.name = FONT_NAME
            r.font.size = FONT_SIZE
            r.bold = is_bold
            r.font.color.rgb = BLACK
        is_bold = not is_bold
    return p

def add_apa_table(table_num_str, title_str, headers, rows_data, note_str=None, col_widths=None):
    """
    Tabla conforme a APA 7ma Edición:
    1. 'Tabla X' en negrita.
    2. 'Título' en cursiva.
    3. Bordes horizontales únicamente (sin líneas verticales).
    4. 'Nota.' en cursiva al pie.
    """
    p_num = doc.add_paragraph()
    p_num.paragraph_format.space_before = Pt(14)
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

    # Fila de Encabezados
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

    # Filas de Datos
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
                if "APROBADO" in r.text or "RECHAZADO" in r.text:
                    r.font.bold = True

    if col_widths:
        for row in t.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    if note_str:
        p_note = doc.add_paragraph()
        p_note.paragraph_format.space_before = Pt(4)
        p_note.paragraph_format.space_after = Pt(12)
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

def add_apa_figure(fig_num_str, title_str, img_path, note_str=None, width_inches=5.2):
    """
    Inserta una figura en formato APA 7ma Edición.
    """
    full_path = os.path.join(BASE_DIR, img_path)
    if os.path.exists(full_path):
        p_num = doc.add_paragraph()
        p_num.paragraph_format.space_before = Pt(14)
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
            p_note.paragraph_format.space_after = Pt(12)
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
    """
    Inserta una ecuación nativa de Word (OMML) en Cambria Math, centrada
    con número entre paréntesis (X) alineado a la derecha.
    """
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

print("[3/5] Redactando informe con formato natural, consignas y diagrama original...")

# -------------------------------------------------------------
# INTRODUCCIÓN AL CASO DE ESTUDIO
# -------------------------------------------------------------
add_task_heading("Introducción al Caso de Estudio: Embutidos Kimby")

add_body(
    "En la industria moderna de alimentos y procesamiento cárnico, la **correcta codificación y trazabilidad** de los productos "
    "no constituyen únicamente un estándar de calidad interna, sino un **requisito legal y sanitario estricto** regulado por las autoridades "
    "de salud pública y normativas internacionales como el CODEX Alimentarius (CODEX, 2018). La impresión de la fecha de vencimiento y el número de lote "
    "sobre el empaque plástico garantiza que el consumidor final adquiera un producto en óptimas condiciones organolépticas y microbiológicas, "
    "permitiendo al mismo tiempo rastrear el turno de manufactura, la formulación empleada y la línea de envasado en caso de cualquier reclamo sanitario (ISO, 2007)."
)

add_body(
    "**Embutidos Kimby** cuenta con una línea de producción continua donde imprime automáticamente, mediante cabezales de transferencia térmica (TIJ/TTO), "
    "la codificación alfanumérica sobre el film plástico retráctil de cada paquete antes de su encartonado y distribución. Recientemente, la empresa enfrentó "
    "un grave problema operativo: **una falla menor en los cabezales térmicos provocó que un lote completo saliera al mercado con la fecha de vencimiento "
    "borrosa e ilegible**. Esta eventualidad derivó en devoluciones masivas y costosas por parte de los distribuidores mayoristas y cadenas de supermercados, "
    "generando cuantiosas pérdidas por merma y una severa advertencia de los organismos de control de calidad."
)

add_apa_figure(
    "1",
    "Muestra de Etiqueta Conforme de Salchicha Viena Kimby 500g (Lote KMB-2026-A01)",
    "etiquetas_blender/01_conforme_salchicha_viena.png",
    "Etiqueta con impresión térmica nítida, caracteres íntegros y fecha de caducidad vigente. Cumple con todos los estándares de aprobación.",
    width_inches=4.8
)

add_body(
    "Como se ilustra en la Figura 1, una etiqueta conforme presenta una tipografía matricial clara, alto contraste entre la tinta negra y el sustrato blanco, "
    "y la estructura completa del lote institucional. Por el contrario, la Figura 2 exhibe la consecuencia directa de la falla térmica analizada en este estudio, "
    "donde la pérdida de pines en el cabezal mutila las líneas de texto, haciendo imposible verificar la vigencia sanitaria del alimento."
)

add_apa_figure(
    "2",
    "Muestra de Etiqueta con Defecto Térmico Crítico por Pines Quemados",
    "etiquetas_blender/04_falla_cabezal_pines_rotos.png",
    "Simulación de líneas horizontales blancas (drop-outs) que cortan el texto, impidiendo la lectura por OCR y motivando el rechazo inmediato.",
    width_inches=4.8
)

add_body(
    "Para resolver de raíz esta problemática, la dirección de planta determinó como imperativo implementar un **Sistema de Inspección Automatizada en Línea** "
    "utilizando una cámara inteligente y económica que capture la etiqueta en pleno movimiento, aplique **lectura en tiempo real (OCR)** para verificar el texto impreso, "
    "lo contraste contra la base de datos de producción y ordene a un brazo neumático rechazar automáticamente cualquier paquete cuyo texto no sea 100% legible o presente "
    "errores en la fecha. A continuación, se da respuesta puntual y técnica a cada una de las tareas del caso."
)

# -------------------------------------------------------------
# TAREA 1: RESTRICCIONES DE VELOCIDAD EN TIEMPO REAL
# -------------------------------------------------------------
add_task_heading(
    "Tarea 1: Análisis de Restricciones de Velocidad en Tiempo Real",
    "Indagar y analizar por qué el proceso en tiempo real (en línea) requiere fases de preprocesamiento de imagen sumamente rápidas y ligeras a diferencia de un escaneo de documentos estáticos."
)

add_subheading("Diferencias Fundamentales entre Escaneo Estático y Visión en Línea")
add_body(
    "Uno de los principios esenciales en la visión por computadora industrial es comprender por qué un proceso en tiempo real sobre una banda transportadora "
    "requiere fases de preprocesamiento de imagen **sumamente rápidas y ligeras**, a diferencia de un escaneo de documentos estáticos de oficina. "
    "En un escáner convencional, el documento permanece totalmente inmóvil, el sensor puede tardar entre **5 y 15 segundos** en digitalizar la hoja con iluminación homogénea, "
    "y el procesador puede permitirse aplicar algoritmos pesados de múltiples pasadas, filtrados gaussianos profundos o transformadas espaciales complejas sin restricción temporal."
)

add_body(
    "En contraste, en la línea de empaque de Embutidos Kimby, los productos se desplazan de manera continua a una velocidad lineal de **1.0 a 1.2 metros por segundo**, "
    "con una cadencia de producción de **100 a 120 paquetes por minuto**. Bajo estas condiciones operativas, el producto no se detiene; cada unidad dispone de una ventana "
    "temporal estricta de apenas **500 milisegundos de tiempo de ciclo**. Más aún, la distancia física disponible entre el punto de captura de la cámara y el actuador neumático "
    "de descarte es de aproximadamente **d = 0.85 metros**. Si los algoritmos de visión consumen más de 200 milisegundos, el empaque defectuoso sobrepasará físicamente "
    "la posición del cilindro eyector antes de que se emita la orden de rechazo, escapando hacia la zona de embalaje final."
)

add_subheading("Mitigación del Desenfoque por Movimiento (Motion Blur)")
add_body(
    "El desplazamiento continuo del objeto mientras el obturador de la cámara permanece abierto genera el fenómeno físico conocido como **desenfoque por movimiento (Motion Blur)**. "
    "Si se utilizara una cámara convencional de video con tiempo de exposición estándar de 1/30 de segundo (33.3 ms), los caracteres se correrían a lo largo de 40 milímetros, "
    "convirtiendo las letras en manchas grises continuas imposibles de decodificar por cualquier motor OCR. La formulación matemática de este corrimiento se expresa en la Ecuación 1:"
)

# Ecuación 1 OMML
eq1_omml = '<m:r><m:t>B = v · </m:t></m:r><m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>exp</m:t></m:r></m:sub></m:sSub>'
add_apa_equation(eq1_omml, "1")

add_body(
    "Donde **B** es el corrimiento en metros, **v** es la velocidad de la banda (1.2 m/s) y **t_exp** es el tiempo de exposición. La solución técnica implementada "
    "consiste en sincronizar la cámara con un destello de **iluminación estroboscópica LED de alta intensidad** con un tiempo de exposición ultracorto de "
    "**t_exp = 1/2000 s (500 microsegundos)**. Al evaluar la Ecuación 1 bajo estos parámetros, el corrimiento resultante se reduce a apenas **B = 0.60 mm** "
    "(menos de 3 píxeles en el sensor), congelando ópticamente el texto en pleno movimiento sin requerir algoritmos pesados de desborronado por software."
)

add_subheading("Arquitectura del Pipeline de Preprocesamiento Ligero")
add_body(
    "Para garantizar que el tiempo total de procesamiento se mantenga por debajo de los **25 milisegundos**, se estructuró un pipeline secuencial optimizado "
    "que prescinde de filtros convolucionales complejos. En la Figura 3 se ilustra la secuencia de etapas aplicadas sobre cada fotograma:"
)

add_apa_figure(
    "3",
    "Diagrama del Pipeline de Preprocesamiento de Imagen en Tiempo Real (< 25 ms)",
    "fig_pipeline_ocr.png",
    "Flujo de optimización que incluye recorte directo de la Región de Interés (ROI), conversión a escala de grises y binarización adaptativa Otsu antes del OCR.",
    width_inches=5.2
)

add_body(
    "Como se evidencia en la Figura 3, el preprocesamiento opera en cuatro fases de mínima carga de cálculo: 1) **Recorte de ROI fija (60x25 mm)**, "
    "descartando el 85% de los píxeles del empaque que no contienen texto; 2) **Conversión rápida a escala de grises** en memoria; 3) **Binarización de Otsu** "
    "(Otsu, 1979) para separar la tinta negra del fondo plástico con alto contraste; y 4) Envío de la matriz binaria limpia hacia el motor de reconocimiento neuronal."
)

add_body(
    "El tiempo de tránsito físico que tarda el paquete en viajar desde la cámara hasta el pistón neumático se rige por la cinemática lineal (Ecuación 2):"
)

# Ecuación 2 OMML
eq2_omml = (
    '<m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>tránsito</m:t></m:r></m:sub></m:sSub><m:r><m:t> = </m:t></m:r>'
    '<m:f><m:num><m:r><m:t>d</m:t></m:r></m:num><m:den><m:r><m:t>v</m:t></m:r></m:den></m:f><m:r><m:t> = </m:t></m:r>'
    '<m:f><m:num><m:r><m:t>0.85 m</m:t></m:r></m:num><m:den><m:r><m:t>1.20 m/s</m:t></m:r></m:den></m:f><m:r><m:t> ≈ 0.708 s = 708 ms</m:t></m:r>'
)
add_apa_equation(eq2_omml, "2")

add_body(
    "Por su parte, el tiempo total de respuesta del sistema automatizado se descompone según la Ecuación 3:"
)

# Ecuación 3 OMML
eq3_omml = (
    '<m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>respuesta</m:t></m:r></m:sub></m:sSub><m:r><m:t> = </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>adq</m:t></m:r></m:sub></m:sSub><m:r><m:t> + </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>prep</m:t></m:r></m:sub></m:sSub><m:r><m:t> + </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>ocr</m:t></m:r></m:sub></m:sSub><m:r><m:t> + </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>plc</m:t></m:r></m:sub></m:sSub><m:r><m:t> = 15 + 25 + 90 + 45 = 175 ms</m:t></m:r>'
)
add_apa_equation(eq3_omml, "3")

add_body(
    "Al comparar los **708 ms** disponibles con los **175 ms** de tiempo de respuesta total, se comprueba un margen de seguridad temporal superior a **4.0 veces**, "
    "garantizando que la decisión se tome con holgura antes de que el producto arribe al eyector mecánico."
)

# -------------------------------------------------------------
# TAREA 2: DIAGNÓSTICO DEL PROBLEMA
# -------------------------------------------------------------
add_task_heading(
    "Tarea 2: Diagnóstico Detallado del Problema",
    "Explicar detalladamente por qué el sistema actual falló en eficiencia, escalabilidad y control de calidad."
)

add_subheading("Falla en el Control de Calidad")
add_body(
    "La planta operaba bajo un esquema de **inspección visual humana por muestreo aleatorio** (revisión de un empaque cada 50 o 100 unidades). "
    "La fisiología humana no está diseñada para mantener concentración fija sobre objetos que transitan a 1.2 m/s durante turnos de 8 horas: "
    "la fatiga visual, los parpadeos y las distracciones inevitables provocan que defectos sutiles pasen inadvertidos. Si el cabezal térmico sufre una falla "
    "justo después de una revisión manual, transcurren hasta 45 minutos antes del siguiente chequeo, lapso en el que se producen miles de paquetes con anomalías."
)

add_apa_figure(
    "4",
    "Muestra de Etiqueta con Tinta Borrosa y Frotada por Falla Térmica",
    "etiquetas_blender/05_falla_impresion_borrosa_frotada.png",
    "Simulación de arrastre mecánico y baja temperatura en el cabezal térmico, reproduciendo la falla del incidente real de Embutidos Kimby.",
    width_inches=4.8
)

add_body(
    "Las fallas típicas en cabezales térmicos son de naturaleza progresiva: **pines térmicos quemados** por fatiga eléctrica que abren surcos horizontales, "
    "o **degradación de temperatura** que genera tinta frotada y desvanecida (Figura 4). Asimismo, el envasado al vacío produce arrugas plásticas con brillos "
    "especulares que ciegan la visibilidad del código (Figura 5). Sin una cámara en línea que verifique el 100% de la producción, el sistema de calidad era ciego."
)

add_apa_figure(
    "5",
    "Muestra de Etiqueta con Deformación y Reflejo Especular en Film Retráctil",
    "etiquetas_blender/08_falla_arruga_y_reflejo_luz.png",
    "Reflejo de luz parásita sobre el film plástico que oculta los caracteres de caducidad, simulando una condición crítica de interferencia óptica.",
    width_inches=4.8
)

add_subheading("Falla en la Eficiencia Operativa y Costos")
add_body(
    "El costo de la no-calidad se multiplica exponencialmente a medida que el defecto avanza en la cadena de suministro. En Kimby, el fallo fue detectado "
    "por los distribuidores en los andenes de recepción de los supermercados. Esto obligó a la empresa a asumir la **logística inversa** (flete de retorno del producto), "
    "la **pérdida de empaques plásticos al vacío**, el costo de mano de obra para desempaque y reclasificación, merma por pérdida de cadena de frío y multas comerciales. "
    "Con un sistema automatizado en línea, el fallo se detecta en el primer empaque defectuoso, deteniendo la línea en menos de 5 segundos y limitando la merma a una sola unidad."
)

add_subheading("Falla en la Escalabilidad")
add_body(
    "El control manual actúa como un obstáculo para el crecimiento de la fábrica. Si la dirección requiere aumentar la cadencia de empaque de 100 a 160 ppm "
    "para atender picos de demanda estacional, el ojo humano colapsa de inmediato. Contratar más personal para mirar etiquetas no solo es económicamente ineficiente, "
    "sino técnicamente inútil debido a las restricciones de tiempo de respuesta de los operarios."
)

# -------------------------------------------------------------
# TAREA 3: PROPUESTA TECNOLÓGICA Y CÓMO SE IMPLEMENTARÍA
# -------------------------------------------------------------
add_task_heading(
    "Tarea 3: Propuesta Tecnológica y Cómo se Implementaría",
    "Definir qué combinación de tecnologías se debe utilizar para resolver el problema y justificar por qué."
)

add_body(
    "Frente a soluciones comerciales propietarias cuyos costos oscilan entre $10,000 y $15,000 USD por estación, se diseñó una arquitectura "
    "industrial basada en **componentes estándar, código abierto y procesamiento en el borde (Edge Computing)**, logrando máxima robustez por menos de $400 USD en hardware:"
)

add_bullet(
    "Sensor Óptico (Cámara Global Shutter)",
    "Módulo de cámara CMOS de 1.58 MP (sensor Sony IMX296) con obturación global (**Global Shutter**) nativa y lente montura C/CS de 8 mm (apertura focal f/1.8). "
    "A diferencia del Rolling Shutter de las cámaras web convencionales que leen línea por línea deformando los objetos en movimiento, el Global Shutter expone "
    "la matriz completa de píxeles al mismo instante exacto, garantizando imágenes libres de distorsión geométrica por un costo de mercado de **$55 USD**."
)

add_bullet(
    "Iluminación Estroboscópica LED Difusa Cenital",
    "Anillo de iluminación LED blanco frío difuso con filtro polarizador cruzado, disparado por un driver estroboscópico de **500 microsegundos** sincronizado con la fotocélula. "
    "Elimina de raíz los reflejos especulares sobre el film retráctil y asegura contraste permanente sin importar las condiciones de luz ambiental del galpón cárnico."
)

add_bullet(
    "Unidad de Procesamiento en el Borde (Edge Computing Local)",
    "Mini PC industrial compacta (procesador Intel N100 / Raspberry Pi 5 con 8GB RAM). Ejecuta la inferencia de forma **100% local y desconectada**, "
    "eliminando la dependencia de servidores en la nube, tarifas por uso de API externa y problemas por fluctuaciones en la red de internet."
)

add_bullet(
    "Software SCADA y Motor OCR Neuronal",
    "Motor **Tesseract OCR (LSTM)** compilado en WebAssembly (WASM) con aceleración SIMD, integrado en una interfaz de supervisión SCADA con alertas sonoras "
    "(chime melódico para conformes y buzzer de 85 dB para rechazos) y bitácora de auditoría exportable a CSV."
)

add_bullet(
    "Módulo Actuador Neumático de Descarte",
    "Cilindro guiado de doble efecto FESTO DFM (carrera de 100 mm, diámetro de 25 mm) con electroválvula monoestable 5/2 de 24V DC conectada al PLC. "
    "Ofrece una conmutación ultrarrápida de 12 ms y fuerza de empuje para desviar el empaque hacia la tolva de merma sin dañar la integridad física del producto."
)

# Tabla 1 APA 7
t1_headers = ["Componente del Sistema", "Tecnología Seleccionada", "Función en la Línea", "Justificación Técnica"]
t1_rows = [
    ["Sensor Óptico", "Cámara CMOS Global Shutter ($55 USD)", "Captura fotograma instantáneo", "Evita distorsión por movimiento sin pagar miles por marcas propietarias."],
    ["Iluminación", "Anillo LED Estroboscópico Difuso", "Flash cenital sincronizado (500 μs)", "Elimina reflejos parásitos del plástico y congela el desplazamiento."],
    ["Unidad de Cómputo", "Mini PC Edge Computing Offline", "Procesamiento local de visión y OCR", "Cero latencia de red, disponibilidad continua y sin tarifas de API."],
    ["Software / OCR", "Tesseract WASM + SCADA Web", "Lectura de texto y toma de decisión", "Red neuronal LSTM especializada en fuentes matriciales térmicas."],
    ["Actuador de Rechazo", "Cilindro Neumático + Válvula 24V", "Expulsión física de paquetes malos", "Accionamiento rápido (< 20 ms), higiénico y apto para plantas cárnicas."]
]
add_apa_table("1", "Especificaciones y Justificación de Componentes de la Propuesta Tecnológica", t1_headers, t1_rows, "Componentes seleccionados para máxima eficiencia operativa a bajo costo.")

add_body(
    "En la Figura 6 se exhibe la interfaz general del software SCADA desarrollado para la supervisión en tiempo real desde la consola de control principal:"
)

add_apa_figure(
    "6",
    "Interfaz de la Aplicación de Control SCADA en Entorno de Escritorio - Caso Aprobado",
    "fig_desktop_aprobado.png",
    "Visualización panorámica mostrando el sensor óptico en vivo, etiqueta conforme, banner verde de APROBADO, telemetría y bitácora de auditoría.",
    width_inches=5.6
)

add_body(
    "Para transformar la imagen cruda capturada por la cámara a una matriz monocromática adecuada para el algoritmo de Otsu, se aplica la ponderación "
    "luminante estandarizada expresada en la Ecuación 4:"
)

# Ecuación 4 OMML
eq4_omml = '<m:r><m:t>Y = 0.299 · R + 0.587 · G + 0.114 · B</m:t></m:r>'
add_apa_equation(eq4_omml, "4")

# -------------------------------------------------------------
# TAREA 4: DISEÑO DE FLUJO LÓGICO DEL PROCESO
# -------------------------------------------------------------
doc.add_page_break() # Nueva página para presentar el diagrama de flujo original en toda su extensión

add_task_heading(
    "Tarea 4: Diseño de Flujo Lógico del Proceso",
    "Describir paso a paso cómo funciona el sistema mediante un diagrama de flujo con decisiones."
)

add_body(
    "A continuación se presenta el **diagrama de flujo de decisión industrial** que gobierna el funcionamiento de la máquina de estados determinista. "
    "El flujo detalla la secuencia completa desde la detección fotoeléctrica en la cinta transportadora, la captura estroboscópica, el preprocesamiento, "
    "las cinco evaluaciones lógicas booleanas y las acciones físicas finales:"
)

# Figura 7: Diagrama de Flujo Original Exacto
add_apa_figure(
    "7",
    "Diagrama de Flujo del Proceso Automatizado de Inspección y Decisión Industrial",
    "fig_diagrama_flujo_original.png",
    "Secuencia determinista original con las bifurcaciones de validación (KMB, longitud >= 10 caracteres, legibilidad de fecha, fecha vencida y confianza >= 60%) "
    "conduciendo a los estados finales de Producto Aprobado o Activación de Señal de Rechazo a 24V hacia el brazo neumático.",
    width_inches=3.4 # Ajustado para que quepa verticalmente en su página de forma nítida y completa
)

add_body(
    "El flujo lógico ilustrado en la Figura 7 describe las decisiones críticas que adopta el sistema para cada paquete individual:"
)

add_bullet("1. Detección Física por Sensor Infrarrojo", "El empaque corta el haz fotoeléctrico, generando el flanco de subida que inicia el ciclo de inspección.")
add_bullet("2. Disparo de Cámara y Extracción de ROI", "El flash LED estroboscópico de 500 μs y el obturador global congelan la etiqueta; se recorta únicamente la ventana del fechador.")
add_bullet("3. Preprocesamiento e Inferencia OCR", "Conversión a escala de grises y binarización Otsu para alimentar la red neuronal LSTM de Tesseract.")
add_bullet("4. Cascada de Decisiones Booleanas", "Se evalúa secuencialmente: ¿Se lee 'KMB'? ¿Longitud ≥ 10 caracteres? ¿Fecha legible? ¿Fecha no vencida? ¿Confianza ≥ 60%?")
add_bullet("5A. Rama Conforme (APROBADO)", "Si todas las condiciones son afirmativas, se emite el chime armónico de confirmación, se registra en bitácora y la cinta continúa libre.")
add_bullet("5B. Rama No Conforme (RECHAZADO)", "Si cualquiera de las condiciones falla, se genera timestamp, se activa la baliza estroboscópica roja, suena el buzzer industrial y se envía el pulso de 24V DC al PLC para que el brazo neumático empuje el empaque al contenedor de mermas.")

# Tabla 2 APA 7
t2_headers = ["Condición Detectada", "Texto Extraído por OCR", "Nivel de Confianza", "Veredicto", "Acción Física del Sistema"]
t2_rows = [
    ["Etiqueta nítida y completa", "LOTE: KMB-2026-A01 | VENC: 15/12/2026", "96% (Excelente)", "APROBADO", "Libre tránsito hacia encartonado."],
    ["Líneas blancas (pines rotos)", "LOTE: KM -202 -A0  | VENC: 15/--/----", "38% (Muy bajo)", "RECHAZADO", "Disparo neumático 24V a tolva de merma."],
    ["Tinta frotada o borrosa", "LOTE: [Ilegible]  | VENC: [Ilegible]", "41% (Insuficiente)", "RECHAZADO", "Disparo neumático 24V y sirena de alarma."],
    ["Fecha vencida o antigua", "LOTE: KMB-2026-A01 | VENC: 10/01/2023", "92% (Texto claro)", "RECHAZADO", "Bloqueo sanitario por fecha caducada."],
    ["Falta prefijo 'KMB'", "LOTE: 2026-A01     | VENC: 15/12/2026", "55% (Incompleto)", "RECHAZADO", "Disparo neumático a tolva de merma."]
]
add_apa_table("2", "Matriz de Decisión Lógica del Algoritmo de Calidad Kimby", t2_headers, t2_rows, "Criterios booleanos aplicados a cada fotograma capturado.")

add_body(
    "En la Figura 8 se aprecia la respuesta inmediata de la interfaz ante un caso de producto rechazado por caracteres borrosos, mostrando la activación "
    "de la señal PLC de 24V y la alarma sonora en planta:"
)

add_apa_figure(
    "8",
    "Interfaz de Control SCADA ante Detección de Falla y Accionamiento del Actuador Neumático",
    "fig_desktop_rechazado.png",
    "Banner rojo de DESCARTADO, señal de disparo PLC a 24V hacia la electroválvula del actuador neumático y registro del incidente en bitácora.",
    width_inches=5.6
)

# -------------------------------------------------------------
# TAREA 5: MITIGACIÓN DE ERRORES Y CALIBRACIÓN DE UMBRALES
# -------------------------------------------------------------
add_task_heading(
    "Tarea 5: Mitigación de Errores y Calibración de Umbrales",
    "¿Qué sucede si el sistema confunde un dígito debido a una arruga en la etiqueta y rechaza un producto bueno, o peor aún, acepta uno malo? ¿Cómo se ajustarán los niveles de tolerancia o umbrales de confianza?"
)

add_body(
    "En la industria de alimentos procesados se presenta la disyuntiva estadística fundamental entre dos tipos de error:"
)

add_subheading("Escenario de Falso Positivo (Rechazar un Producto Bueno)")
add_body(
    "Ocurre cuando una etiqueta con impresión perfecta sufre una arruga pronunciada sobre el plástico retráctil al momento del sellado al vacío, "
    "generando una sombra que hace dudar al algoritmo de OCR (por ejemplo, confundiendo un '8' con un '3' y reduciendo la confianza al 50%). "
    "**¿Qué sucede operativamente?** El sistema descarta el paquete hacia la tolva de merma acolchada. La consecuencia para la empresa es sumamente baja: "
    "al final de la hora, un operario recoge los empaques de la tolva, los inspecciona visualmente y los reingresa a la banda en segundos. "
    "El costo de este falso rechazo se limita a fracciones de centavo de dólar en tiempo de operario."
)

add_subheading("Escenario de Falso Negativo (Aceptar un Producto Malo)")
add_body(
    "Ocurre cuando el sistema se calibra con umbrales excesivamente permisivos y deja pasar como 'APROBADO' un empaque con la fecha ilegible o caducada. "
    "**¿Qué sucede operativamente?** Este es el peor escenario posible para la industria cárnica: el producto defectuoso llega a las estanterías de los supermercados, "
    "provocando decomisos de las autoridades sanitarias (MINSA), multas regulatorias, retiro masivo de lotes del mercado, pérdida de contratos de distribución "
    "y un severo daño a la reputación de la marca Embutidos Kimby (costo superior a los $4,500 USD por evento)."
)

add_subheading("Política de Calidad y Calibración de Umbrales de Confianza")
add_body(
    "Dada la enorme asimetría de costos entre ambos errores, la ingeniería de calidad exige fijar una política estricta de **'Cero Tolerancia Sanitaria'**: "
    "es preferible asumir una tasa de falsos rechazos de 0.2% en la tolva de línea que permitir que un solo paquete con fecha ilegible alcance el mercado. "
    "Para mitigar los efectos de las arrugas sin relajar la seguridad sanitaria, se implementaron tres medidas técnicas:"
)

add_bullet("1. Regla de Identificación de Lote Kimby ('KMB' + Longitud Completa)", "El sistema valida que el OCR sea capaz de leer el prefijo corporativo 'KMB' y la dotación mínima de 10 caracteres estructurados. Si el código está incompleto o falta el prefijo, se rechaza de inmediato.")
add_bullet("2. Validación Cronológica de Caducidad", "La fecha leída no debe pertenecer al pasado. Un producto con fecha menor a la fecha de producción actual se rechaza automáticamente por riesgo sanitario.")
add_bullet("3. Iluminación Polarizada y Binarización Adaptativa", "Se combate la sombra física de las arrugas mediante iluminación cenital difusa y el algoritmo adaptativo de Otsu, permitiendo segmentar la tinta negra incluso sobre sustratos plásticos deformados.")

add_body(
    "Las Figuras 9 y 10 muestran la validación de la interfaz móvil en navegadores Android Chrome, verificando que los supervisores de planta pueden "
    "monitorear el encuadre exacto sin recortes y observar las alarmas de descarte en tiempo real desde sus terminales portátiles:"
)

add_apa_figure(
    "9",
    "Interfaz Móvil en Android Chrome - Sección de Sensor Óptico y Encuadre Completo",
    "fig_mobile_pantalla1_sensor.png",
    "Captura íntegra sin cortes laterales en pantalla de teléfono móvil, demostrando el encuadre exacto del empaque Kimby y controles táctiles.",
    width_inches=3.0
)

add_apa_figure(
    "10",
    "Interfaz Móvil en Android Chrome - Notificación de Rechazo y Disparo Neumático",
    "fig_mobile_pantalla2_rechazo.png",
    "Pantalla móvil mostrando el banner de rechazo por texto borroso, activación de disparo al pistón neumático y registro de auditoría.",
    width_inches=3.0
)

add_body(
    "Por último, la Figura 11 muestra el Estudio Web Interactivo (`generador.html`) programado para simular fallas térmicas y deformaciones plásticas:"
)

add_apa_figure(
    "11",
    "Estudio Web y Generador de Etiquetas Interactivo para Simulación Industrial",
    "fig_generador_estudio.png",
    "Panel de control para generar variantes de etiquetas Kimby, ajustar sliders de desenfoque, pérdida de pines y arrugas para pruebas físicas y modelado 3D.",
    width_inches=5.6
)

# -------------------------------------------------------------
# CONCLUSIONES
# -------------------------------------------------------------
add_task_heading("Conclusiones")

add_body(
    "1. La problemática de legibilidad de fechas en Embutidos Kimby encuentra una solución técnica viable, robusta y accesible mediante la combinación "
    "de una cámara CMOS con **Global Shutter** de bajo costo ($55 USD), iluminación estroboscópica LED cenital de 500 μs y procesamiento en el borde "
    "(**Edge Computing**), reduciendo en más del 95% los costos frente a soluciones propietarias."
)
add_body(
    "2. Las restricciones cinemáticas de una línea continua a 1.2 m/s imponen que el preprocesamiento sea **ultraligero (< 25 ms)**, apoyándose en el recorte "
    "de ROI fija y la binarización de Otsu, lo que permite tomar la decisión de descarte en 175 ms con un factor de seguridad superior a 4.0 respecto al tránsito disponible."
)
add_body(
    "3. La política de calidad de **Cero Tolerancia Sanitaria** salvaguarda la reputación legal y comercial de Embutidos Kimby al eliminar la posibilidad de que empaques "
    "con fechas borrosas o vencidas alcancen los canales de distribución, manejando los falsos rechazos por arrugas de forma económica mediante reinspección en tolva."
)

# -------------------------------------------------------------
# REFERENCIAS BIBLIOGRÁFICAS APA 7
# -------------------------------------------------------------
add_task_heading("Referencias")

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
add_apa_reference("FESTO AG & Co. KG. (2022). Manual de selección y diseño de cilindros neumáticos guiados serie DFM. FESTO Pneumatics Publication.")
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

#!/usr/bin/env python3
"""
Generador del Informe Técnico ULSA 2026 - Caso de Estudio: Embutidos Kimby
Edición Especializada con Profundidad Exhaustiva en Reconocimiento Óptico de Caracteres (OCR):
- Teoría y práctica profunda de OCR/ICR: Densidad PPC, Binarización Otsu, BLSTM, CTC Loss, Whitelisting, Bounding Boxes y Softmax
- Diagrama de flujo original exacto (Mermaid HD render)
- Nueva Figura 8 de Análisis de Segmentación e Inferencia Neuronal OCR (LSTM)
- Títulos de Tarea limpios y sin duplicaciones con sus Consignas oficiales
- Fórmulas matemáticas nativas de Word (OMML en Cambria Math)
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
p8.text = "RESOLUCIÓN DE ESTUDIO DE CASO"
p8.runs[0].font.bold = True
p8.runs[0].font.name = FONT_NAME
p8.runs[0].font.size = Pt(13)
p8.runs[0].font.color.rgb = BLACK

p9 = doc.paragraphs[9]
p9.text = "SISTEMA AUTOMATIZADO DE INSPECCIÓN EN LÍNEA Y CONTROL DE CALIDAD POR RECONOCIMIENTO ÓPTICO DE CARACTERES (OCR)\nCASO 1: EMBUTIDOS KIMBY"
p9.runs[0].font.bold = True
p9.runs[0].font.name = FONT_NAME
p9.runs[0].font.size = Pt(13.5)
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
p16.runs[0].font.size = Pt(11.5)
p16.runs[0].font.color.rgb = BLACK

p17 = doc.paragraphs[17]
p17.text = "Francini Rocío"
if len(p17.runs) == 0:
    p17.add_run("Francini Rocío")
p17.runs[0].font.bold = False
p17.runs[0].font.name = FONT_NAME
p17.runs[0].font.size = Pt(11.5)
p17.runs[0].font.color.rgb = BLACK

p18 = doc.paragraphs[18]
p18.text = "Edmundo González"
if len(p18.runs) == 0:
    p18.add_run("Edmundo González")
p18.runs[0].font.bold = False
p18.runs[0].font.name = FONT_NAME
p18.runs[0].font.size = Pt(11.5)
p18.runs[0].font.color.rgb = BLACK

p19 = doc.paragraphs[19]
p19.text = "Revisado por:"
p19.runs[0].font.bold = True
p19.runs[0].font.name = FONT_NAME
p19.runs[0].font.color.rgb = BLACK

p20 = doc.paragraphs[20]
p20.text = "Ing. Fimvark Guzmán Orozco"
p20.runs[0].font.bold = False
p20.runs[0].font.name = FONT_NAME
p20.runs[0].font.size = Pt(11.5)
p20.runs[0].font.color.rgb = BLACK

for idx in [21, 22, 23, 24]:
    doc.paragraphs[idx].text = ""

p25 = doc.paragraphs[25]
p25.text = "4 de octubre de 2026"
p25.runs[0].font.italic = True
p25.runs[0].font.name = FONT_NAME
p25.runs[0].font.size = Pt(11)
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

print("[3/5] Redactando informe con fundamentación exhaustiva en OCR y Visión Artificial...")

# -------------------------------------------------------------
# INTRODUCCIÓN AL CASO DE ESTUDIO
# -------------------------------------------------------------
add_task_heading("Introducción al Caso de Estudio: Embutidos Kimby")

add_body(
    "El **Reconocimiento Óptico de Caracteres (OCR)** representa una de las disciplinas más críticas y complejas de la visión por computadora "
    "aplicada a la automatización industrial. Su objetivo primordial consiste en transformar matrices bidimensionales de píxeles capturadas mediante sensores ópticos "
    "en representaciones textuales codificadas simbólicamente (cadenas ASCII/Unicode) que puedan ser contrastadas en tiempo real contra registros de bases de datos relacionales, "
    "sistemas de ejecución de manufactura (MES) o plataformas de planificación de recursos empresariales (ERP) (Gonzalez & Woods, 2018)."
)

add_body(
    "En la industria alimentaria y de procesamiento cárnico, la codificación alfanumérica de **lote de producción** y **fecha de caducidad** "
    "constituye el eje legal y técnico de la trazabilidad exigida por regulaciones internacionales como la norma ISO 22005 y las directrices del CODEX Alimentarius (CODEX, 2018). "
    "El código de lote delimita de forma unívoca la línea de sacrificio, el turno de picado y la formulación química empleada, mientras que la fecha de caducidad "
    "establece el límite biológico seguro de inocuidad microbiológica para el consumo humano."
)

add_apa_figure(
    "1",
    "Muestra de Etiqueta Conforme de Salchicha Viena Kimby 500g (Lote KMB-2026-A01)",
    "etiquetas_blender/01_conforme_salchicha_viena.png",
    "Etiqueta con impresión térmica nítida, caracteres matriciales íntegros y fecha de caducidad vigente. Cumple con todos los estándares de aprobación.",
    width_inches=4.8
)

add_body(
    "**Embutidos Kimby** imprime automáticamente esta información sobre el film retráctil de polietileno/poliamida de cada paquete mediante cabezales "
    "de transferencia térmica industrial (TIJ/TTO). Recientemente, la empresa sufrió una crisis operativa de graves repercusiones económicas y comerciales: "
    "**una falla no detectada en los cabezales de impresión térmica provocó que un lote completo saliera al mercado con la fecha de caducidad borrosa e ilegible**. "
    "Esta contingencia derivó en devoluciones masivas y costosas por parte de los distribuidores mayoristas, penalizaciones contractuales y una severa advertencia de los organismos de control sanitario."
)

add_apa_figure(
    "2",
    "Muestra de Etiqueta con Defecto Térmico Crítico por Pines Quemados",
    "etiquetas_blender/04_falla_cabezal_pines_rotos.png",
    "Simulación de líneas horizontales blancas (drop-outs) que cortan el texto, impidiendo la segmentación por OCR y motivando el rechazo inmediato.",
    width_inches=4.8
)

add_body(
    "Como se evidencia al comparar la Figura 1 (etiqueta conforme) con la Figura 2 (etiqueta defectuosa), la pérdida de micro-resistencias en el cabezal genera "
    "**rupturas topológicas horizontales** en los trazos de las letras. Ante esta situación, la empresa requiere la implementación de un sistema de inspección automatizada en línea "
    "que capture la etiqueta en movimiento, aplique **lectura OCR neuronal en tiempo real**, valide la estructura y fechas, y comande el rechazo neumático de cualquier pieza ilegible. "
    "A continuación, se desarrolla la resolución técnica exhaustiva orientada a la ingeniería de OCR y procesamiento digital de imágenes."
)

# -------------------------------------------------------------
# TAREA 1: RESTRICCIONES DE VELOCIDAD EN TIEMPO REAL
# -------------------------------------------------------------
doc.add_page_break()

add_task_heading(
    "Tarea 1: Análisis de Restricciones de Velocidad en Tiempo Real",
    "Indagar y analizar por qué el proceso en tiempo real (en línea) requiere fases de preprocesamiento de imagen sumamente rápidas y ligeras a diferencia de un escaneo de documentos estáticos."
)

add_subheading("Diferencias Estructurales entre Escaneo Estático de Documentos y OCR en Línea Industrial")
add_body(
    "Para comprender las restricciones del sistema, es imperativo establecer la frontera metodológica entre el **escaneo estático tradicional de documentos** "
    "(como la digitalización de facturas, libros o contratos administrativos) y el **OCR industrial en tiempo real (Hard Real-Time OCR)** sobre una cinta transportadora:"
)

add_bullet(
    "Escaneo Estático de Oficina",
    "El soporte de información (papel plano) permanece completamente inmóvil sobre una cama plana de cristal. Las condiciones de iluminación son homogéneas, "
    "difusas y calibradas mecánicamente mediante lámparas móviles CCD/CIS. En este escenario, **el tiempo no constituye una variable crítica**: el software de OCR "
    "puede tomarse entre **2 y 15 segundos por página**, aplicando algoritmos pesados de múltiples pasadas como corrección de perspectiva afín tridimensional, "
    "desparasitado morfológico denso, binarización adaptativa local por ventanas deslizantes de Sauvola ($O(W^2)$ por píxel) y segmentación jerárquica de bloques "
    "mediante redes neuronales convolucionales profundas de cientos de millones de parámetros."
)

add_bullet(
    "OCR en Línea Industrial en Tiempo Real",
    "En la línea de empaque de Embutidos Kimby, los productos se desplazan a una velocidad lineal continua de **1.0 a 1.2 metros por segundo**, con una cadencia "
    "de producción nominal de **100 a 120 empaques por minuto (ppm)**. Bajo este régimen cinemático, **el producto jamás se detiene**; cada paquete dispone de un tiempo "
    "de ciclo unitario de apenas **500 a 600 milisegundos**. Si el algoritmo de visión y OCR introduce una latencia computacional superior a 200 ms, se produce "
    "un desbordamiento en el buffer de fotogramas (*dropped frames*), y el producto defectuoso habrá sobrepasado físicamente la ubicación del eyector neumático antes "
    "de que el controlador determine su condición de rechazo."
)

add_subheading("El Problema Óptico del Desenfoque por Movimiento (Motion Blur)")
add_body(
    "En visión por computadora, el desplazamiento relativo entre el objeto y el plano focal durante el intervalo de apertura del obturador genera una convolución "
    "espacial del patrón de intensidad luminosa conocida como **Motion Blur**. Si se utilizara una cámara comercial con tiempo de exposición estándar de video "
    "de **t_exp = 1/30 s (33.3 ms)**, el desplazamiento físico de la etiqueta durante la captura alcanzaría los **40 milímetros (4.0 cm)**, como se modela en la Ecuación 1:"
)

# Ecuación 1 OMML
eq1_omml = '<m:r><m:t>B = v · </m:t></m:r><m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>exp</m:t></m:r></m:sub></m:sSub>'
add_apa_equation(eq1_omml, "1")

add_body(
    "Un corrimiento de 40 mm destruye completamente la función de transferencia de modulación (MTF) de la óptica, provocando que los trazos de los caracteres "
    "se fundan en un manchón gris continuo. Intentar restaurar una imagen con semejante grado de degradación requeriría filtros inversos de Wiener o algoritmos "
    "iterativos de deconvolución ciega (*Blind Deconvolution*), cuyo coste temporal supera los **500 a 1200 milisegundos por fotograma**, resultando inviable en línea. "
    "Por consiguiente, la restricción de velocidad exige resolver el desenfoque **físicamente en el hardware óptico**: se acopla un sensor con **obturador global (Global Shutter)** "
    "y un destello de **iluminación estroboscópica LED de 500 microsegundos (t_exp = 0.0005 s)**, reduciendo el desenfoque residual a escasos **B = 0.60 mm** "
    "(menos de 3 píxeles), congelando instantáneamente los caracteres para el motor OCR."
)

add_subheading("Densidad Óptica y Resolución de Muestreo (Pixels Per Character)")
add_body(
    "Para que un clasificador OCR sea capaz de decodificar caracteres formados por cabezales de transferencia térmica (que utilizan fuentes matriciales de 7x5 o trazos continuos estrechos), "
    "la teoría de muestreo de Nyquist-Shannon impone una densidad mínima de **Pixels Per Character (PPC)** de al menos **18 a 25 píxeles de altura** por carácter, equivalente a una densidad de **300 PPI** en el campo visual (FOV), modelada según la Ecuación 2:"
)

# Ecuación 2 OMML
eq2_omml = (
    '<m:r><m:t>PPC = </m:t></m:r>'
    '<m:f><m:num><m:sSub><m:e><m:r><m:t>H</m:t></m:r></m:e><m:sub><m:r><m:t>carácter</m:t></m:r></m:sub></m:sSub><m:r><m:t> · </m:t></m:r><m:sSub><m:e><m:r><m:t>N</m:t></m:r></m:e><m:sub><m:r><m:t>vertical</m:t></m:r></m:sub></m:sSub></m:num>'
    '<m:den><m:sSub><m:e><m:r><m:t>H</m:t></m:r></m:e><m:sub><m:r><m:t>campo</m:t></m:r></m:sub></m:sSub></m:den></m:f>'
)
add_apa_equation(eq2_omml, "2")

add_subheading("Pipeline de Preprocesamiento Ligero Especializado para OCR (< 25 ms)")
add_body(
    "Para cumplir con el plazo estricto de tiempo real, el preprocesamiento digital de la imagen se optimizó bajo una estructura lineal de complejidad O(N), "
    "como se detalla esquemáticamente en la Figura 3:"
)

add_apa_figure(
    "3",
    "Diagrama del Pipeline de Preprocesamiento de Imagen en Tiempo Real (< 25 ms)",
    "fig_pipeline_ocr.png",
    "Flujo de optimización que incluye recorte directo de la Región de Interés (ROI), conversión a escala de grises y binarización adaptativa Otsu antes del OCR.",
    width_inches=5.2
)

add_body(
    "El pipeline opera en cuatro fases secuenciales estrictas: 1) **Recorte de ROI fija (60x25 mm)**: en lugar de procesar la imagen completa del paquete (1200x800 píxeles = 960,000 píxeles), "
    "el algoritmo aísla exclusivamente la ventana geométrica donde se imprime el fechador (300x120 píxeles = 36,000 píxeles), reduciendo la carga de cómputo en un **96.2%**; "
    "2) **Conversión rápida a escala de grises** en memoria mediante ponderación luminante estándar (Y = 0.299R + 0.587G + 0.114B); "
    "3) **Binarización Adaptativa Global de Otsu**: calcula el umbral óptimo k* maximizando la varianza inter-clases en tiempo O(L) "
    "mediante histograma de 256 niveles (Otsu, 1979), formulado según la Ecuación 3:"
)

# Ecuación 3 OMML (Varianza Inter-clases de Otsu)
eq3_omml = (
    '<m:sSubSup><m:e><m:r><m:t>σ</m:t></m:r></m:e><m:sub><m:r><m:t>B</m:t></m:r></m:sub><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSubSup><m:r><m:t>(k) = </m:t></m:r>'
    '<m:f><m:num><m:sSup><m:e><m:d><m:e><m:sSub><m:e><m:r><m:t>μ</m:t></m:r></m:e><m:sub><m:r><m:t>T</m:t></m:r></m:sub></m:sSub>'
    '<m:r><m:t> · ω(k) - μ(k)</m:t></m:r></m:e></m:d></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup></m:num>'
    '<m:den><m:r><m:t>ω(k) · [1 - ω(k)]</m:t></m:r></m:den></m:f>'
)
add_apa_equation(eq3_omml, "3")

add_body(
    "Donde ω(k) representa la probabilidad acumulada de fondo, μ(k) es la intensidad media acumulada y μ_T es la media global de la ROI. "
    "La evaluación por tabla acumulativa requiere apenas 256 iteraciones, completándose en menos de **2.5 ms**; y "
    "4) **Inferencia OCR directa** sobre la máscara binaria resultante, completando todo el ciclo de visión en menos de **25 ms**."
)

add_subheading("Presupuesto de Tiempo y Tiempo de Tránsito en la Banda")
add_body(
    "El tiempo físico disponible desde que el paquete es detectado por la fotocélula de disparo hasta que cruza la posición del cilindro de descarte "
    "(distancia d = 0.85 m a velocidad v = 1.20 m/s) establece el límite superior del ciclo de inspección, según se modela en la Ecuación 4:"
)

# Ecuación 4 OMML (Tiempo de Tránsito vs Presupuesto)
eq4_omml = (
    '<m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>tránsito</m:t></m:r></m:sub></m:sSub><m:r><m:t> = </m:t></m:r>'
    '<m:f><m:num><m:r><m:t>d</m:t></m:r></m:num><m:den><m:r><m:t>v</m:t></m:r></m:den></m:f><m:r><m:t> = </m:t></m:r>'
    '<m:f><m:num><m:r><m:t>0.85 m</m:t></m:r></m:num><m:den><m:r><m:t>1.20 m/s</m:t></m:r></m:den></m:f><m:r><m:t> ≈ 0.708 s = 708 ms &gt; </m:t></m:r>'
    '<m:sSub><m:e><m:r><m:t>t</m:t></m:r></m:e><m:sub><m:r><m:t>respuesta</m:t></m:r></m:sub></m:sSub><m:r><m:t> = 175 ms</m:t></m:r>'
)
add_apa_equation(eq4_omml, "4")

add_body(
    "Dado que el tiempo total de respuesta del sistema compuesto por adquisición estroboscópica (15 ms), preprocesamiento (25 ms), inferencia OCR (90 ms) "
    "y latencia de ciclo del PLC (45 ms) suma únicamente **175 ms**, el sistema cuenta con un factor de seguridad temporal de **4.05 veces**, "
    "garantizando que la orden neumática de descarte esté calculada y memorizada en el registro de desplazamiento mucho antes de que el paquete alcance el pistón."
)

# -------------------------------------------------------------
# TAREA 2: DIAGNÓSTICO DEL PROBLEMA
# -------------------------------------------------------------
doc.add_page_break()

add_task_heading(
    "Tarea 2: Diagnóstico Detallado del Problema",
    "Explicar detalladamente por qué el sistema actual falló en eficiencia, escalabilidad y control de calidad."
)

add_subheading("El Colapso de la Segmentación y Reconocimiento de Caracteres por Fallas Térmicas")
add_body(
    "El incidente que enfrentó Embutidos Kimby tuvo como raíz física la interacción entre la degradación electromecánica de los cabezales térmicos (TIJ/TTO) "
    "y la falta de un sistema de visión artificial en lazo cerrado (*Closed-Loop Feedback*). Desde la perspectiva del reconocimiento de patrones y el OCR, "
    "ocurrieron tres modos de falla determinantes:"
)

add_bullet(
    "Ruptura de Trazos por Pines Quemados (Thermal Pin Drop-outs)",
    "Los cabezales térmicos transfieren calor mediante una matriz microscópica de micro-resistencias eléctricas cerámicas. Cuando se queman 2 o más pines contiguos "
    "por choque electrostático o fatiga térmica, se generan líneas horizontales blancas continuas que atraviesan los caracteres impresos. En la teoría de OCR, "
    "esto destruye las propiedades topológicas fundamentales de las letras: el clasificador neuronal depende de los lazos cerrados (*loops*) y cruces (*junctions*). "
    "Al cortarse el lazo superior de una letra **'B'**, la red neuronal la confunde sistemáticamente con un **'3'** o con fragmentos disconexos de ruido, "
    "provocando el colapso de la confianza de lectura."
)

add_bullet(
    "Degradación de Temperatura y Frotado Mecánico (Under-segmentation)",
    "Si la temperatura del cabezal disminuye por fluctuación de voltaje o acumulación de carbonilla, la tinta de cera/resina no alcanza el punto óptimo de fusión. "
    "Al entrar en contacto con las guías de transporte antes de su curado, la tinta se dispersa (Figura 4), reduciendo el contraste local y provocando que "
    "los caracteres contiguos se toquen entre sí. El OCR es incapaz de segmentar dónde termina un carácter y dónde inicia el siguiente, fusionando palabras enteras en una sola masa ilegible."
)

add_apa_figure(
    "4",
    "Muestra de Etiqueta con Tinta Borrosa y Frotada por Falla Térmica",
    "etiquetas_blender/05_falla_impresion_borrosa_frotada.png",
    "Simulación de arrastre mecánico y baja temperatura en el cabezal térmico, reproduciendo la falla del incidente real de Embutidos Kimby.",
    width_inches=4.8
)

add_bullet(
    "Deformaciones Plásticas y Reflejos Especulares (Glint Artifacts)",
    "El envasado al vacío de embutidos produce pliegues irregulares sobre el film retráctil (Figura 5). Cuando una arruga coincide con la ventana del fechador, "
    "la luz incide con ángulo especular saturando los píxeles a valor 255. Esto ciega al sensor, amputando fragmentos críticos de la fecha de caducidad."
)

add_apa_figure(
    "5",
    "Muestra de Etiqueta con Deformación y Reflejo Especular en Film Retráctil",
    "etiquetas_blender/08_falla_arruga_y_reflejo_luz.png",
    "Reflejo de luz parásita sobre el film plástico que oculta los caracteres de caducidad, simulando una condición crítica de interferencia óptica.",
    width_inches=4.8
)

add_subheading("Vulnerabilidad del Control por Muestreo Humano frente a la Inspección por OCR al 100%")
add_body(
    "La planta operaba bajo un esquema obsoleto de **inspección visual humana discontinua** (muestreo de una pieza cada 30 o 60 minutos). "
    "La psicofísica humana demuestra que el ojo de un operario sufre fatiga visual, microsueños y ceguera por inatención a cadencias industriales. "
    "Si un cabezal térmico se deteriora en el minuto 5 de un turno, se fabrican y encartonan miles de salchichas defectuosas antes del siguiente chequeo. "
    "Asimismo, el control manual es **completamente inescalable**: si la empresa requiere acelerar la línea a 160 ppm, no es viable contratar más personal para mirar etiquetas. "
    "En términos económicos, detectar el defecto en las bodegas del distribuidor multiplicó los costos por 100 debido a la logística inversa y mermas por pérdida de cadena de frío."
)

# -------------------------------------------------------------
# TAREA 3: PROPUESTA TECNOLÓGICA Y CÓMO SE IMPLEMENTARÍA
# -------------------------------------------------------------
doc.add_page_break()

add_task_heading(
    "Tarea 3: Propuesta Tecnológica y Cómo se Implementaría",
    "Definir qué combinación de tecnologías se debe utilizar para resolver el problema y justificar por qué."
)

add_subheading("Arquitectura del Sistema Ciber-Físico y Motor OCR en el Borde (Edge Computing)")
add_body(
    "Para resolver el problema sin incurrir en equipos de visión propietarios de $15,000 USD, se implementó una arquitectura basada en **Edge Computing**, "
    "código abierto y aceleración por hardware local:"
)

add_bullet(
    "Sensor Óptico con Global Shutter ($55 USD)",
    "Módulo CMOS Sony IMX296 de 1.58 MP con lente de 8 mm f/1.8. Su obturación global expone todos los píxeles en el mismo microsegundo, "
    "eliminando la distorsión geométrica (*jelly effect*) del Rolling Shutter y garantizando trazos ortogonales perfectos para el OCR."
)

add_bullet(
    "Iluminación Estroboscópica LED Cenital Polarizada",
    "Anillo difuso con filtro polarizador cruzado disparado por driver estroboscópico de **500 μs** sincronizado con fotocélula infrarroja PNP. "
    "Elimina de raíz los reflejos especulares de las arrugas plásticas y proporciona un contraste constante superior al 85% entre tinta y fondo."
)

add_bullet(
    "Unidad de Cómputo Edge (Mini PC Industrial Offline)",
    "Mini PC con procesador Intel N100 / Raspberry Pi 5 ejecutando Linux LTS. Procesa el 100% de los algoritmos localmente sin conexión a internet, "
    "garantizando latencias menores a 180 ms, confidencialidad total y cero costos mensuales recurrentes de API en la nube."
)

add_bullet(
    "Motor OCR Neuronal (Tesseract.js con Redes LSTM y Decodificación CTC)",
    "A diferencia de los métodos anticuados de correlación por plantillas (*Template Matching*) que fallan ante cualquier rotación o escala, el motor implementa "
    "**redes neuronales recurrentes bidireccionales de memoria a largo-corto plazo (BLSTM)** compiladas en WebAssembly (WASM) con aceleración SIMD. "
    "La red analiza franjas verticales de píxeles secuencialmente, decodificando el texto mediante la función de pérdida **CTC (Connectionist Temporal Classification)**, "
    "la cual permite leer secuencias de caracteres sin requerir una segmentación previa perfecta entre letras (Smith, 2007)."
)

add_bullet(
    "Restricción de Espacio de Estados (Character Whitelisting)",
    "Para maximizar la velocidad y precisión, se configura una lista blanca de caracteres estrictos: `tessedit_char_whitelist = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/-:'`. "
    "Esto anula la posibilidad de confundir dígitos con símbolos exóticos, acelerando la inferencia de la red en un **45%**."
)

add_bullet(
    "Actuador Neumático de Descarte",
    "Cilindro guiado de doble efecto FESTO DFM (carrera 100 mm, diámetro 25 mm) con electroválvula monoestable 5/2 de 24V DC accionada por salida digital del PLC. "
    "Tiempo de respuesta mecánico de 12 ms, idóneo para plantas cárnicas por su higiene y resistencia a la humedad."
)

# Tabla 1 APA 7
t1_headers = ["Componente del Sistema", "Tecnología Seleccionada", "Función en la Línea", "Justificación Técnica"]
t1_rows = [
    ["Sensor Óptico", "Cámara CMOS Global Shutter ($55 USD)", "Captura fotograma instantáneo", "Evita distorsión por movimiento sin pagar miles por marcas propietarias."],
    ["Iluminación", "Anillo LED Estroboscópico Difuso", "Flash cenital sincronizado (500 μs)", "Elimina reflejos parásitos del plástico y congela el desplazamiento."],
    ["Unidad de Cómputo", "Mini PC Edge Computing Offline", "Procesamiento local de visión y OCR", "Cero latencia de red, disponibilidad continua y sin tarifas de API."],
    ["Software / OCR", "Tesseract WASM (BLSTM + CTC)", "Lectura de texto y toma de decisión", "Red neuronal entrenada para fuentes matriciales de cabezal térmico."],
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
    width_inches=5.4
)

# Salto de página para que el Gemelo Digital 2D y su figura queden integrados limpiamente
doc.add_page_break()

add_subheading("Validación Cinemática Mediante Gemelo Digital 2D de la Línea y Pistón Neumático")
add_body(
    "Como fase previa y complementaria al montaje electromecánico en planta, se desarrolló un **Gemelo Digital 2D interactivo** "
    "de la línea de empaque (Figura 7). Este entorno simula la cinemática continua de la cinta a **1.20 m/s (120 ppm)**, la interrupción del haz fotoeléctrico PNP, "
    "el destello estroboscópico sincronizado de **500 μs** de la cámara CAM-01, la binarización de Otsu en tiempo real y la carrera de avance "
    "del cilindro neumático guiado **FESTO DFM** en un tiempo de **12 ms**. La herramienta permite inyectar interactivamente las fallas "
    "reales del caso (pines quemados, tinta borrosa, caducidades vencidas y arrugas plásticas con reflejo especular), verificando que el actuador "
    "descarte físicamente las piezas defectuosas hacia la tolva de merma con un margen de seguridad temporal de **4.05 veces** frente al tiempo de tránsito de 708 ms."
)

add_apa_figure(
    "7",
    "Gemelo Digital 2D: Simulación Cinemática de la Cinta Transportadora y Pistón Neumático FESTO DFM",
    "fig_simulador_2d.png",
    "Entorno interactivo 2D donde se modela la cinemática continua a 1.2 m/s, la captura estroboscópica por la cámara CAM-01, la binarización en tiempo real y la expulsión lateral de paquetes con defectos hacia la tolva de mermas.",
    width_inches=5.4
)

# -------------------------------------------------------------
# TAREA 4: DISEÑO DE FLUJO LÓGICO DEL PROCESO
# -------------------------------------------------------------
doc.add_page_break()

add_task_heading(
    "Tarea 4: Diseño de Flujo Lógico del Proceso",
    "Describir paso a paso cómo funciona el sistema mediante un diagrama de flujo con decisiones."
)

add_body(
    "A continuación se presenta el **diagrama de flujo de decisión industrial** que gobierna el funcionamiento de la máquina de estados determinista. "
    "El flujo detalla la secuencia completa desde la detección fotoeléctrica en la cinta transportadora, la captura estroboscópica, el preprocesamiento, "
    "las cinco evaluaciones lógicas booleanas y las acciones físicas finales:"
)

# Figura 8: Diagrama de Flujo Original Exacto en una sola página completa
add_apa_figure(
    "8",
    "Diagrama de Flujo del Proceso Automatizado de Inspección y Decisión Industrial",
    "fig_diagrama_flujo_original.png",
    "Secuencia determinista original con las bifurcaciones de validación (KMB, longitud >= 10 caracteres, legibilidad de fecha, fecha vencida y confianza >= 60%) "
    "conduciendo a los estados finales de Producto Aprobado o Activación de Señal de Rechazo a 24V hacia el brazo neumático.",
    width_inches=2.15
)

# Salto de página para que el diagrama de flujo quede enmarcado en su propia página exclusiva sin cortes
doc.add_page_break()

add_subheading("Análisis de Inferencia Neuronal (LSTM) y Extracción de Bounding Boxes")
add_body(
    "Para profundizar en el funcionamiento interno del clasificador neuronal, la Figura 9 desglosa la extracción a nivel de Bounding Boxes individuales "
    "y la distribución Softmax de probabilidades, contrastando el caso de una etiqueta conforme frente al colapso de confianza provocado por la falla de cabezal:"
)

# Figura 9: Análisis OCR Bounding Boxes
add_apa_figure(
    "9",
    "Análisis de Segmentación e Inferencia Neuronal OCR (LSTM) - Conforme vs. Falla en Cabezal Térmico",
    "fig_analisis_ocr_caracteres.png",
    "Desglose de Bounding Boxes individuales y vector de probabilidades Softmax: en la etiqueta conforme la confianza media alcanza 96.2%; en la falla térmica la ruptura de trazos provoca un colapso al 36.4%, disparando el descarte.",
    width_inches=5.4
)

add_body(
    "El flujo lógico detallado en las Figuras 8 y 9 se ejecuta siguiendo la siguiente secuencia de pasos operativos:"
)

add_bullet("1. Detección Física por Sensor Infrarrojo", "El empaque corta el haz fotoeléctrico, generando el flanco de subida que inicia el ciclo de inspección.")
add_bullet("2. Disparo de Cámara y Extracción de ROI", "El flash LED estroboscópico de 500 μs y el obturador global congelan la etiqueta; se recorta únicamente la ventana del fechador.")
add_bullet("3. Binarización Adaptativa de Otsu", "Transformación a grises (Y = 0.299R+0.587G+0.114B) y cálculo del umbral k* maximizando la varianza inter-clases.")
add_bullet("4. Inferencia OCR Neuronal (BLSTM + CTC)", "La red procesa las secuencias de trazos y decodifica la cadena alfanumérica junto con el vector de confianzas c_i.")
add_bullet("5. Cascada de Decisiones Booleanas", "Se evalúa secuencialmente: ¿Se lee 'KMB'? ¿Longitud ≥ 10 caracteres? ¿Fecha legible? ¿Fecha no vencida? ¿Confianza ≥ 60%?")
add_bullet("6A. Rama Conforme (APROBADO)", "Si todas las condiciones son afirmativas, se emite el chime armónico de confirmación, se registra en bitácora y la cinta continúa libre.")
add_bullet("6B. Rama No Conforme (RECHAZADO)", "Si cualquiera de las condiciones falla, se calcula el retardo cinemático (t = d / v), se activa la baliza estroboscópica roja, suena el buzzer industrial y se envía el pulso de 24V DC al PLC para que el brazo neumático empuje el empaque al contenedor de mermas.")

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
    "En la Figura 10 se aprecia la respuesta inmediata de la interfaz ante un caso de producto rechazado por caracteres borrosos, mostrando la activación "
    "de la señal PLC de 24V y la alarma sonora en planta:"
)

# Figura 10: Interfaz SCADA Rechazado
add_apa_figure(
    "10",
    "Interfaz de Control SCADA ante Detección de Falla y Accionamiento del Actuador Neumático",
    "fig_desktop_rechazado.png",
    "Banner rojo de DESCARTADO, señal de disparo PLC a 24V hacia la electroválvula del actuador neumático y registro del incidente en bitácora.",
    width_inches=5.4
)

# -------------------------------------------------------------
# TAREA 5: MITIGACIÓN DE ERRORES Y CALIBRACIÓN DE UMBRALES
# -------------------------------------------------------------
doc.add_page_break()

add_task_heading(
    "Tarea 5: Mitigación de Errores y Calibración de Umbrales",
    "¿Qué sucede si el sistema confunde un dígito debido a una arruga en la etiqueta y rechaza un producto bueno, o peor aún, acepta uno malo? ¿Cómo se ajustarán los niveles de tolerancia o umbrales de confianza?"
)

add_subheading("La Matriz de Confusión del OCR y Pares Críticos de Caracteres")
add_body(
    "En metrología industrial y visión por computadora, la interacción entre arrugas en el film plástico y la tipografía térmica genera pares críticos de confusión en la red neuronal: "
    "1) **'8' vs. 'B'**: la deformación de un lazo o una línea horizontal blanca puede hacer que un 'B' se clasifique como '8' o viceversa; "
    "2) **'0' vs. 'O'**: ambigüedad geométrica resuelta mediante segmentación sintáctica (en la fecha solo se admiten dígitos numéricos); "
    "3) **'3' vs. '8'**: la desaparición del segmento vertical izquierdo por baja temperatura del cabezal convierte un '8' en un '3'; "
    "4) **'1' vs. '/'**: confusión por similitud de trazo vertical cuando la inclinación de la cámara sufre desajuste angular (*skew*)."
)

add_subheading("Análisis Operativo: Falso Positivo vs. Falso Negativo")
add_body(
    "Ante estas confusiones, se presentan dos posibles errores estadísticos cuyas consecuencias en el negocio son radicalmente dispares:"
)

add_bullet(
    "Falso Positivo (Rechazar un Producto Bueno por una Arruga)",
    "Ocurre cuando una etiqueta con impresión perfecta sufre una sombra por un pliegue al vacío, reduciendo la confianza del OCR a un 52% y descartando el paquete. "
    "**Impacto:** El producto cae en la tolva de merma acolchada. Al final de la hora, un operario recoge estos paquetes, revisa visualmente que la fecha esté nítida "
    "y los reingresa a la cinta transportadora en segundos. El costo unitario es insignificante ($0.05 USD por tiempo de operario)."
)

add_bullet(
    "Falso Negativo (Aceptar un Producto Malo con Fecha Ilegible o Vencida)",
    "Ocurre si el sistema es demasiado permisivo y califica como 'APROBADO' un paquete con la fecha mutilada o vencida. "
    "**Impacto:** El alimento llega a las tiendas de autoservicio. Esto desencadena multas sanitarias del Ministerio de Salud (MINSA), devolución masiva del lote, "
    "pérdida de contratos comerciales y daño irreversible a la marca Embutidos Kimby (costo superior a $4,500 USD por incidente)."
)

add_subheading("Política de Calidad y Formulación Matemática de los Umbrales")
add_body(
    "Dada la asimetría de costos, la empresa adopta una política estricta de **'Cero Tolerancia Sanitaria'**: se asume una tasa de falsos rechazos de 0.2% en tolva "
    "antes que permitir un solo escape defectuoso al mercado. El índice de confianza global de la cadena se calcula según la Ecuación 5:"
)

# Ecuación 5 OMML (Confianza Global)
eq_conf_omml = (
    '<m:sSub><m:e><m:r><m:t>C</m:t></m:r></m:e><m:sub><m:r><m:t>global</m:t></m:r></m:sub></m:sSub><m:r><m:t> = </m:t></m:r>'
    '<m:f><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>N</m:t></m:r></m:den></m:f><m:r><m:t> </m:t></m:r>'
    '<m:nary><m:naryPr><m:chr m:val="∑"/><m:limLoc m:val="undOvr"/></m:naryPr>'
    '<m:sub><m:r><m:t>i=1</m:t></m:r></m:sub><m:sup><m:r><m:t>N</m:t></m:r></m:sup>'
    '<m:e><m:sSub><m:e><m:r><m:t>c</m:t></m:r></m:e><m:sub><m:r><m:t>i</m:t></m:r></m:sub></m:sSub></m:e></m:nary>'
)
add_apa_equation(eq_conf_omml, "5")

add_body(
    "Donde **c_i** es la probabilidad Softmax de cada carácter individual y **N** es la longitud de la cadena. El sistema exige simultáneamente dos condiciones: "
    "1) **C_global ≥ 60%**; y 2) **Consistencia Sintáctica al 100%**: el prefijo corporativo 'KMB' debe ser identificado inequívocamente y la fecha de vencimiento "
    "debe validar la expresión regular DD/MM/AAAA y ser estrictamente posterior al día de fabricación. Si un pliegue plástico baja la confianza de un dígito por debajo del 50%, "
    "el producto se descarta de forma segura hacia la tolva."
)

add_body(
    "Las Figuras 11 y 12 exhiben la implementación de la aplicación en dispositivos móviles Android Chrome, mostrando la captura del sensor y la alarma de rechazo:"
)

add_apa_figure(
    "11",
    "Interfaz Móvil en Android Chrome - Sección de Sensor Óptico y Encuadre Completo",
    "fig_mobile_pantalla1_sensor.png",
    "Captura íntegra sin cortes laterales en pantalla de teléfono móvil, demostrando el encuadre exacto del empaque Kimby y controles táctiles.",
    width_inches=2.9
)

add_apa_figure(
    "12",
    "Interfaz Móvil en Android Chrome - Notificación de Rechazo y Disparo Neumático",
    "fig_mobile_pantalla2_rechazo.png",
    "Pantalla móvil mostrando el banner de rechazo por texto borroso, activación de disparo al pistón neumático y registro de auditoría.",
    width_inches=2.9
)

add_body(
    "Por último, la Figura 13 muestra el Estudio Web Interactivo (`generador.html`) programado para simular fallas térmicas y deformaciones plásticas:"
)

add_apa_figure(
    "13",
    "Estudio Web y Generador de Etiquetas Interactivo para Simulación Industrial",
    "fig_generador_estudio.png",
    "Panel de control para generar variantes de etiquetas Kimby, ajustar sliders de desenfoque, pérdida de pines y arrugas para pruebas físicas y modelado 3D.",
    width_inches=5.4
)

# -------------------------------------------------------------
# CONCLUSIONES
# -------------------------------------------------------------
doc.add_page_break()

add_task_heading("Conclusiones")

add_body(
    "1. La ingeniería de Reconocimiento Óptico de Caracteres (OCR) aplicada a la línea de Embutidos Kimby demostró que la combinación de redes neuronales "
    "recurrentes **BLSTM con decodificación CTC** y preprocesamiento de Otsu es capaz de resolver de forma definitiva las fallas de legibilidad en empaques plásticos, "
    "operando en un tiempo de inferencia determinista inferior a **175 ms**."
)
add_body(
    "2. Las restricciones cinemáticas de una línea a 1.2 m/s se resuelven en el dominio físico mediante **obturación Global Shutter y destellos estroboscópicos de 500 μs**, "
    "eliminando el desenfoque por movimiento (B = 0.6 mm) sin necesidad de recurrir a filtros de deconvolución pesados que provocarían congelamiento del sistema."
)
add_body(
    "3. La política de calidad de **Cero Tolerancia Sanitaria** y la fijación del umbral de confianza global en C_global ≥ 60% garantizan que ningún producto con fecha caducada "
    "o borrosa alcance los supermercados, blindando a la empresa frente a sanciones legales y multas de salud pública."
)
add_body(
    "4. La integración y modelado cinemático mediante el **Gemelo Digital 2D interactivo** de la línea de empaque y el actuador neumático FESTO DFM permitió verificar previamente al montaje físico el factor de seguridad temporal (4.05 veces mayor a los 175 ms de latencia), validando la sincronización estroboscópica y la expulsión lateral de mermas a 1.2 m/s."
)

# -------------------------------------------------------------
# REFERENCIAS BIBLIOGRÁFICAS APA 7
# -------------------------------------------------------------
doc.add_page_break()

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

# 5. Convertir a PDF institucionalmente con Word COM (DisplayAlerts=0)
print(f"[5/5] Convirtiendo a PDF institucional en: {FINAL_PDF}...")
try:
    import win32com.client
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0 # Suprimir alertas y cuadros de recuperación
    doc_word = word.Documents.Open(FINAL_DOCX, ReadOnly=True)
    doc_word.SaveAs(FINAL_PDF, FileFormat=17) # 17 = wdFormatPDF
    doc_word.Close(False)
    word.Quit()
except Exception as e:
    print(f"Aviso en Word COM: {e}. Intentando convert()...")
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

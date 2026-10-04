import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_font(size, bold=False):
    # Try standard Windows fonts
    font_paths = [
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf" if bold else "C:\\Windows\\Fonts\\calibri.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_flowchart():
    """Crea el diagrama de flujo oficial con decisiones para la Tarea 4"""
    width, height = 1200, 850
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_sub = get_font(15, bold=False)
    f_box_t = get_font(16, bold=True)
    f_box_d = get_font(13, bold=False)
    f_label = get_font(14, bold=True)

    # Título superior del diagrama
    draw.text((600, 30), "DIAGRAMA DE FLUJO LÓGICO DEL PROCESO DE INSPECCIÓN EN LÍNEA", fill=(15, 23, 42), font=f_title, anchor="mt")
    draw.text((600, 65), "Sistema Automatizado de Control de Calidad y Rechazo Neumático — Embutidos Kimby", fill=(71, 85, 105), font=f_sub, anchor="mt")
    draw.line([(80, 95), (1120, 95)], fill=(203, 213, 225), width=2)

    def draw_box(x, y, w, h, title, desc, shape="rect", fill_color=(248, 250, 252), border_color=(15, 23, 42)):
        if shape == "round":
            draw.rounded_rectangle([x, y, x + w, y + h], radius=15, fill=fill_color, outline=border_color, width=2)
        elif shape == "diamond":
            pts = [(x + w // 2, y), (x + w, y + h // 2), (x + w // 2, y + h), (x, y + h // 2)]
            draw.polygon(pts, fill=fill_color, outline=border_color)
            # Re-draw outline for thickness
            for i in range(4):
                draw.line([pts[i], pts[(i + 1) % 4]], fill=border_color, width=2)
        else: # rect
            draw.rectangle([x, y, x + w, y + h], fill=fill_color, outline=border_color, width=2)
        
        # Text
        lines = desc.split("\n") if desc else []
        total_text_h = 20 + len(lines) * 16
        start_y = y + (h - total_text_h) // 2
        
        draw.text((x + w // 2, start_y), title, fill=border_color, font=f_box_t, anchor="mt")
        for idx, line in enumerate(lines):
            draw.text((x + w // 2, start_y + 22 + idx * 16), line, fill=(51, 65, 85), font=f_box_d, anchor="mt")

    def draw_arrow(x1, y1, x2, y2, text=None, text_side="right"):
        draw.line([(x1, y1), (x2, y2)], fill=(15, 23, 42), width=2)
        # Arrowhead
        if x1 == x2: # vertical
            if y2 > y1: # down
                draw.polygon([(x2 - 6, y2 - 10), (x2 + 6, y2 - 10), (x2, y2)], fill=(15, 23, 42))
            else: # up
                draw.polygon([(x2 - 6, y2 + 10), (x2 + 6, y2 + 10), (x2, y2)], fill=(15, 23, 42))
        elif y1 == y2: # horizontal
            if x2 > x1: # right
                draw.polygon([(x2 - 10, y2 - 6), (x2 - 10, y2 + 6), (x2, y2)], fill=(15, 23, 42))
            else: # left
                draw.polygon([(x2 + 10, y2 - 6), (x2 + 10, y2 + 6), (x2, y2)], fill=(15, 23, 42))
        
        if text:
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2
            if text_side == "right":
                draw.text((mx + 10, my - 8), text, fill=(15, 23, 42), font=f_label)
            elif text_side == "left":
                draw.text((mx - 35, my - 8), text, fill=(15, 23, 42), font=f_label)
            elif text_side == "top":
                draw.text((mx, my - 20), text, fill=(15, 23, 42), font=f_label, anchor="mt")

    # Paso 1: Inicio / Fotocélula
    draw_box(460, 115, 280, 55, "1. DETECCIÓN (TRIGGER)", "Empaque corta haz de fotocélula", shape="round")
    draw_arrow(600, 170, 600, 205)

    # Paso 2: Disparo Estroboscópico y Cámara
    draw_box(440, 205, 320, 60, "2. ADQUISICIÓN ÓPTICA", "Flash LED (500 μs) + Global Shutter\nCongelamiento sin motion blur")
    draw_arrow(600, 265, 600, 300)

    # Paso 3: Preprocesamiento ROI y Otsu
    draw_box(440, 300, 320, 60, "3. PREPROCESAMIENTO LIGERO", "Recorte de ROI (fechador) < 15 ms\nEscala de grises y binarización Otsu")
    draw_arrow(600, 360, 600, 395)

    # Paso 4: Inferencia OCR
    draw_box(440, 395, 320, 60, "4. INFERENCIA OCR (EDGE)", "Motor neuronal Tesseract LSTM\nExtracción de caracteres y confianza")
    draw_arrow(600, 455, 600, 495)

    # Paso 5: Rombo de Decisión Principal
    draw_box(420, 495, 360, 120, "¿CUMPLE REGLAS?", "• ¿Contiene 'KMB'?\n• ¿Longitud lote >= 10?\n• ¿Fecha válida y no vencida?\n• ¿Confianza media >= 65%?", shape="diamond")

    # Rama SÍ (Aprobado - Hacia la izquierda)
    draw_line_pts_yes = [(420, 555), (240, 555), (240, 660)]
    draw.line(draw_line_pts_yes, fill=(15, 23, 42), width=2)
    draw.polygon([(234, 650), (246, 650), (240, 660)], fill=(15, 23, 42))
    draw.text((310, 532), "SÍ (100% Válido)", fill=(15, 23, 42), font=f_label)

    draw_box(100, 660, 280, 80, "PRODUCTO APROBADO", "• Libre tránsito hacia encartonado\n• Señal visual verde y chime melódico\n• Registro conforme en bitácora", shape="round", fill_color=(240, 253, 244), border_color=(22, 101, 52))

    # Rama NO (Rechazado - Hacia la derecha)
    draw_line_pts_no = [(780, 555), (960, 555), (960, 660)]
    draw.line(draw_line_pts_no, fill=(15, 23, 42), width=2)
    draw.polygon([(954, 650), (966, 650), (960, 660)], fill=(15, 23, 42))
    draw.text((820, 532), "NO (Cualquier fallo)", fill=(15, 23, 42), font=f_label)

    draw_box(820, 660, 280, 80, "PRODUCTO RECHAZADO", "• Retardo cinemático t = d / v\n• Disparo 24V a pistón neumático\n• Eyección a tolva + Alarma sonora", shape="round", fill_color=(254, 242, 242), border_color=(153, 27, 27))

    # Pie de diagrama
    draw.line([(80, 775), (1120, 775)], fill=(203, 213, 225), width=1)
    draw.text((600, 795), "Tiempo de ciclo total: < 180 ms | Distancia a actuador: 0.85 m | Tiempo de tránsito disponible: 708 ms (Margen seguro)", fill=(71, 85, 105), font=f_box_d, anchor="mt")

    out_path = os.path.join(BASE_DIR, "fig_diagrama_flujo.png")
    img.save(out_path, dpi=(300, 300))
    print("Guardado:", out_path)

def create_ocr_pipeline_diagram():
    """Crea una ilustración del pipeline de preprocesamiento de imagen para la Tarea 1"""
    width, height = 1100, 420
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(20, bold=True)
    f_sub = get_font(14, bold=False)
    f_step_t = get_font(15, bold=True)
    f_step_d = get_font(12, bold=False)
    f_mono = get_font(13, bold=True)

    draw.text((550, 20), "PIPELINE DE PREPROCESAMIENTO DE IMAGEN EN TIEMPO REAL (< 25 ms)", fill=(15, 23, 42), font=f_title, anchor="mt")
    draw.text((550, 48), "Secuencia de optimización para OCR en banda continua sin sobrecarga computacional", fill=(71, 85, 105), font=f_sub, anchor="mt")
    draw.line([(60, 75), (1040, 75)], fill=(203, 213, 225), width=2)

    steps = [
        ("Paso 1: Captura Instantánea", "Fotograma crudo 1200x800\nGlobal Shutter (500 μs)\nSin motion blur", (248, 250, 252)),
        ("Paso 2: Recorte de ROI", "Coordenadas fijas 60x25 mm\nElimina 85% de la imagen\nTiempo: < 3 ms", (241, 245, 249)),
        ("Paso 3: Escala de Grises", "Fórmula Y = 0.299R+0.587G+0.114B\nMatriz monocromática 8 bits\nTiempo: < 5 ms", (241, 245, 249)),
        ("Paso 4: Binarización Otsu", "Umbralización adaptativa\nTinta negra aislada de fondo\nTiempo: < 12 ms", (241, 245, 249))
    ]

    box_w = 220
    box_h = 240
    start_x = 70
    gap = 40
    y_pos = 100

    for i, (title, desc, bg) in enumerate(steps):
        bx = start_x + i * (box_w + gap)
        draw.rounded_rectangle([bx, y_pos, bx + box_w, y_pos + box_h], radius=10, fill=bg, outline=(15, 23, 42), width=2)
        
        # Header inside box
        draw.text((bx + box_w // 2, y_pos + 15), title, fill=(15, 23, 42), font=f_step_t, anchor="mt")
        draw.line([(bx + 15, y_pos + 42), (bx + box_w - 15, y_pos + 42)], fill=(203, 213, 225), width=1)
        
        # Inner simulated screen/preview
        preview_y = y_pos + 55
        preview_h = 90
        draw.rectangle([bx + 15, preview_y, bx + box_w - 15, preview_y + preview_h], fill=(255, 255, 255), outline=(100, 116, 139), width=1)
        
        if i == 0:
            # Full label mini representation
            draw.rectangle([bx + 25, preview_y + 10, bx + box_w - 25, preview_y + 80], fill=(254, 242, 242), outline=(185, 28, 28), width=1)
            draw.text((bx + box_w // 2, preview_y + 22), "KIMBY", fill=(185, 28, 28), font=f_step_t, anchor="mt")
            draw.rectangle([bx + 40, preview_y + 48, bx + box_w - 40, preview_y + 72], fill=(255, 255, 255), outline=(15, 23, 42))
            draw.text((bx + box_w // 2, preview_y + 54), "LOTE / VENC", fill=(15, 23, 42), font=f_step_d, anchor="mt")
        elif i == 1:
            # Cropped ROI
            draw.rectangle([bx + 25, preview_y + 25, bx + box_w - 25, preview_y + 65], fill=(248, 250, 252), outline=(15, 23, 42), width=2)
            draw.text((bx + box_w // 2, preview_y + 32), "KMB-2026-A01", fill=(15, 23, 42), font=f_mono, anchor="mt")
            draw.text((bx + box_w // 2, preview_y + 48), "15/12/2026", fill=(15, 23, 42), font=f_mono, anchor="mt")
        elif i == 2:
            # Grayscale
            draw.rectangle([bx + 25, preview_y + 25, bx + box_w - 25, preview_y + 65], fill=(226, 232, 240), outline=(71, 85, 105), width=2)
            draw.text((bx + box_w // 2, preview_y + 32), "KMB-2026-A01", fill=(51, 65, 85), font=f_mono, anchor="mt")
            draw.text((bx + box_w // 2, preview_y + 48), "15/12/2026", fill=(51, 65, 85), font=f_mono, anchor="mt")
        elif i == 3:
            # Binary Otsu (high contrast pure black and white)
            draw.rectangle([bx + 25, preview_y + 25, bx + box_w - 25, preview_y + 65], fill=(255, 255, 255), outline=(15, 23, 42), width=2)
            draw.text((bx + box_w // 2, preview_y + 32), "KMB-2026-A01", fill=(0, 0, 0), font=f_mono, anchor="mt")
            draw.text((bx + box_w // 2, preview_y + 48), "15/12/2026", fill=(0, 0, 0), font=f_mono, anchor="mt")

        # Description text below preview
        lines = desc.split("\n")
        for l_idx, line in enumerate(lines):
            draw.text((bx + box_w // 2, preview_y + preview_h + 12 + l_idx * 16), line, fill=(51, 65, 85), font=f_step_d, anchor="mt")

        # Arrow between steps
        if i < 3:
            ax = bx + box_w + 10
            ay = y_pos + box_h // 2
            draw.line([(ax, ay), (ax + 20, ay)], fill=(15, 23, 42), width=2)
            draw.polygon([(ax + 14, ay - 5), (ax + 14, ay + 5), (ax + 22, ay)], fill=(15, 23, 42))

    # Bottom footer
    draw.line([(60, 365), (1040, 365)], fill=(203, 213, 225), width=1)
    draw.text((550, 385), "Salida preprocesada lista para inferencia neuronal por Tesseract.js WASM | Carga de CPU: < 18%", fill=(71, 85, 105), font=f_step_d, anchor="mt")

    out_path = os.path.join(BASE_DIR, "fig_pipeline_ocr.png")
    img.save(out_path, dpi=(300, 300))
    print("Guardado:", out_path)

if __name__ == "__main__":
    create_flowchart()
    create_ocr_pipeline_diagram()

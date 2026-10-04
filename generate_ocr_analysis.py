import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_font(size, bold=False):
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

def create_ocr_character_analysis():
    width, height = 1200, 520
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(20, bold=True)
    f_sub = get_font(14, bold=False)
    f_box_t = get_font(15, bold=True)
    f_box_d = get_font(12, bold=False)
    f_mono = get_font(18, bold=True)
    f_conf = get_font(11, bold=True)

    # Title
    draw.text((600, 20), "ANÁLISIS DE SEGMENTACIÓN E INFERENCIA NEURONAL OCR (LSTM)", fill=(15, 23, 42), font=f_title, anchor="mt")
    draw.text((600, 48), "Comparativa de decodificación y matrices de confianza: Etiqueta Conforme vs. Falla en Cabezal Térmico", fill=(71, 85, 105), font=f_sub, anchor="mt")
    draw.line([(60, 75), (1140, 75)], fill=(203, 213, 225), width=2)

    # PANEL 1: ETIQUETA CONFORME (IZQUIERDA)
    p1_x, p1_y, p1_w, p1_h = 60, 95, 520, 380
    draw.rounded_rectangle([p1_x, p1_y, p1_x + p1_w, p1_y + p1_h], radius=10, fill=(248, 250, 252), outline=(22, 101, 52), width=2)
    draw.rectangle([p1_x, p1_y, p1_x + p1_w, p1_y + 35], fill=(220, 252, 231))
    draw.text((p1_x + p1_w // 2, p1_y + 10), "CASO 1: ETIQUETA NÍTIDA (CONFORME) — CONFIANZA GLOBAL: 96.2%", fill=(22, 101, 52), font=f_box_t, anchor="mt")

    # Character boxes row 1 (KMB-2026-A01)
    chars_good = [("K", "99%"), ("M", "97%"), ("B", "96%"), ("-", "99%"), ("2", "98%"), ("0", "96%"), ("2", "97%"), ("6", "95%"), ("-", "99%"), ("A", "96%"), ("0", "95%"), ("1", "98%")]
    start_cx = p1_x + 25
    c_w, c_h = 36, 50
    cy1 = p1_y + 60

    draw.text((p1_x + 25, cy1 - 18), "Lote detectado: Bounding Boxes individuales y Softmax:", fill=(15, 23, 42), font=f_box_d)

    for i, (ch, conf) in enumerate(chars_good):
        bx = start_cx + i * 39
        draw.rectangle([bx, cy1, bx + c_w, cy1 + c_h], fill=(255, 255, 255), outline=(22, 101, 52), width=1)
        draw.text((bx + c_w // 2, cy1 + 10), ch, fill=(0, 0, 0), font=f_mono, anchor="mt")
        draw.rectangle([bx, cy1 + c_h - 14, bx + c_w, cy1 + c_h], fill=(220, 252, 231))
        draw.text((bx + c_w // 2, cy1 + c_h - 13), conf, fill=(22, 101, 52), font=f_conf, anchor="mt")

    # Row 2 (VENC: 15/12/2026)
    chars_date = [("1", "99%"), ("5", "96%"), ("/", "99%"), ("1", "98%"), ("2", "97%"), ("/", "99%"), ("2", "98%"), ("0", "96%"), ("2", "97%"), ("6", "95%")]
    cy2 = cy1 + 80
    draw.text((p1_x + 25, cy2 - 18), "Fecha de vencimiento: Extracción cronológica:", fill=(15, 23, 42), font=f_box_d)

    for i, (ch, conf) in enumerate(chars_date):
        bx = start_cx + i * 39
        draw.rectangle([bx, cy2, bx + c_w, cy2 + c_h], fill=(255, 255, 255), outline=(22, 101, 52), width=1)
        draw.text((bx + c_w // 2, cy2 + 10), ch, fill=(0, 0, 0), font=f_mono, anchor="mt")
        draw.rectangle([bx, cy2 + c_h - 14, bx + c_w, cy2 + c_h], fill=(220, 252, 231))
        draw.text((bx + c_w // 2, cy2 + c_h - 13), conf, fill=(22, 101, 52), font=f_conf, anchor="mt")

    # Diagnostic text
    draw.rectangle([p1_x + 20, cy2 + 65, p1_x + p1_w - 20, p1_y + p1_h - 15], fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((p1_x + 30, cy2 + 75), "• CTC Loss Decoder: Alineación continua perfecta sin saltos.", fill=(51, 65, 85), font=f_box_d)
    draw.text((p1_x + 30, cy2 + 95), "• Validación Regex: Prefijo 'KMB' presente (12 chars válidos).", fill=(51, 65, 85), font=f_box_d)
    draw.text((p1_x + 30, cy2 + 115), "• Consistencia Cronológica: 15/12/2026 > Fecha actual (Vigente).", fill=(51, 65, 85), font=f_box_d)
    draw.text((p1_x + 30, cy2 + 135), "• Veredicto Final: APROBADO (Paso libre a encartonado).", fill=(22, 101, 52), font=f_box_t)

    # PANEL 2: ETIQUETA CON FALLA TÉRMICA (DERECHA)
    p2_x = 620
    draw.rounded_rectangle([p2_x, p1_y, p2_x + p1_w, p1_y + p1_h], radius=10, fill=(248, 250, 252), outline=(153, 27, 27), width=2)
    draw.rectangle([p2_x, p1_y, p2_x + p1_w, p1_y + 35], fill=(254, 226, 226))
    draw.text((p2_x + p1_w // 2, p1_y + 10), "CASO 2: FALLA CABEZAL (PINES QUEMADOS) — CONFIANZA: 36.4%", fill=(153, 27, 27), font=f_box_t, anchor="mt")

    # Character boxes row 1 (Broken KMB)
    chars_bad = [("K", "61%"), (" ", "0%"), ("3", "28%"), ("-", "88%"), ("2", "41%"), (" ", "0%"), ("2", "39%"), ("-", "75%"), (" ", "0%"), ("?", "15%"), (" ", "0%"), ("1", "55%")]
    start_cx2 = p2_x + 25
    draw.text((p2_x + 25, cy1 - 18), "Lote mutilado: Ruptura de trazos por drop-out térmico:", fill=(15, 23, 42), font=f_box_d)

    for i, (ch, conf) in enumerate(chars_bad):
        bx = start_cx2 + i * 39
        draw.rectangle([bx, cy1, bx + c_w, cy1 + c_h], fill=(255, 255, 255), outline=(153, 27, 27), width=1)
        # Draw broken char simulation
        draw.text((bx + c_w // 2, cy1 + 10), ch, fill=(153, 27, 27), font=f_mono, anchor="mt")
        # Draw white strike-through line simulating missing thermal pin
        draw.line([(bx + 4, cy1 + 24), (bx + c_w - 4, cy1 + 24)], fill=(255, 255, 255), width=3)
        draw.rectangle([bx, cy1 + c_h - 14, bx + c_w, cy1 + c_h], fill=(254, 226, 226))
        draw.text((bx + c_w // 2, cy1 + c_h - 13), conf, fill=(153, 27, 27), font=f_conf, anchor="mt")

    # Row 2 (Broken date)
    chars_date_bad = [("1", "62%"), ("?", "18%"), ("/", "85%"), ("-", "0%"), ("-", "0%"), ("/", "70%"), ("-", "0%"), ("-", "0%"), ("-", "0%"), ("-", "0%")]
    draw.text((p2_x + 25, cy2 - 18), "Fecha ilegible: Segmentación colapsada por pines quemados:", fill=(15, 23, 42), font=f_box_d)

    for i, (ch, conf) in enumerate(chars_date_bad):
        bx = start_cx2 + i * 39
        draw.rectangle([bx, cy2, bx + c_w, cy2 + c_h], fill=(255, 255, 255), outline=(153, 27, 27), width=1)
        draw.text((bx + c_w // 2, cy2 + 10), ch, fill=(153, 27, 27), font=f_mono, anchor="mt")
        draw.line([(bx + 4, cy2 + 24), (bx + c_w - 4, cy2 + 24)], fill=(255, 255, 255), width=3)
        draw.rectangle([bx, cy2 + c_h - 14, bx + c_w, cy2 + c_h], fill=(254, 226, 226))
        draw.text((bx + c_w // 2, cy2 + c_h - 13), conf, fill=(153, 27, 27), font=f_conf, anchor="mt")

    # Diagnostic text
    draw.rectangle([p2_x + 20, cy2 + 65, p2_x + p1_w - 20, p1_y + p1_h - 15], fill=(255, 255, 255), outline=(203, 213, 225))
    draw.text((p2_x + 30, cy2 + 75), "• CTC Loss Decoder: Confusión fonética / Colapso 'B' -> '3' o espacio.", fill=(153, 27, 27), font=f_box_d)
    draw.text((p2_x + 30, cy2 + 95), "• Validación Regex: FALLA. No se lee prefijo 'KMB' completo.", fill=(153, 27, 27), font=f_box_d)
    draw.text((p2_x + 30, cy2 + 115), "• Confianza Global: 36.4% < 60.0% (Umbral crítico insatisfecho).", fill=(153, 27, 27), font=f_box_d)
    draw.text((p2_x + 30, cy2 + 135), "• Veredicto Final: RECHAZADO (Disparo neumático 24V inmediato).", fill=(153, 27, 27), font=f_box_t)

    out_path = os.path.join(BASE_DIR, "fig_analisis_ocr_caracteres.png")
    img.save(out_path, dpi=(300, 300))
    print("Guardado:", out_path)

if __name__ == "__main__":
    create_ocr_character_analysis()

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT_DIR = r"d:\III Pacial 4to Año\kimby_qc_app\etiquetas_blender"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Try loading Windows system fonts
try:
    font_header = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 46)
    font_sub = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 26)
    font_tag = ImageFont.truetype(r"C:\Windows\Fonts\arial.ttf", 18)
    font_thermal = ImageFont.truetype(r"C:\Windows\Fonts\courbd.ttf", 44)
    font_thermal_sub = ImageFont.truetype(r"C:\Windows\Fonts\courbd.ttf", 24)
    font_barcode = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 22)
except Exception:
    font_header = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_tag = ImageFont.load_default()
    font_thermal = ImageFont.load_default()
    font_thermal_sub = ImageFont.load_default()
    font_barcode = ImageFont.load_default()

def draw_barcode(draw, x, y, width, height):
    """Draws a realistic industrial 1D barcode with guard bars and text."""
    random.seed(42)
    cur_x = x
    while cur_x < x + width:
        bar_w = random.choice([2, 3, 5, 7])
        draw.rectangle([cur_x, y, cur_x + bar_w, y + height], fill=(20, 20, 20))
        space_w = random.choice([2, 4, 6])
        cur_x += bar_w + space_w
    # Guard lines at ends
    draw.rectangle([x - 6, y, x - 2, y + height + 8], fill=(0, 0, 0))
    draw.rectangle([x + width + 2, y, x + width + 6, y + height + 8], fill=(0, 0, 0))
    # Code text below
    draw.text((x + 15, y + height + 4), "7 701234 567890", fill=(20, 20, 20), font=font_barcode)

def create_base_pack(product_title, product_sub):
    """Generates the vacuum pack package base image with industrial branding."""
    W, H = 1200, 800
    img = Image.new("RGBA", (W, H), (245, 245, 245, 255))
    draw = ImageDraw.Draw(img)

    # 1. Outer background (plastic vacuum sealed gradient)
    # Kimby Red gradient
    for y in range(H):
        ratio = y / H
        r = int(140 + 45 * math.sin(ratio * math.pi))
        g = int(20 + 15 * math.cos(ratio * math.pi))
        b = int(25 + 15 * math.cos(ratio * math.pi))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Plastic seal edges (sealed packaging seams)
    draw.rectangle([0, 0, W, 25], fill=(120, 15, 20))
    draw.rectangle([0, H - 25, W, H], fill=(120, 15, 20))
    # Sealing texture dots / crimps
    for cx in range(0, W, 8):
        draw.rectangle([cx, 2, cx + 4, 23], fill=(160, 25, 30))
        draw.rectangle([cx, H - 23, cx + 4, H - 2], fill=(160, 25, 30))

    # Main Brand Card (Center)
    card_x0, card_y0 = 60, 50
    card_x1, card_y1 = W - 60, H - 50
    draw.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=16, fill=(185, 28, 28), outline=(220, 38, 38), width=3)

    # Top Brand Ribbon (Gold)
    ribbon_y0 = card_y0 + 15
    ribbon_y1 = ribbon_y0 + 75
    draw.rounded_rectangle([card_x0 + 20, ribbon_y0, card_x1 - 20, ribbon_y1], radius=10, fill=(245, 158, 11), outline=(251, 191, 36), width=2)
    
    # Header text
    brand_text = "EMBUTIDOS KIMBY - CALIDAD Y TRADICIÓN"
    bbox = draw.textbbox((0, 0), brand_text, font=font_header)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, ribbon_y0 + 12), brand_text, fill=(120, 20, 20), font=font_header)

    # Product Title & Subtitle
    bbox_p = draw.textbbox((0, 0), product_title, font=font_header)
    tw_p = bbox_p[2] - bbox_p[0]
    draw.text(((W - tw_p) / 2, ribbon_y1 + 18), product_title, fill=(255, 255, 255), font=font_header)

    bbox_s = draw.textbbox((0, 0), product_sub, font=font_sub)
    tw_s = bbox_s[2] - bbox_s[0]
    draw.text(((W - tw_s) / 2, ribbon_y1 + 72), product_sub, fill=(254, 240, 138), font=font_sub)

    # Thermal printing window (Matte White window for thermal transfer)
    win_w, win_h = 820, 300
    win_x0 = int((W - win_w) / 2)
    win_y0 = ribbon_y1 + 115
    win_x1 = win_x0 + win_w
    win_y1 = win_y0 + win_h

    # White box background
    draw.rounded_rectangle([win_x0, win_y0, win_x1, win_y1], radius=8, fill=(255, 255, 255), outline=(203, 213, 225), width=2)
    # Registration corner marks (industrial alignment marks)
    draw.line([(win_x0 + 10, win_y0 + 10), (win_x0 + 30, win_y0 + 10)], fill=(148, 163, 184), width=2)
    draw.line([(win_x0 + 10, win_y0 + 10), (win_x0 + 10, win_y0 + 30)], fill=(148, 163, 184), width=2)
    draw.line([(win_x1 - 30, win_y0 + 10), (win_x1 - 10, win_y0 + 10)], fill=(148, 163, 184), width=2)
    draw.line([(win_x1 - 10, win_y0 + 10), (win_x1 - 10, win_y0 + 30)], fill=(148, 163, 184), width=2)
    draw.line([(win_x0 + 10, win_y1 - 10), (win_x0 + 30, win_y1 - 10)], fill=(148, 163, 184), width=2)
    draw.line([(win_x0 + 10, win_y1 - 10), (win_x0 + 10, win_y1 - 30)], fill=(148, 163, 184), width=2)
    draw.line([(win_x1 - 30, win_y1 - 10), (win_x1 - 10, win_y1 - 10)], fill=(148, 163, 184), width=2)
    draw.line([(win_x1 - 10, win_y1 - 10), (win_x1 - 10, win_y1 - 30)], fill=(148, 163, 184), width=2)

    # Sub-header inside thermal window
    tag_str = "[VENTANA DE CODIFICACION TERMICA TIJ / TTO - ALTA VELOCIDAD]"
    draw.text((win_x0 + 35, win_y0 + 16), tag_str, fill=(100, 116, 139), font=font_tag)
    draw.line([(win_x0 + 35, win_y0 + 42), (win_x1 - 35, win_y0 + 42)], fill=(226, 232, 240), width=1)

    # Barcode & Regulatory Seals at bottom
    draw_barcode(draw, win_x0 + 35, win_y1 + 22, 260, 50)
    
    # Sanitation / Inspection badge
    badge_x = win_x1 - 320
    badge_y = win_y1 + 20
    draw.rounded_rectangle([badge_x, badge_y, win_x1 - 35, badge_y + 70], radius=6, fill=(153, 27, 27), outline=(254, 240, 138), width=1)
    draw.text((badge_x + 15, badge_y + 12), "INSPECCIONADO Y APROBADO", fill=(255, 255, 255), font=font_barcode)
    draw.text((badge_x + 15, badge_y + 40), "MINISTERIO DE SALUD | REG. SAN. 4410", fill=(254, 240, 138), font=font_tag)

    return img, (win_x0, win_y0, win_x1, win_y1)

def render_label_variant(variant_id, filename, product_title, product_sub, lot_str, exp_str, prod_str, defect_type=None):
    """Renders a specific label variant with high resolution and defect simulation."""
    img, (wx0, wy0, wx1, wy1) = create_base_pack(product_title, product_sub)

    # Separate thermal text layer to apply blur/distortion independently
    thermal_img = Image.new("RGBA", (wx1 - wx0, wy1 - wy0), (255, 255, 255, 0))
    t_draw = ImageDraw.Draw(thermal_img)

    text_x = 45
    text_y_lote = 75
    text_y_venc = 150
    text_y_prod = 225

    t_color = (15, 23, 42, 255)
    if defect_type == "expired":
        t_color_venc = (185, 28, 28, 255) # Highlight expired in red
    else:
        t_color_venc = t_color

    t_draw.text((text_x, text_y_lote), f"LOTE: {lot_str}", fill=t_color, font=font_thermal)
    t_draw.text((text_x, text_y_venc), f"VENC: {exp_str}", fill=t_color_venc, font=font_thermal)
    t_draw.text((text_x, text_y_prod), f"PROD: {prod_str}", fill=(71, 85, 105, 255), font=font_thermal_sub)

    # Apply defect logic
    if defect_type == "broken_pins":
        # Simulates burned out pins in thermal head (horizontal white dropouts cutting through text)
        for py in [text_y_lote + 15, text_y_lote + 22, text_y_venc + 18, text_y_venc + 26]:
            t_draw.rectangle([text_x - 10, py, wx1 - wx0 - 20, py + 4], fill=(255, 255, 255, 255))
        # Slight jitter / faintness
        thermal_img = thermal_img.filter(ImageFilter.GaussianBlur(radius=0.7))

    elif defect_type == "heavy_blur":
        # Simulates low head temperature, wrong ribbon speed, or smearing
        thermal_img = thermal_img.filter(ImageFilter.GaussianBlur(radius=4.5))

    elif defect_type == "moderate_blur":
        thermal_img = thermal_img.filter(ImageFilter.GaussianBlur(radius=2.8))

    elif defect_type == "wrinkle_glare":
        # Simulates packaging wrinkle across thermal window
        w_overlay = Image.new("RGBA", thermal_img.size, (255, 255, 255, 0))
        w_draw = ImageDraw.Draw(w_overlay)
        # Specular light bar (reflection)
        for offset in range(-30, 30):
            alpha = int(140 * (1 - abs(offset) / 30))
            w_draw.line([(100 + offset, 0), (280 + offset, wy1 - wy0)], fill=(255, 255, 255, alpha), width=2)
        thermal_img = Image.alpha_composite(thermal_img, w_overlay)

    # Composite thermal text onto main image
    img.paste(thermal_img, (wx0, wy0), thermal_img)

    # Save to disk
    out_path = os.path.join(OUTPUT_DIR, filename)
    img.save(out_path, "PNG", dpi=(300, 300))
    print(f"Generated: {filename}")
    return out_path

# Generate 8 distinct labels for testing and Blender animation
variants = [
    {
        "id": 1,
        "filename": "01_conforme_salchicha_viena.png",
        "title": "SALCHICHA VIENA TRADICIONAL",
        "sub": "EMPAQUE AL VACÍO • 500g • MANTÉNGASE EN REFRIGERACIÓN",
        "lote": "KMB-2026-A01",
        "venc": "15/12/2026",
        "prod": "15/10/2026  TURNO 1  L-01",
        "defect": None
    },
    {
        "id": 2,
        "filename": "02_conforme_jamon_cocido.png",
        "title": "JAMÓN COCIDO ESPECIAL PIERNA",
        "sub": "REBANADO FINO • 400g • MANTÉNGASE EN REFRIGERACIÓN",
        "lote": "KMB-2026-B14",
        "venc": "20/01/2027",
        "prod": "20/10/2026  TURNO 2  L-03",
        "defect": None
    },
    {
        "id": 3,
        "filename": "03_conforme_mortadela_familiar.png",
        "title": "MORTADELA FAMILIAR SUPREMA",
        "sub": "EMPAQUE AL VACÍO • 750g • MANTÉNGASE EN REFRIGERACIÓN",
        "lote": "KMB-2026-C08",
        "venc": "05/02/2027",
        "prod": "25/10/2026  TURNO 1  L-02",
        "defect": None
    },
    {
        "id": 4,
        "filename": "04_falla_cabezal_pines_rotos.png",
        "title": "SALCHICHA VIENA TRADICIONAL",
        "sub": "EMPAQUE AL VACÍO • 500g • MANTÉNGASE EN REFRIGERACIÓN",
        "lote": "KMB-2026-A01",
        "venc": "15/12/2026",
        "prod": "15/10/2026  TURNO 1  L-01",
        "defect": "broken_pins"  # Falla real del cabezal térmico (pines quemados)
    },
    {
        "id": 5,
        "filename": "05_falla_impresion_borrosa_frotada.png",
        "title": "SALCHICHA VIENA TRADICIONAL",
        "sub": "EMPAQUE AL VACÍO • 500g • MANTÉNGASE EN REFRIGERACIÓN",
        "lote": "KMB-2026-A01",
        "venc": "15/12/2026",
        "prod": "15/10/2026  TURNO 1  L-01",
        "defect": "heavy_blur"  # Falla de arrastre o temperatura baja
    },
    {
        "id": 6,
        "filename": "06_falla_producto_vencido.png",
        "title": "SALCHICHA VIENA TRADICIONAL",
        "sub": "EMPAQUE AL VACÍO • 500g • MANTÉNGASE EN REFRIGERACIÓN",
        "lote": "KMB-2026-A01",
        "venc": "10/01/2023",  # Vencido
        "prod": "10/07/2022  TURNO 1  L-01",
        "defect": "expired"
    },
    {
        "id": 7,
        "filename": "07_falla_codigo_trunco_ilegible.png",
        "title": "SALCHICHA VIENA TRADICIONAL",
        "sub": "EMPAQUE AL VACÍO • 500g • MANTÉNGASE EN REFRIGERACIÓN",
        "lote": "KM-26",       # Menor a 10 caracteres, falta B y año
        "venc": "15/--/----",
        "prod": "15/10/2026  TURNO 1  L-01",
        "defect": "moderate_blur"
    },
    {
        "id": 8,
        "filename": "08_falla_arruga_y_reflejo_luz.png",
        "title": "SALCHICHA VIENA TRADICIONAL",
        "sub": "EMPAQUE AL VACÍO • 500g • MANTÉNGASE EN REFRIGERACIÓN",
        "lote": "KMB-2026-A01",
        "venc": "15/12/2026",
        "prod": "15/10/2026  TURNO 1  L-01",
        "defect": "wrinkle_glare"
    }
]

for v in variants:
    render_label_variant(v["id"], v["filename"], v["title"], v["sub"], v["lote"], v["venc"], v["prod"], v["defect"])

print("All 8 Kimby label variants generated successfully!")

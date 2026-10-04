import os
import time
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_URL = "file:///" + os.path.join(BASE_DIR, "index.html").replace("\\", "/")
GENERADOR_URL = "file:///" + os.path.join(BASE_DIR, "generador.html").replace("\\", "/")

print("Capturing precision screenshots with Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # ---------------------------------------------------------
    # 1. DESKTOP VIEW - APROBADO (1440 x 940)
    # ---------------------------------------------------------
    page = browser.new_page(viewport={"width": 1440, "height": 940}, device_scale_factor=2)
    page.goto(INDEX_URL)
    page.wait_for_timeout(1000)
    page.evaluate("document.querySelectorAll('.sample-chip')[0].click();")
    page.wait_for_timeout(2000)
    out_desktop_pass = os.path.join(BASE_DIR, "fig_desktop_aprobado.png")
    page.screenshot(path=out_desktop_pass)
    print("Saved:", out_desktop_pass)
    
    # ---------------------------------------------------------
    # 2. DESKTOP VIEW - RECHAZADO (1440 x 940)
    # ---------------------------------------------------------
    page.evaluate("document.querySelectorAll('.sample-chip')[1].click();")
    page.wait_for_timeout(2000)
    out_desktop_fail = os.path.join(BASE_DIR, "fig_desktop_rechazado.png")
    page.screenshot(path=out_desktop_fail)
    print("Saved:", out_desktop_fail)
    
    # ---------------------------------------------------------
    # 3. GENERADOR DE ETIQUETAS DESKTOP (1440 x 940)
    # ---------------------------------------------------------
    page.goto(GENERADOR_URL)
    page.wait_for_timeout(1500)
    out_gen = os.path.join(BASE_DIR, "fig_generador_estudio.png")
    page.screenshot(path=out_gen)
    print("Saved:", out_gen)
    
    # ---------------------------------------------------------
    # 4. MOBILE VIEW - APROBADO (PANTALLA COMPLETA & SCROLL)
    # ---------------------------------------------------------
    m_page = browser.new_page(
        viewport={"width": 390, "height": 844},
        device_scale_factor=2,
        is_mobile=True,
        has_touch=True
    )
    m_page.goto(INDEX_URL)
    m_page.wait_for_timeout(1000)
    m_page.evaluate("document.querySelectorAll('.sample-chip')[0].click();")
    m_page.wait_for_timeout(2000)
    
    # Top view (Sensor y Cámara)
    m_page.evaluate("window.scrollTo(0, 0);")
    m_page.wait_for_timeout(300)
    out_m_top = os.path.join(BASE_DIR, "fig_mobile_pantalla1_sensor.png")
    m_page.screenshot(path=out_m_top)
    print("Saved:", out_m_top)

    # Rejection click
    m_page.evaluate("document.querySelectorAll('.sample-chip')[1].click();")
    m_page.wait_for_timeout(2000)

    # Scrolled view (Rechazo y Alarma)
    m_page.evaluate("window.scrollTo(0, 520);")
    m_page.wait_for_timeout(400)
    out_m_mid = os.path.join(BASE_DIR, "fig_mobile_pantalla2_rechazo.png")
    m_page.screenshot(path=out_m_mid)
    print("Saved:", out_m_mid)

    # Bitácora view
    m_page.evaluate("window.scrollTo(0, 950);")
    m_page.wait_for_timeout(400)
    out_m_bot = os.path.join(BASE_DIR, "fig_mobile_pantalla3_bitacora.png")
    m_page.screenshot(path=out_m_bot)
    print("Saved:", out_m_bot)

    browser.close()

print("All precision screenshots captured successfully!")

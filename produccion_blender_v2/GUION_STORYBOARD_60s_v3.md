# Guion storyboard de 60 segundos

## Proyecto

Sistema de control de calidad y trazabilidad OCR para Embutidos Kimby, caso 1.

Esta versión condensa el storyboard original de 150 segundos. El archivo original se conserva sin modificaciones. La escena Blender, sus objetos, materiales, etiquetas, scripts, previews y el proyecto 3D de Higgsfield también se conservan.

## Estructura del plano secuencia

| Tiempo | Imagen y acción | Voz / idea principal |
|---|---|---|
| 0–7 s | Plano aéreo de la línea completa. La cámara entra hacia la estación. | Una falla de impresión puede volver ilegible el lote o la fecha de vencimiento. |
| 7–14 s | Vista cenital del cabezal de codificación. Se marca el lote y la fecha sobre el empaque. | La codificación ocurre antes de que el producto salga al mercado. |
| 14–21 s | Seguimiento del paquete conforme hacia la cámara de visión. Flash estroboscópico. | La cámara captura la etiqueta mientras el producto continúa en movimiento. |
| 21–34 s | La cámara atraviesa el pórtico y entra al módulo OCR. Aparecen recorte, escala de grises, binarización Otsu, regiones de interés, cajas de caracteres y lectura de números. | El preprocesamiento ligero permite leer rápido; la confianza indica si la lectura es segura. |
| 34–41 s | Comparación visual entre `LEÍDO` y `ESPERADO`. El paquete conforme recibe estado ACEPTADO. | Si el formato, la fecha y la confianza son válidos, el producto continúa. |
| 41–52 s | Segundo paquete con impresión borrosa. Los caracteres se fragmentan, baja la confianza y aparece discrepancia. | Una lectura ilegible o dudosa se retiene para revisión y evita una aceptación incorrecta. |
| 52–57 s | El pistón neumático se extiende y desvía el paquete hacia la bandeja roja. | El rechazo ocurre sin detener el flujo principal. |
| 57–60 s | La cámara sale del módulo y muestra la estación completa. | La solución combina visión, reglas de calidad y trazabilidad. |

## Tratamiento visual

- Mantener la cámara como un plano secuencia continuo de 60 segundos.
- Reutilizar la estación, etiquetas y materiales ya construidos en Blender.
- Mantener la velocidad de simulación y la demora cámara-actuador ya definidas en la escena.
- Presentar los estados como simulación didáctica; no atribuir al prototipo una comparación con base de producción que todavía no está implementada en la app.
- Mantener `ACEPTADO`, `RECHAZADO` y `RETENER PARA REVISIÓN` como gráficos controlados para evitar deformaciones generativas.
- La web real puede entrar como monitor dentro de la escena o como composición final breve.

## Producción

1. Extender la animación Blender a 1.800 fotogramas a 30 fps.
2. Añadir el módulo visual interno del OCR y sincronizarlo con la captura de cada paquete.
3. Revisar cámara, etiquetas, contacto del pistón y legibilidad.
4. Renderizar el plano maestro en Blender.
5. Entregar el render real de Blender y conservar el archivo editable.

## Estado actual

- Escena remota y Blender: revisión 21, animación de 60 segundos y 1.800 fotogramas a 30 fps.
- Render Eevee completo: 60.00 segundos, 600 cuadros, 640×360, 10 fps; versión de revisión con ruido visible.
- Macro conforme comprobada en cuadros extraídos del MP4 a los 16 y 18 segundos: LOTE KMB-2026-A01 y VENC 15/12/2026.
- OCR y rechazo son una simulación didáctica.
- Archivo editable, revisiones anteriores y storyboard original de 150 segundos conservados.


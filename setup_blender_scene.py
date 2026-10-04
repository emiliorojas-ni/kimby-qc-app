"""
Script de Automatización 3D para Blender (Python / bpy)
======================================================
Proyecto: Caso 1 - Embutidos Kimby (Control de Calidad & Trazabilidad)
Autor: Antigravity Assistant para Video Híbrido Físico + 3D
Compatibilidad: Blender 3.6 / 4.x / Hixfield MCP

Instrucciones de Uso:
1. Abre Blender con un archivo nuevo.
2. Ve a la pestaña 'Scripting' en la parte superior.
3. Haz clic en 'New', pega este código completo y pulsa 'Run Script' (o tecla Alt + P).
4. El script creará automáticamente:
   - Cinta transportadora industrial de acero inoxidable.
   - Pórtico de inspección con cámara de visión artificial e iluminación anular.
   - Módulo eyector neumático FESTO (pistón con zapata de descarte).
   - Rampa y contenedor de productos rechazados (mermas).
   - 4 empaques de embutidos Kimby con texturas UV automáticas.
   - Animación de transporte, flash de disparo y expulsión neumática del producto defectuoso.
   - Cámara cinematográfica con animación de recorrido de inspección.
"""

import bpy
import os
import math

# -------------------------------------------------------------
# 0. CONFIGURACIÓN DE RUTAS Y PARÁMETROS
# -------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(bpy.data.filepath) if bpy.data.filepath else r"d:\III Pacial 4to Año\kimby_qc_app"
TEXTURE_DIR = os.path.join(SCRIPT_DIR, "etiquetas_blender")

FPS = 30
bpy.context.scene.render.fps = FPS
bpy.context.scene.frame_start = 1
bpy.context.scene.frame_end = 240 # 8 segundos a 30 FPS

# Limpiar objetos existentes para una escena limpia
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Crear Colección Principal Kimby
col_name = "Kimby_QC_Production_Line"
if col_name not in bpy.data.collections:
    kimby_col = bpy.data.collections.new(col_name)
    bpy.context.scene.collection.children.link(kimby_col)
else:
    kimby_col = bpy.data.collections[col_name]

def link_to_col(obj):
    if obj.name in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.unlink(obj)
    if obj.name not in kimby_col.objects:
        kimby_col.objects.link(obj)

# -------------------------------------------------------------
# 1. MATERIALES BÁSICOS
# -------------------------------------------------------------
def get_or_create_mat(name, color=(0.8, 0.8, 0.8, 1.0), metallic=0.0, roughness=0.4):
    mat = bpy.data.materials.get(name)
    if not mat:
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            # Compatibilidad Blender 3.x y 4.x
            if "Base Color" in bsdf.inputs:
                bsdf.inputs["Base Color"].default_value = color
            if "Metallic" in bsdf.inputs:
                bsdf.inputs["Metallic"].default_value = metallic
            if "Roughness" in bsdf.inputs:
                bsdf.inputs["Roughness"].default_value = roughness
    return mat

mat_steel = get_or_create_mat("Industrial_Steel", color=(0.7, 0.72, 0.75, 1.0), metallic=0.9, roughness=0.25)
mat_belt = get_or_create_mat("Belt_Rubber", color=(0.04, 0.08, 0.14, 1.0), metallic=0.1, roughness=0.6)
mat_piston = get_or_create_mat("Piston_Aluminum", color=(0.85, 0.88, 0.9, 1.0), metallic=0.95, roughness=0.15)
mat_pusher = get_or_create_mat("Pusher_POM_Plastic", color=(0.1, 0.45, 0.9, 1.0), metallic=0.0, roughness=0.3)
mat_sensor = get_or_create_mat("Sensor_Housing", color=(0.9, 0.5, 0.05, 1.0), metallic=0.2, roughness=0.3)
mat_reject_bin = get_or_create_mat("Reject_Bin", color=(0.7, 0.1, 0.1, 1.0), metallic=0.0, roughness=0.5)

# -------------------------------------------------------------
# 2. CINTA TRANSPORTADORA (CONVEYOR BELT)
# -------------------------------------------------------------
# Superficie de la banda
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0))
belt = bpy.context.active_object
belt.name = "Conveyor_Belt"
belt.scale = (0.6, 6.0, 0.04)
belt.data.materials.append(mat_belt)
link_to_col(belt)

# Chasis de acero inoxidable
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, -0.06))
frame = bpy.context.active_object
frame.name = "Conveyor_Frame"
frame.scale = (0.66, 6.05, 0.08)
frame.data.materials.append(mat_steel)
link_to_col(frame)

# Guías laterales (barandillas)
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(side * 0.32, 0, 0.06))
    guide = bpy.context.active_object
    guide.name = f"Guide_Rail_{'L' if side < 0 else 'R'}"
    guide.scale = (0.02, 5.8, 0.08)
    guide.data.materials.append(mat_steel)
    link_to_col(guide)

# Patas de soporte
for y_pos in [-2.4, 0.0, 2.4]:
    for x_pos in [-0.3, 0.3]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.8, location=(x_pos, y_pos, -0.45))
        leg = bpy.context.active_object
        leg.name = f"Conveyor_Leg_{x_pos}_{y_pos}"
        leg.data.materials.append(mat_steel)
        link_to_col(leg)

# -------------------------------------------------------------
# 3. PÓRTICO DE VISIÓN ARTIFICIAL & CÁMARA INDUSTRIAL
# -------------------------------------------------------------
# Poste vertical y brazo horizontal
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.45, 0, 0.5))
post = bpy.context.active_object
post.name = "Vision_Post"
post.scale = (0.06, 0.06, 1.0)
post.data.materials.append(mat_steel)
link_to_col(post)

bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.2, 0, 0.95))
arm = bpy.context.active_object
arm.name = "Vision_Arm"
arm.scale = (0.45, 0.06, 0.06)
arm.data.materials.append(mat_steel)
link_to_col(arm)

# Carcasa de la cámara industrial (tipo Basler/Cognex)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 0.85))
cam_body = bpy.context.active_object
cam_body.name = "Industrial_Camera_Body"
cam_body.scale = (0.12, 0.12, 0.14)
cam_body.data.materials.append(mat_sensor)
link_to_col(cam_body)

# Lente óptico
bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.08, location=(0, 0, 0.74))
lens = bpy.context.active_object
lens.name = "Industrial_Lens"
lens.data.materials.append(mat_steel)
link_to_col(lens)

# Anillo de Luz LED (Ring Light Estroboscópico)
bpy.ops.mesh.primitive_torus_add(major_radius=0.08, minor_radius=0.015, location=(0, 0, 0.72))
ring_light = bpy.context.active_object
ring_light.name = "LED_Ring_Light"
mat_led = get_or_create_mat("LED_Ring_Mat", color=(1.0, 1.0, 1.0, 1.0), roughness=0.1)
ring_light.data.materials.append(mat_led)
link_to_col(ring_light)

# Luz puntual para el Flash de inspección
bpy.ops.object.light_add(type='POINT', radius=0.05, location=(0, 0, 0.7))
strobe_light = bpy.context.active_object
strobe_light.name = "Strobe_Inspection_Flash"
strobe_light.data.energy = 5.0 # Base tenue
strobe_light.data.color = (0.9, 0.95, 1.0)
link_to_col(strobe_light)

# -------------------------------------------------------------
# 4. MÓDULO ACTUADOR DE RECHAZO (PISTÓN NEUMÁTICO FESTO)
# -------------------------------------------------------------
# Ubicado a 60 cm después de la cámara en Y = 0.8
piston_y = 0.85

# Cilindro exterior neumático
bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.35, location=(-0.52, piston_y, 0.12))
piston_body = bpy.context.active_object
piston_body.name = "Pneumatic_Cylinder"
piston_body.rotation_euler = (0, math.radians(90), 0)
piston_body.data.materials.append(mat_piston)
link_to_col(piston_body)

# Vástago y zapata de empuje (Objeto que se animará hacia X+)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(-0.35, piston_y, 0.12))
pusher = bpy.context.active_object
pusher.name = "Pneumatic_Pusher_Plate"
pusher.scale = (0.03, 0.22, 0.1)
pusher.data.materials.append(mat_pusher)
link_to_col(pusher)

# Rampa y caja de descarte en el lado opuesto (X = +0.55)
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.65, piston_y, -0.15))
reject_bin = bpy.context.active_object
reject_bin.name = "Reject_Merma_Bin"
reject_bin.scale = (0.4, 0.5, 0.35)
reject_bin.data.materials.append(mat_reject_bin)
link_to_col(reject_bin)

# -------------------------------------------------------------
# 5. CREACIÓN DE PAQUETES DE EMBUTIDOS KIMBY CON TEXTURAS UV
# -------------------------------------------------------------
package_configs = [
    {
        "name": "Kimby_Pack_1_Conforme",
        "tex": "01_conforme_salchicha_viena.png",
        "start_y": -2.2,
        "is_defect": False
    },
    {
        "name": "Kimby_Pack_2_Conforme",
        "tex": "02_conforme_jamon_cocido.png",
        "start_y": -1.2,
        "is_defect": False
    },
    {
        "name": "Kimby_Pack_3_DEFECTO_Borrosa",
        "tex": "05_falla_impresion_borrosa_frotada.png",
        "start_y": -0.2,
        "is_defect": True
    },
    {
        "name": "Kimby_Pack_4_DEFECTO_PinesRotos",
        "tex": "04_falla_cabezal_pines_rotos.png",
        "start_y": 0.8,
        "is_defect": True
    }
]

created_packs = []

for i, cfg in enumerate(package_configs):
    # Crear malla del empaque tipo blister al vacío
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, cfg["start_y"], 0.055))
    pack = bpy.context.active_object
    pack.name = cfg["name"]
    pack.scale = (0.36, 0.24, 0.045)
    
    # Crear material con textura de etiqueta
    mat_pack = bpy.data.materials.new(name=f"Mat_{cfg['name']}")
    mat_pack.use_nodes = True
    bsdf = mat_pack.node_tree.nodes.get("Principled BSDF")
    
    # Ruta de la textura
    tex_path = os.path.join(TEXTURE_DIR, cfg["tex"])
    if os.path.exists(tex_path):
        tex_node = mat_pack.node_tree.nodes.new("ShaderNodeTexImage")
        img = bpy.data.images.load(tex_path)
        tex_node.image = img
        mat_pack.node_tree.links.new(tex_node.outputs["Color"], bsdf.inputs["Base Color"])
    else:
        # Color rojo Kimby de respaldo si aún no se cargó la ruta
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = (0.7, 0.1, 0.1, 1.0)
            
    if "Roughness" in bsdf.inputs:
        bsdf.inputs["Roughness"].default_value = 0.2
    
    pack.data.materials.append(mat_pack)
    link_to_col(pack)
    created_packs.append((pack, cfg))

# -------------------------------------------------------------
# 6. ANIMACIÓN DE LA LÍNEA DE PRODUCCIÓN & RECHAZO NEUMÁTICO
# -------------------------------------------------------------
# La cinta avanza a 0.6 m/s (0.02 m por fotograma)
CONVEYOR_SPEED = 0.025

for pack, cfg in created_packs:
    # Keyframe de movimiento a lo largo del eje Y
    initial_y = cfg["start_y"]
    
    # Frame 1
    pack.location = (0, initial_y, 0.055)
    pack.keyframe_insert(data_path="location", frame=1)
    
    # Momento en que pasa bajo la cámara (Y = 0)
    # y = initial_y + speed * frame => frame_at_camera = -initial_y / speed
    frame_at_camera = int(-initial_y / CONVEYOR_SPEED) + 1
    
    # Momento en que llega frente al pistón neumático (Y = 0.85)
    frame_at_piston = int((piston_y - initial_y) / CONVEYOR_SPEED) + 1
    
    if cfg["is_defect"] and frame_at_piston <= bpy.context.scene.frame_end:
        # Avance hasta el pistón
        p_y = initial_y + CONVEYOR_SPEED * frame_at_piston
        pack.location = (0, p_y, 0.055)
        pack.keyframe_insert(data_path="location", frame=frame_at_piston)
        
        # ¡IMPACTO NEUMÁTICO! El pistón lo empuja a la caja de rechazo
        # Se desplaza violentamente hacia X = +0.65 y cae a Z = -0.15
        push_frame = frame_at_piston + 8
        pack.location = (0.65, p_y + 0.05, -0.15)
        pack.rotation_euler = (math.radians(15), math.radians(-20), math.radians(45))
        pack.keyframe_insert(data_path="location", frame=push_frame)
        pack.keyframe_insert(data_path="rotation_euler", frame=push_frame)
    else:
        # Producto conforme: sigue recto hasta el final de la línea
        end_frame = bpy.context.scene.frame_end
        final_y = initial_y + CONVEYOR_SPEED * end_frame
        pack.location = (0, final_y, 0.055)
        pack.keyframe_insert(data_path="location", frame=end_frame)

# Animación del Pistón Neumático (Golpe de rechazo sincronizado con el Pack 3 defectuoso)
# El Pack 3 llega al pistón en frame:
pack3_cfg = package_configs[2]
f_strike = int((piston_y - pack3_cfg["start_y"]) / CONVEYOR_SPEED) + 1

# Posición de reposo
pusher.location.x = -0.35
pusher.keyframe_insert(data_path="location", frame=f_strike - 2)

# Extensión rápida (disparo neumático a 6 bar)
pusher.location.x = 0.05
pusher.keyframe_insert(data_path="location", frame=f_strike + 4)

# Retracción a posición inicial
pusher.location.x = -0.35
pusher.keyframe_insert(data_path="location", frame=f_strike + 14)

# Animación del Flash Estroboscópico de la Cámara
strobe_light.data.energy = 5.0
strobe_light.data.keyframe_insert(data_path="energy", frame=1)

for cfg in package_configs:
    f_cam = int(-cfg["start_y"] / CONVEYOR_SPEED) + 1
    if 1 < f_cam < bpy.context.scene.frame_end:
        # Pre-flash
        strobe_light.data.energy = 5.0
        strobe_light.data.keyframe_insert(data_path="energy", frame=f_cam - 1)
        # Flashazo
        strobe_light.data.energy = 350.0
        strobe_light.data.keyframe_insert(data_path="energy", frame=f_cam)
        # Post-flash
        strobe_light.data.energy = 5.0
        strobe_light.data.keyframe_insert(data_path="energy", frame=f_cam + 2)

# -------------------------------------------------------------
# 7. CÁMARA CINEMATOGRÁFICA PRINCIPAL CON RECORRIDO
# -------------------------------------------------------------
bpy.ops.object.camera_add(location=(1.4, -1.8, 1.3))
cinematic_cam = bpy.context.active_object
cinematic_cam.name = "Cinematic_QC_Camera"
cinematic_cam.data.lens = 45 # 45mm industrial lens
bpy.context.scene.camera = cinematic_cam

# Apuntar hacia el centro de inspección (0, 0.4, 0.1)
track_empty = bpy.data.objects.new("Camera_Target", None)
kimby_col.objects.link(track_empty)
track_empty.location = (0, 0.4, 0.1)

constraint = cinematic_cam.constraints.new(type='TRACK_TO')
constraint.target = track_empty
constraint.track_axis = 'TRACK_NEGATIVE_Z'
constraint.up_axis = 'UP_Y'

# Keyframes de movimiento de cámara cinematográfico (Travelling orbital)
cinematic_cam.location = (1.5, -1.5, 1.2)
cinematic_cam.keyframe_insert(data_path="location", frame=1)

cinematic_cam.location = (1.2, 0.2, 0.9)
cinematic_cam.keyframe_insert(data_path="location", frame=110)

cinematic_cam.location = (0.7, 1.4, 0.8)
cinematic_cam.keyframe_insert(data_path="location", frame=240)

# Luz de entorno suave tipo fábrica
bpy.ops.object.light_add(type='SUN', location=(3, -2, 5))
sun = bpy.context.active_object
sun.data.energy = 3.0
link_to_col(sun)

print("=" * 60)
print("¡Escena 3D de Embutidos Kimby creada exitosamente en Blender!")
print("Presiona la barra espaciadora para reproducir la animación.")
print("=" * 60)

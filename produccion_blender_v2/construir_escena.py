"""Kimby | editable cinematic prototype. Run in Blender; original app remains untouched.
Local: execute with Blender --background --python construir_escena.py.
Remote runner injects TEXTURE_PAYLOADS containing the two original PNG textures.
"""
import bpy, math, os, json
from mathutils import Vector

FPS=30
SPEED=.6
END=360
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
s=bpy.context.scene
s.render.engine='BLENDER_EEVEE'
s.render.fps=FPS
s.frame_start=1
s.frame_end=END
s.unit_settings.system='METRIC'
s.render.resolution_x=1280
s.render.resolution_y=720
s.render.resolution_percentage=100
if not s.world:s.world=bpy.data.worlds.new('Ambiente fabrica')
s.world.color=(.07,.07,.07)
s['simulation_speed_m_s']=SPEED
s['camera_to_actuator_m']=.9
s['transport_delay_s']=1.5
s['warning']='SIMULACION DIDACTICA. Estados predefinidos; no son resultados OCR.'
s['source']='Etiquetas originales del proyecto. No acredita certificaciones impresas.'

def mat(name,c,metal=0,rough=.4,em=0):
    m=bpy.data.materials.new(name);m.diffuse_color=(*c,1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1)
    p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    if em:p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=em
    return m
steel=mat('Acero satinado',(.38,.46,.52),.8,.3)
dark=mat('Carcasa grafito',(.025,.045,.065),.5)
belt=mat('Banda azul sanitaria',(.025,.12,.18),.1,.6)
red=mat('Kimby rojo',(.55,.025,.035),.2)
white=mat('Tipografia blanca',(.85,.94,1),0,.5)
green=mat('ACEPTADO verde',(.03,.8,.39),0,.3,1)
amber=mat('REVISION ambar',(1,.48,.035),0,.3,1)
alert=mat('RECHAZADO rojo',(1,.045,.035),0,.3,1)
led=mat('LED frio',(.65,.85,1),0,.3,3)
rubber=mat('POM zapata',(.02,.025,.035))
tray=mat('Funda burdeos',(.21,.018,.025),.2,.25)

def cube(name,loc,dim,m,bevel=.02):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=name;o.dimensions=dim
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if m:o.data.materials.append(m)
    if bevel:
        mod=o.modifiers.new('Bordes mecanizados','BEVEL');mod.width=bevel;mod.segments=3
        o.modifiers.new('Normales','WEIGHTED_NORMAL')
    return o
def cyl(name,loc,r,depth,m,rotation=(0,0,0)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=depth,location=loc)
    o=bpy.context.object;o.name=name;o.rotation_euler=rotation;o.data.materials.append(m)
    mod=o.modifiers.new('Cantos','BEVEL');mod.width=.007;mod.segments=2
    for p in o.data.polygons:p.use_smooth=True
    return o
def txt(name,body,loc,size,m,rotation=(0,0,0)):
    cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.size=size;cu.extrude=.0007
    o=bpy.data.objects.new(name,cu);s.collection.objects.link(o);o.location=loc;o.rotation_euler=rotation;o.data.materials.append(m);return o
def key(o,f,loc):o.location=loc;o.keyframe_insert(data_path='location',frame=f)
def linear(o):
    if o.animation_data and o.animation_data.action:
        for slot in o.animation_data.action.slots:
            for layer in o.animation_data.action.layers:
                for strip in layer.strips:
                    bag=strip.channelbag(slot)
                    if bag:
                        for fc in bag.fcurves:
                            for k in fc.keyframe_points:k.interpolation='LINEAR'
def visible(o,start,end):
    for f,v in [(1,True),(max(1,start-1),True),(start,False),(end,False),(end+1,True)]:
        o.hide_render=v;o.keyframe_insert(data_path='hide_render',frame=f)

# Clean factory stage, warm brand and cool inspection light.
cube('Suelo fabrica',(0,0,-.08),(20,22,.12),mat('Suelo',(.075,.10,.13),.25,.5))
cube('Isla tecnica',(0,.3,.015),(4.4,9,.12),dark,.08)
cube('Banda principal',(0,.4,.94),(.72,8,.12),belt)
for x in [-.42,.42]:
    cube('Larguero inox',(x,.4,.87),(.09,8,.18),steel)
    # Outlet gap at the ejector avoids the old rail intersection.
    for y,length in [(-1.45,4.2),(2.95,2.7)]:
        cube('Guia lateral',(x,y,1.065),(.027,length,.045),steel,.01)
for y in [-3.3,-1.2,1.5,4.1]:
    for x in [-.4,.4]:
        cube('Pata perfil',(x,y,.46),(.075,.075,.8),steel,.01)
        cyl('Pie nivelador',(x,y,.095),.07,.05,rubber)
for y in [-3.58,4.38]:cyl('Rodillo extremo',(0,y,.93),.10,.73,steel,(0,math.pi/2,0))
for i in range(40):
    o=cube('Junta movil banda %02d'%i,(0,-3.5+i*.2,1.003),(.70,.007,.002),dark,0)
    key(o,1,tuple(o.location));key(o,11,(0,o.location.y+.2,1.003));linear(o)
    for layer in o.animation_data.action.layers:
        for strip in layer.strips:
            for slot in o.animation_data.action.slots:
                for fc in strip.channelbag(slot).fcurves:fc.modifiers.new('CYCLES')

# Codification is a print head; no sealing jaws.
for x in [-.59,.59]:cube('Codificador columna',(x,-1.2,1.42),(.09,.18,.95),dark)
cube('Codificador puente',(0,-1.2,1.87),(1.25,.2,.13),steel)
cube('Modulo termico lateral',(-.34,-1.2,1.54),(.31,.32,.46),red)
head=cube('Cabezal de codificacion',(0,-1.2,1.21),(.46,.07,.075),dark,.012)
cube('Soporte cabezal',(-.28,-1.2,1.43),(.07,.1,.45),steel)
txt('Rotulo codificacion','01 / CODIFICACION',( -.57,-1.313,1.82),.068,white,(math.pi/2,0,0))

# Open inspection hood lets the camera travel inside.
for x in [-.57,.57]:cube('Vision columna',(x,0,1.49),(.075,.075,1),steel)
cube('Vision travesano',(0,0,1.98),(1.22,.09,.08),steel)
cube('Camara industrial',(0,0,1.79),(.17,.18,.23),dark)
cyl('Objetivo',(0,0,1.61),.06,.14,dark)
cyl('Cristal optico',(0,0,1.535),.048,.008,mat('Cristal lente',(.025,.11,.17),.75,.12))
bpy.ops.mesh.primitive_torus_add(major_radius=.13,minor_radius=.012,location=(0,0,1.52))
bpy.context.object.name='Anillo LED';bpy.context.object.data.materials.append(led)
txt('Rotulo vision','02 / VISION OCR',(-.55,-.055,1.96),.065,white,(math.pi/2,0,0))
cube('Panel control',(-.85,.07,1.44),(.42,.08,.4),dark)
txt('Panel OCR','KIMBY / QC',(-1.03,.022,1.55),.046,white,(math.pi/2,0,0))
txt('Panel estado','SIMULACION',(-1.03,.021,1.47),.039,amber,(math.pi/2,0,0))
txt('Panel velocidad','0.60 m/s',(-1.03,.02,1.39),.04,white,(math.pi/2,0,0))

# Lateral pneumatic unit and open receiving tray.
cyl('Cilindro neumatico',(-.77,.9,1.095),.065,.5,steel,(0,math.pi/2,0))
rod=cyl('Vastago',(-.48,.9,1.095),.022,.43,steel,(0,math.pi/2,0))
push=cube('Zapata neumática',(-.36,.9,1.095),(.035,.4,.14),rubber,.015)
cube('Base actuador',(-.8,.9,.95),(.55,.45,.07),dark)
cube('Bandeja segregacion',(1.03,1.06,.96),(1.3,.8,.07),red)
for y in [.64,1.48]:cube('Pared bandeja',(1.05,y,1.035),(1.3,.035,.16),steel)
cube('Tope bandeja',(1.71,1.06,1.04),(.035,.85,.2),steel)
txt('Rotulo segregacion','RETENIDO / REVISION',(.55,.72,1.007),.068,white)
for x in [.7,1.4]:cube('Pata bandeja',(x,1.1,.5),(.08,.08,.9),steel)

# Two original PNGs, packed unchanged. No generated OCR values.
texture_names=['01_conforme_salchicha_viena.png','05_falla_impresion_borrosa_frotada.png']
images=[]
for fn in texture_names:
    if 'TEXTURE_PAYLOADS' in globals():
        import base64,tempfile
        path=os.path.join(tempfile.gettempdir(),fn)
        with open(path,'wb') as f:f.write(base64.b64decode(TEXTURE_PAYLOADS[fn]))
    else:path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'etiquetas_blender',fn)
    im=bpy.data.images.load(path);im.pack();images.append(im)
    im.filepath='//texturas/'+fn
events=[]
packs=[]
for i,initial in enumerate([-2.4,-5.4]):
    root=bpy.data.objects.new('Paquete %s / %s'%(i+1,'conforme' if i==0 else 'borroso'),None);s.collection.objects.link(root)
    root['predefined_result']='ACEPTADO' if i==0 else 'RECHAZADO — RETENER PARA REVISION'
    p=cube('Envase al vacio %d'%i,(0,0,0),(.5,.34,.09),tray,.028);p.parent=root
    rim=cube('Borde sellado previo %d'%i,(0,0,-.037),(.52,.36,.009),red,.009);rim.parent=root
    bpy.ops.mesh.primitive_plane_add(size=1,location=(0,0,.046));lab=bpy.context.object;lab.name='Etiqueta original %d'%i
    lab.scale=(.48,.32,1);lab.parent=root
    m=mat('PNG original %d'%i,(1,1,1),0,.65);n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=images[i]
    m.node_tree.links.new(n.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color']);lab.data.materials.append(m)
    scan=1+round(-initial/SPEED*FPS);hit=scan+45;printing=scan-60
    # White mask models appearance of code under the head; source texture remains intact.
    mask=cube('Area de codigo antes de imprimir %d'%i,(0,-.01,.0475),(.306,.077,.001),mat('Fondo codigo %d'%i,(1,1,1)),0);mask.parent=root
    for f,y in [(1,1),(printing-3,1),(printing+5,0)]:mask.scale.y=y;mask.keyframe_insert(data_path='scale',frame=f)
    key(root,1,(0,initial,1.046));key(root,hit,(0,.9,1.046))
    if i==0:key(root,END,(0,initial+(END-1)*SPEED/FPS,1.046))
    else:
        key(root,hit+4,(0,.98,1.046));key(root,hit+15,(.87,1.04,1.046));key(root,END,(.94,1.04,1.046))
    linear(root)
    for child in [p,rim,lab,mask]:visible(child, max(1,1+round((-3.5-initial)/SPEED*FPS)), min(END,1+round((4.1-initial)/SPEED*FPS)) if i==0 else END)
    events.append({'package':root.name,'print_frame':printing,'scan_frame':scan,'actuator_frame':hit,'delay_frames':45,'delay_s':1.5,'result':root['predefined_result']})
    packs.append(root)
    # Flat signage facing the main cameras, deliberately simulation-labelled.
    status=txt('Decision %d'%i,'ACEPTADO' if i==0 else 'RECHAZADO',(-.39,.12,1.26),.092,green if i==0 else alert,(math.pi/2,0,0))
    visible(status,scan+2,scan+40)
    sub=txt('Decision nota %d'%i,'ESTADO SIMULADO',(-.32,.119,1.19),.043,white,(math.pi/2,0,0));visible(sub,scan+2,scan+40)
    bpy.ops.object.light_add(type='POINT',location=(0,0,1.43));flash=bpy.context.object;flash.name='Disparo captura %d'%i;flash.data.color=(.68,.85,1)
    for f,e in [(1,0),(scan-1,0),(scan,25),(scan+2,0)]:flash.data.energy=e;flash.data.keyframe_insert(data_path='energy',frame=f)

# Plate contacts left package edge at frame 320; then follows lateral displacement.
hit=events[1]['actuator_frame']
for f,x in [(1,-.36),(hit,-.36),(hit+4,-.268),(hit+15,.602),(hit+19,.602),(hit+31,-.36),(END,-.36)]:
    key(push,f,(x,.9,1.095))
    key(rod,f,((-.52+x-.0175)/2,.9,1.095))
    rod.scale.z=(x-.0175+.52)/.43;rod.keyframe_insert(data_path='scale',frame=f)
linear(push);linear(rod)
# Telescoping housing visually supports the long stroke.
cyl('Guia longa cilindro',(-1.06,.9,1.095),.071,.62,steel,(0,math.pi/2,0))

# Lighting: broad ceiling sources plus motivated camera light.
def area(name,loc,target,power,size,color):
    bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.data.color=color
    o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('Softbox principal',(2,-2,6),(0,0,1),1400,5,(.8,.9,1))
area('Recorte calido',(-3,2,4),(0,0,1),1100,4,(1,.72,.55))
area('Relleno frontal',(0,-5,3),(0,0,1),750,4,(.75,.84,1))
area('Luz lectura',(0,0,1.49),(0,0,1),12,.35,(.8,.9,1))

# Multi-camera edit, continuous process clock. Marker cuts remain editable.
shots=[]
def camera(name,start,end,loc1,loc2,tar1,tar2,lens):
    bpy.ops.object.camera_add(location=loc1);cam=bpy.context.object;cam.name=name;cam.data.lens=lens;cam.data.clip_start=.01;cam.data.clip_end=100
    target=bpy.data.objects.new(name+' / objetivo',None);s.collection.objects.link(target)
    key(cam,start,loc1);key(cam,end,loc2);key(target,start,tar1);key(target,end,tar2)
    con=cam.constraints.new('TRACK_TO');con.target=target;con.track_axis='TRACK_NEGATIVE_Z';con.up_axis='UP_Y'
    linear(cam);linear(target)
    mark=s.timeline_markers.new(name,frame=start);mark.camera=cam;shots.append({'camera':name,'start':start,'end':end})
    return cam
camera('01_Dron_apertura',1,48,(3.7,-5.1,4.3),(2.3,-3.9,3.0),(0,-.1,1),(0,-.6,1.1),37)
camera('02_Cenital_codificacion',49,85,(.02,-1.45,2.9),(.02,-.85,2.5),(0,-1.38,1.05),(0,-.7,1.05),46)
camera('03_Entrada_maquina',86,118,(.45,-1.1,1.48),(.28,-.36,1.38),(0,-.6,1.12),(0,-.03,1.08),30)
camera('04_Macro_aceptado',119,152,(.28,-.23,1.61),(.28,.43,1.61),(0,-.04,1.09),(0,.62,1.09),34)
camera('05_Seguimiento_linea',153,250,(2.4,2.7,2.7),(1.3,-1.4,2.1),(0,.7,1.04),(0,-.45,1.08),40)
camera('06_Macro_borroso',251,289,(.28,-.61,1.62),(.28,.15,1.62),(0,-.4,1.09),(0,.36,1.09),34)
camera('07_Seleccion_neumatica',290,345,(2.7,-.7,2.35),(2.25,-.4,2.05),(0,.9,1.05),(.35,1.04,1.04),48)
camera('08_Dron_cierre',346,360,(2.4,-2.7,3.1),(3.4,-3.7,3.9),(0,.5,1),(0,.5,1),40)
s.camera=bpy.data.objects['01_Dron_apertura']

# Camera-attached minimal editorial overlay, independent from label artwork.
for sh in shots:
    cam=bpy.data.objects[sh['camera']]
    title=txt('Overlay '+sh['camera'],'KIMBY  /  CONTROL DE CALIDAD',(-.30,.151,-1),.013,white)
    title.parent=cam
    foot=txt('Simulacion '+sh['camera'],'SIMULACION 3D  |  0.60 m/s  |  ESTADOS PREDEFINIDOS',(-.30,-.164,-1),.0085,amber)
    foot.parent=cam
    for ob in [title,foot]:visible(ob,sh['start'],sh['end'])

s['event_manifest']=json.dumps(events,ensure_ascii=False)
s['shot_manifest']=json.dumps(shots,ensure_ascii=False)
readme=bpy.data.texts.new('LEEME_KIMBY')
readme.write('Escena editable de 12 s / 360 f / 30 fps. Simulacion a 0.6 m/s. Distancia camara-actuador 0.9 m: demora 1.5 s = 45 f. Dos PNG originales empacados. Estados narrativos, sin OCR ejecutado. Baja confianza: retener y revisar. No es validacion de hardware.\n'+json.dumps(events,ensure_ascii=False,indent=2))
s.frame_set(30)
bpy.ops.file.pack_all()
if 'artifacts' not in globals():
    out=os.path.dirname(os.path.abspath(__file__))
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(out,'KIMBY_linea_cinematica_v2.blend'))
else:
    result={'objects':len(s.objects),'frames':END,'fps':FPS,'events':events,'shots':shots,'packed_images':[(i.name,bool(i.packed_file)) for i in images]}

"""Apply after construir_escena.py. Corrections based on actual rendered previews."""
import bpy, json
s=bpy.context.scene
# Matte unlit print surface protects exact source artwork from washout in macros.
for name in ['PNG original 0','PNG original 1']:
    m=bpy.data.materials[name];nt=m.node_tree
    tex=next(n for n in nt.nodes if n.type=='TEX_IMAGE')
    out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL')
    em=nt.nodes.new('ShaderNodeEmission');em.inputs['Strength'].default_value=.8
    nt.links.new(tex.outputs['Color'],em.inputs['Color']);nt.links.new(em.outputs[0],out.inputs['Surface'])
for o in s.objects:
    if o.name.startswith('Codificador columna') or o.name=='Codificador puente':o.location.y-=.3
    if o.name=='Rotulo codificacion':o.location.y-=.3
    if o.name.startswith('Decision '):
        o.animation_data_clear();o.hide_render=True
    if o.name.startswith('Overlay ') or o.name.startswith('Simulacion '):
        cam=o.parent;half=18/cam.data.lens;depth=.04
        o.location=(-.90*half*depth,(.86 if o.name.startswith('Overlay ') else -.88)*half*.5625*depth,-depth)
        o.data.size=half*(.032 if o.name.startswith('Overlay ') else .022)*depth
        o.data.extrude=0
        o.data.materials.clear();o.data.materials.append(bpy.data.materials['LED frio'] if o.name.startswith('Overlay ') else bpy.data.materials['REVISION ambar'])
for name,frames,locations in [
    ('04_Macro_aceptado',[119,152],[(0,-.49,1.48),(0,.17,1.48)]),
    ('06_Macro_borroso',[251,289],[(0,-.85,1.48),(0,-.09,1.48)])]:
    o=bpy.data.objects[name];o.animation_data_clear();o.data.lens=30
    for f,loc in zip(frames,locations):o.location=loc;o.keyframe_insert(data_path='location',frame=f)
    for layer in o.animation_data.action.layers:
        for strip in layer.strips:
            for slot in o.animation_data.action.slots:
                for fc in strip.channelbag(slot).fcurves:
                    for k in fc.keyframe_points:k.interpolation='LINEAR'
for camname,start,end,body,material in [
    ('04_Macro_aceptado',123,152,'ACEPTADO / SIMULADO','ACEPTADO verde'),
    ('06_Macro_borroso',273,289,'RECHAZADO / SIMULADO','RECHAZADO rojo'),
    ('07_Seleccion_neumatica',290,345,'RECHAZADO / RETENER PARA REVISION','RECHAZADO rojo')]:
    cam=bpy.data.objects[camname];half=18/cam.data.lens;depth=.04
    cu=bpy.data.curves.new('Estado pantalla '+camname,'FONT');cu.body=body;cu.size=half*.040*depth
    o=bpy.data.objects.new(cu.name,cu);s.collection.objects.link(o);o.parent=cam;o.location=(-half*.9*depth,-half*.40*depth,-depth);o.data.materials.append(bpy.data.materials[material])
    for f,v in [(1,True),(start-1,True),(start,False),(end,False),(end+1,True)]:o.hide_render=v;o.keyframe_insert(data_path='hide_render',frame=f)
s.eevee.taa_render_samples=16
s['label_material_note']='Original PNG unchanged; emissive matte display surface for readable educational macros.'
s.frame_set(30)
if 'artifacts' in globals():result={'corrections':['print bridge moved away from top camera','original label image connected to emission to avoid washed-out ink','macro cameras aligned with label','camera-space near-plane status captions'],'frame':30}
else:
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

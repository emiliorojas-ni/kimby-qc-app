import bpy, math, json
s=bpy.context.scene; s.render.fps=30; s.frame_start=1; s.frame_end=1800
s['duration_seconds']=60.0; s['one_shot_master']='Kimby_OneShot_60s'; s['ocr_interior']='Didactic ROI/crop, grayscale, Otsu, boxes, read/expected, confidence'; s['ocr_values']='Controlled simulation labels; production comparison pending'
def M(name,c,em=0):
 m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*c,1);p.inputs['Roughness'].default_value=.4
 if em:p.inputs['Emission Color'].default_value=(*c,1);p.inputs['Emission Strength'].default_value=em
 return m
cyan=M('OCR cyan',(.02,.4,.7),1);white=M('OCR white',(.8,.95,1),1);green=M('OCR accept',(.03,.8,.25),1);amber=M('OCR review',(1,.45,.02),1);red=M('OCR reject',(1,.03,.03),1);panel=M('OCR panel',(.015,.03,.06),.15)
def cube(n,loc,dim,ma):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;o.data.materials.append(ma);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);return o
def text(n,body,loc,size,ma):
 cu=bpy.data.curves.new(n,'FONT');cu.body=body;cu.size=size;cu.extrude=.0005;o=bpy.data.objects.new(n,cu);s.collection.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(ma);return o
def k(o,f,loc):o.location=loc;o.keyframe_insert(data_path='location',frame=f)
for i,(y,label,col) in enumerate([(0.05,'ROI / CROP',cyan),(0.55,'GRAYSCALE',white),(1.05,'OTSU THRESHOLD',amber),(1.55,'OCR BOXES',cyan),(2.05,'LEIDO / ESPERADO',green),(2.55,'CONFIANZA 96%',green)]):
 cube('OCR tunnel panel %02d'%i,(0,y,2.25),(1.45,.035,.72),panel);text('OCR stage %02d'%i,label,(-.61,y-.027,2.48),.085,col);text('OCR micro %02d'%i,'SIMULACION DIDACTICA',(-.61,y-.028,2.25),.048,white)
for i,y in enumerate([.2,.7,1.2,1.7,2.2]):
 b=cube('OCR box %02d'%i,(-.15,y,2.15),(.62,.018,.13),cyan)
 for f,scale in [(1,.1),(630,.1),(720,1),(1020,1),(1080,.1),(1800,.1)]:b.scale.x=scale;b.keyframe_insert(data_path='scale',frame=f)
for body,ma,start,end in [('LEIDO: KMB-2026-A01 | ESPERADO: KMB-2026-A01',green,1020,1230),('ACEPTADO | SIMULACION',green,1020,1230),('LEIDO: KM?-2026-?? | ESPERADO: KMB-2026-A01',amber,1231,1560),('CONFIANZA 38% | RETENER PARA REVISION',red,1231,1560),('RECHAZADO / RETENER',red,1561,1800)]:
 o=text('OCR decision '+body,body,(-.68,2.95,2.25),.065,ma)
 for f,v in [(1,True),(start-1,True),(start,False),(end,False),(end+1,True)]:o.hide_render=v;o.keyframe_insert(data_path='hide_render',frame=f)
bpy.ops.object.camera_add(location=(4.2,-5.2,4.1));cam=bpy.context.object;cam.name='Kimby_OneShot_60s';cam.data.lens=36
target=bpy.data.objects.new('Kimby_OneShot_Target',None);s.collection.objects.link(target)
path=[(1,(4.2,-5.2,4.1),(0,-.4,1)),(210,(1.5,-1.6,2.8),(0,-1.1,1.2)),(420,(.6,-.15,1.7),(0,-.1,1.1)),(630,(.2,0,2.45),(0,.7,2.25)),(1020,(.2,1.65,2.42),(0,1.5,2.25)),(1230,(.9,.55,1.75),(0,.55,1.1)),(1560,(.85,.82,1.8),(0,.85,1.1)),(1710,(2.4,-.1,2.2),(0,.9,1.05)),(1800,(3.5,-3.2,3.5),(0,.4,1))]
for f,loc,t in path:k(cam,f,loc);k(target,f,t)
con=cam.constraints.new('TRACK_TO');con.target=target;con.track_axis='TRACK_NEGATIVE_Z';con.up_axis='UP_Y';s.camera=cam
for name,f in [('Dron',1),('Codificacion',210),('Captura',420),('OCR_Interior',630),('Aceptado',1020),('Borroso',1230),('Rechazo',1560),('Cierre',1710)]:s.timeline_markers.new('60s '+name,frame=f)
s['one_shot_timing']=json.dumps({'dron':'0-7s','codificacion':'7-14s','captura':'14-21s','ocr':'21-34s','aceptado':'34-41s','borroso':'41-52s','piston':'52-57s','cierre':'57-60s'},ensure_ascii=False);s.frame_set(1)
result={'frame_end':s.frame_end,'fps':s.render.fps,'camera':cam.name,'objects':len(s.objects),'ocr_stages':6,'one_shot_timing':s['one_shot_timing']}

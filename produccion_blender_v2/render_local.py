"""Optional Blender 5.2 CLI rendering; run against the delivered .blend.
blender -b KIMBY_linea_cinematica_v2.blend -P render_local.py
Default: six still previews. Set KIMBY_ANIMATIC=1 for a 6 fps draft movie.
"""
import bpy, os
s=bpy.context.scene
out=os.path.join(os.path.dirname(bpy.data.filepath),'renders_locales')
os.makedirs(out,exist_ok=True)
s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100
if os.environ.get('KIMBY_ANIMATIC')=='1':
    s.render.engine='BLENDER_WORKBENCH'
    s.display.shading.light='STUDIO';s.display.shading.color_type='TEXTURE'
    s.render.resolution_x=640;s.render.resolution_y=360
    s.render.fps=6;s.frame_step=5
    s.render.image_settings.media_type='VIDEO'
    s.render.image_settings.file_format='FFMPEG'
    s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264'
    s.render.filepath=os.path.join(out,'animatic_12s_6fps.mp4')
    bpy.ops.render.render(animation=True)
else:
    s.render.engine='BLENDER_EEVEE'
    s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG'
    for f in [30,68,108,137,277,330]:
        s.frame_set(f);s.render.filepath=os.path.join(out,'preview_%03d.png'%f)
        bpy.ops.render.render(write_still=True)

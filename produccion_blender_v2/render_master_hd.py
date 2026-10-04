import bpy, os, time, json
from pathlib import Path
root = Path(bpy.data.filepath).parent
s = bpy.context.scene
s.render.engine = 'BLENDER_EEVEE'
s.render.resolution_x = 1920
s.render.resolution_y = 1080
s.render.resolution_percentage = 100
s.render.fps = 30
s.frame_start = 1
s.frame_end = 1800
s.frame_step = 1
s.eevee.taa_render_samples = 32
s.render.image_settings.media_type = 'IMAGE'
s.render.image_settings.file_format = 'PNG'
s.render.image_settings.color_mode = 'RGB'
mode = os.environ.get('KIMBY_RENDER_MODE', 'test')
if mode == 'test':
    s.frame_set(1590)
    s.render.filepath = str(root / 'rechazo_HD_rev28.png')
    started = time.time()
    bpy.ops.render.render(write_still=True)
    (root / 'hd_benchmark.json').write_text(json.dumps({'seconds': time.time()-started, 'resolution':[1920,1080], 'samples':32}), encoding='utf8')
elif mode == 'physics':
    s.render.resolution_x = 960
    s.render.resolution_y = 540
    s.eevee.taa_render_samples = 8
    s.frame_start = 1531
    s.frame_end = 1650
    s.render.image_settings.media_type = 'VIDEO'
    s.render.image_settings.file_format = 'FFMPEG'
    s.render.ffmpeg.format = 'MPEG4'
    s.render.ffmpeg.codec = 'H264'
    s.render.filepath = str(root / 'rechazo_fluido_rev28.mp4')
    bpy.ops.render.render(animation=True)
else:
    out = root / 'master_hd_frames'
    out.mkdir(exist_ok=True)
    s.render.filepath = str(out / 'frame_')
    s.render.use_overwrite = False
    # Give the laptop GPU brief recovery periods rather than continuous heat.
    def cooling_pause(scene):
        time.sleep(1.0)
    bpy.app.handlers.render_post.append(cooling_pause)
    bpy.ops.render.render(animation=True)





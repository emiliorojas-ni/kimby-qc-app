import subprocess, os, json, time
from pathlib import Path
root = Path(__file__).parent
blender = root / 'render_tools/blender-5.2.2-windows-x64/blender.exe'
ffmpeg = next((root / 'render_tools/imageio_ffmpeg/binaries').glob('*.exe'))
env = os.environ.copy()
env['KIMBY_RENDER_MODE'] = 'master'
status = root / 'master_hd_status.json'
status.write_text(json.dumps({'state':'rendering','started':time.time()}))
with (root / 'master_hd_render.log').open('w', encoding='utf8') as log:
    rc = subprocess.call([str(blender), '-b', str(root/'KIMBY_60s_rev28.blend'), '-P',str(root/'render_master_hd.py')], env=env, stdout=log, stderr=subprocess.STDOUT)
if rc:
    status.write_text(json.dumps({'state':'failed','exit_code':rc}))
    raise SystemExit(rc)
frames = list((root/'master_hd_frames').glob('frame_*.png'))
if len(frames) != 1800:
    status.write_text(json.dumps({'state':'incomplete','frames':len(frames)}))
    raise SystemExit(2)
status.write_text(json.dumps({'state':'encoding','frames':len(frames)}))
video = root/'KIMBY_60s_MASTER_HD_rev28.mp4'
subprocess.run([str(ffmpeg),'-y','-framerate','30','-start_number','1','-i',str(root/'master_hd_frames/frame_%04d.png'),'-c:v','libx264','-crf','17','-preset','slow','-pix_fmt','yuv420p','-movflags','+faststart',str(video)],check=True,stdout=subprocess.DEVNULL,stderr=(root/'master_hd_encode.log').open('w'))
with (root/'master_hd_verify.log').open('w') as log:
    subprocess.run([str(ffmpeg),'-i',str(video),'-f','null','-'],check=True,stdout=log,stderr=log)
status.write_text(json.dumps({'state':'complete','frames':1800,'seconds':60,'resolution':[1920,1080],'fps':30,'path':str(video)}))




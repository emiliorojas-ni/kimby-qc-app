import subprocess
from pathlib import Path
root=Path(__file__).parent
ffmpeg=next((root/'render_tools/imageio_ffmpeg/binaries').glob('*.exe'))
video=root/'KIMBY_60s_MASTER_HD_rev28.mp4'
for name,t in [('macro_HD_16s',16),('macro_HD_18s',18),('OCR_HD_30s',30),('rechazo_HD_53s',53),('retiro_HD_54_5s',54.5),('cierre_HD_59s',59)]:
    subprocess.run([str(ffmpeg),'-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(root/(name+'.png')),'-loglevel','error'],check=True)
subprocess.run([str(ffmpeg),'-y','-ss','51','-i',str(video),'-t','4','-vf','fps=2,scale=480:270,tile=4x2','-frames:v','1',str(root/'rechazo_MASTER_contactos.png'),'-loglevel','error'],check=True)

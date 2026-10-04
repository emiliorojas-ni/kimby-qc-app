from pathlib import Path
import subprocess,json
root=Path(r"D:\III Pacial 4to Año\kimby_qc_app\produccion_blender_v2")
exe=next((root/"render_tools").rglob("*ffmpeg*.exe"))
parts=sorted((root/"eevee_chunks").glob("part_*.mp4"))
(root/"eevee_chunks"/"concat.txt").write_text("\n".join("file '"+p.as_posix()+"'" for p in parts),encoding="utf-8")
out=root/"KIMBY_60s_Eevee_rev21.mp4"
subprocess.run([str(exe),"-y","-v","error","-f","concat","-safe","0","-i",str(root/"eevee_chunks"/"concat.txt"),"-c","copy","-movflags","+faststart",str(out)],check=True)
r=subprocess.run([str(exe),"-i",str(out),"-f","null","-"],capture_output=True,text=True)
(root/"video_verification.log").write_text(r.stderr,encoding="utf-8")
for name,t in [("inicio",1),("macro",16),("macro18",18),("ocr",30),("borrosa",45),("rechazo",53),("cierre",59)]:
 subprocess.run([str(exe),"-y","-v","error","-ss",str(t),"-i",str(out),"-frames:v","1",str(root/(name+"_rev21.png"))],check=True)
print(r.stderr[-1500:])


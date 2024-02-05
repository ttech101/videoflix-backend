import os
import subprocess
import django_rq
from storage.models import uploadMovie

def convert_480p(instance):
    source_name = os.path.splitext(instance.video.path)[0]
    video_name = os.path.splitext(instance.video.name)[0]
    target = source_name + '96647835AA3E5537424ABDB439F6E_480p.mp4'
    # cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(instance.video.path, target)
    subprocess.run(['/usr/bin/ffmpeg', '-i', instance.video.path, '-s', 'hd720', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-strict', '-2',  target])
   # subprocess.run(cmd)
    os.remove(instance.video.path)
    instance.video.name = video_name + '96647835AA3E5537424ABDB439F6E_480p.mp4'
    instance.save()

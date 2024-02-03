import os
import subprocess
import django_rq



def convert(source,instance):
    queue = django_rq.get_queue('default', autocommit=True)
    queue.enqueue(convert_video, source,instance)

def convert_video(source,instance):
    print('video wird nun umgewandelt')
    source_name = os.path.splitext(source)[0]
    print('source geandert ->',source_name)
    target = source_name + '_480p.mp4'
    print('bin ich auch noch hier??? ->>',source)
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    print('check vor cmd befehl ->',cmd)
    subprocess.run(cmd)
    print('umwandel ist abgeschlossen')
    instance.video.name = 'video/' + os.path.basename(source_name + '_480p.mp4')
    instance.save()
    os.remove(source)


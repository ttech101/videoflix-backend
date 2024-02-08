import os
import subprocess
import django_rq
from django.utils import timezone
from storage.models import uploadMovie

def convert_480p(instance):
    """
    Convert uploaded video to 480p resolution.
    This function converts an uploaded video to 480p resolution using ffmpeg.
    Args:
        instance (uploadMovie): The uploadMovie instance representing the uploaded video.
    """
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    duration = get_video_duration(instance.video.path)
    source_name = os.path.splitext(instance.video.path)[0]
    video_name = os.path.splitext(instance.video.name)[0]
    target = source_name + timestamp + '_480p.mp4'
    #subprocess.run(['/usr/bin/ffmpeg', '-i', instance.video.path, '-s', 'hd720', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-strict', '-2',  target])
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(instance.video.path, target)
    subprocess.run(cmd)
    os.remove(instance.video.path)
    instance.video.name = video_name + timestamp + '_480p.mp4'

    if instance.automatic_cover:
        middle_time = duration / 5
        middle_time_str = '{:0.3f}'.format(middle_time)
        video_path = instance.video.path.replace("\\video\\", "\\cover\\")
        video_path_without_extension = os.path.splitext(video_path)[0]
        target = video_path_without_extension  + '.png'
        #subprocess.run(['/usr/bin/ffmpeg', '-i', instance.video.path, '-ss' , middle_time_str,'-frames:v' , '1' ,'-vf', 'scale=iw/2:ih/2' ,target])
        cmd ='ffmpeg -i "{}" -ss "{}" -frames:v 1 -vf scale=iw/2:ih/2 "{}"'.format(instance.video.path,middle_time_str, target)
        subprocess.run(cmd)
        sliced_path = target.split("media\\", 1)[1]
        instance.cover.name = sliced_path

    if instance.automatic_image:
        middle_time = duration / 2
        middle_time_str = '{:0.3f}'.format(middle_time)
        video_path = instance.video.path.replace("\\video\\", "\\big_picture\\")
        video_path_without_extension = os.path.splitext(video_path)[0]
        target = video_path_without_extension  +   '.png'
        #subprocess.run(['/usr/bin/ffmpeg', '-i', instance.video.path, '-ss' , middle_time_str,'-frames:v' , '1',target])
        cmd ='ffmpeg -i "{}" -ss "{}" -frames:v 1 "{}"'.format(instance.video.path,middle_time_str, target)
        subprocess.run(cmd)
        sliced_path = target.split("media\\", 1)[1]
        instance.big_picture.name = sliced_path
        instance.convert_status = 2

    instance.save()

def get_video_duration(video_path):
    """
    Get the duration of a video file.
    This function retrieves the duration of a video file using ffprobe.
    Args:
        video_path (str): The path to the video file.
    Returns:
        float: The duration of the video in seconds.
    """
    cmd = ['ffprobe', '-i', video_path, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']
    duration_str = subprocess.check_output(cmd).decode('utf-8').strip()
    duration = float(duration_str)
    return duration
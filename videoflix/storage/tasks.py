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
    target_video = source_name + timestamp + '_480p.mp4'
    subprocess.run(['/usr/bin/ffmpeg', '-i', instance.video.path, '-s', 'hd720', '-c:v', 'libx264', '-crf', '23', '-c:a', 'aac', '-strict','-aspect ASPECT', '-2',  target_video])
    #cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(instance.video.path, target)
    #subprocess.run(cmd)
    os.remove(instance.video.path)
    instance.video.name = video_name + timestamp + '_480p.mp4'


    if instance.automatic_cover:
        target_cover= target_video
        middle_time = duration / 5
        middle_time_str = '{:0.3f}'.format(middle_time)
        cover_path = target_cover.replace("/video/", "/cover/")
        cover_path_without_extension = os.path.splitext(cover_path)[0]
        cover_target = cover_path_without_extension  + '.png'
        subprocess.run(['/usr/bin/ffmpeg', '-i', target_cover, '-ss' , middle_time_str,'-frames:v' , '1' ,'-vf', 'scale=iw/2:ih/2' ,cover_target])
        #cmd ='ffmpeg -i "{}" -ss "{}" -frames:v 1 -vf scale=iw/2:ih/2 "{}"'.format(instance.video.path,middle_time_str, target)
        #subprocess.run(cmd)
        basis_pfad_cover = "/home/tt/projekte/videoflix-backend/videoflix/media/"
        date_path_cover = os.path.relpath(cover_target, basis_pfad_cover)
        instance.cover.name = date_path_cover

    if instance.automatic_image:
        target_image= target_video
        middle_time = duration / 2
        middle_time_str = '{:0.3f}'.format(middle_time)
        image_path = target_image.replace("/video/", "/big_picture/")
        image_path_without_extension = os.path.splitext(image_path)[0]
        image_target = image_path_without_extension  +   '.png'
        subprocess.run(['/usr/bin/ffmpeg', '-i', target_image, '-ss' , middle_time_str,'-frames:v' , '1',image_target])
        #cmd ='ffmpeg -i "{}" -ss "{}" -frames:v 1 "{}"'.format(instance.video.path,middle_time_str, target)
        #subprocess.run(cmd)
        basis_pfad_image = "/home/tt/projekte/videoflix-backend/videoflix/media/"
        date_path_image = os.path.relpath(image_target, basis_pfad_image)
        instance.big_picture.name = date_path_image

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
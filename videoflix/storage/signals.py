import os
from django.dispatch import receiver
from storage.models import uploadMovie
from django.db.models.signals import post_delete,post_save
import django_rq
from storage.tasks import convert_480p


@receiver(post_delete, sender=uploadMovie)
def delete_upload_movie_files(sender, instance, **kwargs):
    print('Signale würde gelöscht!')
    if instance.cover:
        os.remove(instance.cover.path)
    if instance.big_picture:
        os.remove(instance.big_picture.path)
    if instance.video:
        os.remove(instance.video.path)

@receiver(post_save, sender=uploadMovie)
def video_post_save(sender, instance, created, **kwargs):
    if instance.movie_name:
        if instance.convert_status is 0:
            print('start convert_480p')
            instance.convert_status = 1
            instance.save()
            queue = django_rq.get_queue('default', autocommit=True)
            # queue.enqueue(generate_cover,instance)
            # queue.enqueue(generate_image,instance)
            queue.enqueue(convert_480p,instance)







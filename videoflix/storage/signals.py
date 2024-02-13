import os
from django.dispatch import receiver
from storage.models import uploadMovie
from django.db.models.signals import post_delete,post_save
import django_rq
from storage.tasks import convert_480p


@receiver(post_delete, sender=uploadMovie)
def delete_upload_movie_files(sender, instance, **kwargs):
    """
    Signal receiver function to delete associated files when an uploadMovie instance is deleted.
    """
    if instance.cover and instance.cover.name is not 'static/load-142_256.gif':
        os.remove(instance.cover.path)
    if instance.big_picture:
        os.remove(instance.big_picture.path)
    if instance.video:
        os.remove(instance.video.path)

@receiver(post_save, sender=uploadMovie)
def video_post_save(sender, instance, created, **kwargs):
    """
    Signal receiver function to initiate video conversion when an uploadMovie instance is saved.
    """
    if instance.movie_name:
        if instance.convert_status is 0:
            instance.convert_status = 1
            instance.save()
            queue = django_rq.get_queue('default', autocommit=True)
            queue.enqueue(convert_480p,instance)







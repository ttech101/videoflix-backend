import os
from django.dispatch import receiver
from storage.models import uploadMovie
from django.db.models.signals import post_delete



@receiver(post_delete, sender=uploadMovie)
def delete_upload_movie_files(sender, instance, **kwargs):
    print('ich glaub das funktioniert')
    if instance.cover:
        os.remove(instance.cover.path)
    if instance.big_picture:
        os.remove(instance.big_picture.path)
    if instance.video:
        os.remove(instance.video.path)
from time import process_time_ns
from tokenize import Exponent
from cv2 import exp
from django.dispatch import receiver
from django.db.models.signals import(
    post_save    
)
from django.contrib.auth import get_user_model
import face_recognition
from django.db import connection

MyUser = get_user_model()

@receiver(post_save, sender=MyUser)
def user_pos_save(instance, sender, **kwargs):
    if not instance.image:
        return
    if instance.is_valid:
        return

    face_image = face_recognition.load_image_file(instance.image)
    list_encodings = face_recognition.face_encodings(face_image)
    
    if len(list_encodings) != 1:
        return
    
    encodings = list_encodings[0]
    with connection.cursor() as cusor:
        cusor.execute(
            (
            """UPDATE accounts_myuser 
                SET vec_low=cube(array[{}]),
                    vec_high=cube(array[{}]), 
                    is_valid=true 
            WHERE id = {}
            """.format(
                ','.join(str(s) for s in encodings[0:64]),
                ','.join(str(s) for s in encodings[64:128]),
                instance.pk
                ))
            )
        cusor.close()
        
        
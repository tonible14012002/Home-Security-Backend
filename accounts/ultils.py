from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
import face_recognition

MyUser = get_user_model()

class IsAdminOrAccountOwner(BasePermission):
    def has_permission(self, request, view):
        return  (request.user 
                 and (view.action in ['retrieve', 'update'] 
                     or request.user.is_staff))
        
    def has_object_permission(self, request, view, obj):
        if not request.user:
            return False
        return request.user.is_staff or request.user == obj

def detect_face(upload_img):
    img = face_recognition.load_image_file(upload_img)
    face_locations = face_recognition.face_locations(img)
    encodings = face_recognition.face_encodings(img, face_locations)[0]

    threshold = 0.5

    users = MyUser.objects.raw( 
        """
        SELECT username, id FROM accounts_myuser 
        WHERE sqrt(power(CUBE(array[{}]) <-> vec_low, 2) 
                + power(CUBE(array[{}]) <-> vec_high, 2)) <= {}
        """.format(
            ','.join(str(s) for s in encodings[0:64]),
            ','.join(str(s) for s in encodings[64:128]),
            threshold
            ) +  
        """ORDER BY 
            sqrt(power(CUBE(array[{}]) <-> vec_low, 2) 
                + power(CUBE(array[{}]) <-> vec_high, 2)) ASC LIMIT 1
        """.format(
            ','.join(str(s) for s in encodings[0:64]),
            ','.join(str(s) for s in encodings[64:128]),
            )
    )   
    return users

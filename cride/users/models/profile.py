from django.db import models

from utils.models import CRideModel

class Profile(CRideModel):
    """Profile model

    El perfil va a contener la informacion publica del usuario
    como foto de perfil, biografia o estadisticas
    """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    biography = models.TextField(max_length=500, blank=True)
    picture = models.ImageField(
        'profile_pic',
        upload_to='users/pictures/',
        blank=True,
        null=True
    )
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)
    reputation = models.FloatField(
        default=5.0,
        help_text="la reputacion depende de las rides tomadas"
    )

    def __str__(self):
        return str(self.user)
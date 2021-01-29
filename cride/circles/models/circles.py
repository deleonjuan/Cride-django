from django.db import models
from utils.models import CRideModel

class Circle(CRideModel):
    """ circle model
    un circulo es un grupo privado
    """
    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)

    about = models.CharField('circle desription', max_length=155)
    picture = models.ImageField(upload_to='circles/pictures/', blank=True, null=True)

    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)

    is_verified = models.BooleanField(
        'verified_circle',
        default=False,
        help_text="los circulos verificados son tomados como oficiales"
    )

    is_public = models.BooleanField(
        default=True,
        help_text="los circulos publicos no aparecen visibles para todo el publico"
    )

    is_limited = models.BooleanField(
        default=False,
        help_text="los cirulos limitados solo pueden atender una cierta cantidad de usuarios"
    )

    members_limit = models.PositiveIntegerField(
        default=0
        help_text="numero de usuarios al que esta limitado el circulo"
    )

    def __str__(self):
        return self.name

    class Meta(CRideModel.Meta):
        ordering = ['-rides_taken', '-rides_offered']

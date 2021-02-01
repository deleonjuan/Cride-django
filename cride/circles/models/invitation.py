from django.db import models

from utils.models import CRideModel
from circles.managers import InvitationManager

class Invitation(CRideModel):

    code = models.CharField(max_length=50, unique=True)

    issued_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='issued_by'
    )

    used_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        null=True
    )

    circle = models.ForeignKey('circles.circle', on_delete=models.CASCADE)

    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(blank=True, null=True)

    # manager
    objects = InvitationManager()

    def __str__(self):
        return '#{}: {}'.format(self.circle.slug_name, self.code)
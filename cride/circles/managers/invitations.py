

from django.db import models

import random
from string import ascii_uppercase, digits

class InvitationManager(models.Manager):

    CODE_LENGTH = 10

    def create(self, **kwards):
        pool = ascii_uppercase + digits + '.-'
        code = kwards.get('code', ''.join(random.choices(pool, k=self.CODE_LENGTH)))
        while self.filter(code = code).exists():
            code = ''.join(random.choices(pool, k=self.CODE_LENGTH))

        kwards['code'] = code
        return super(InvitationManager, self).create(**kwards)
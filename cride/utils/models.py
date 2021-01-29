from django.db import models

class CRideModel(models.Model):
        created = models.DateTimeField(
            'created_at', 
            auto_now_add=True, 
            help_text='Date time on which the object was created'
        )
        modified = models.DateTimeField(
            'modified_at',
            auto_now=True,
            help_text='Date time on which the object was last modified'
        )

        class Meta:
            """ 
            meta data
            abstract = True impide que el modelo se cree en la base de datos
            este modelo es solo para herencia y no necesita ser migrado
            """
            abstract = True
            get_latest_by = 'created'
            ordering = ['-created', '-modified',]


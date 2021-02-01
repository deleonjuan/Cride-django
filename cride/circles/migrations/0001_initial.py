# Generated by Django 3.1.5 on 2021-02-01 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created_at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified', verbose_name='modified_at')),
                ('name', models.CharField(max_length=140, verbose_name='circle name')),
                ('slug_name', models.SlugField(max_length=40, unique=True)),
                ('about', models.CharField(max_length=155, verbose_name='circle desription')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='circles/pictures/')),
                ('rides_offered', models.PositiveIntegerField(default=0)),
                ('rides_taken', models.PositiveIntegerField(default=0)),
                ('is_verified', models.BooleanField(default=False, help_text='los circulos verificados son tomados como oficiales', verbose_name='verified_circle')),
                ('is_public', models.BooleanField(default=True, help_text='los circulos publicos no aparecen visibles para todo el publico')),
                ('is_limited', models.BooleanField(default=False, help_text='los cirulos limitados solo pueden atender una cierta cantidad de usuarios')),
                ('members_limit', models.PositiveIntegerField(default=0, help_text='numero de usuarios al que esta limitado el circulo')),
            ],
            options={
                'ordering': ['-rides_taken', '-rides_offered'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created_at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified', verbose_name='modified_at')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('is_used', models.BooleanField(default=False)),
                ('used_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the object was created', verbose_name='created_at')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Date time on which the object was last modified', verbose_name='modified_at')),
                ('is_admin', models.BooleanField(default=False, help_text='los admins tienene el control de los circulos', verbose_name='circle_admin')),
                ('used_invitations', models.PositiveSmallIntegerField(default=0)),
                ('remaining_invitations', models.PositiveSmallIntegerField(default=0)),
                ('rides_taken', models.PositiveIntegerField(default=0)),
                ('rides_offered', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True, verbose_name='active_status')),
                ('circle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='circles.circle')),
            ],
            options={
                'ordering': ['-created', '-modified'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
    ]

from django.conf import settings
from rest_framework import serializers 
from django.contrib.auth import authenticate, password_validation
from django.utils import timezone
from datetime import timedelta

from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator

from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string

from users.models import User, Profile
from rest_framework.authtoken.models import Token
import jwt


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'username', 'first_name', 'last_name', 'phone_number', 'email', )


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])

        if not user:
            raise serializers.ValidationError('credenciales invalidas')
        if not user.is_verified:
            raise serializers.ValidationError('el usuario no esta verificado')

        self.context['user'] = user
        return data

    def create(self, data):
        """ generar u obtener nuevo token """
        token, created = Token.objects.get_or_create(user=self.context['user'])

        return self.context['user'], token.key


class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_regex = RegexValidator(
        regex = r'\+?1?\d{8,15}$',
        message='El telefono debe cumplir el formato +111111111'
    )
    phone_number = serializers.CharField(validators=[phone_regex], max_length=17)

    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    first_name = serializers.CharField(min_length=2, max_length=64)
    last_name = serializers.CharField(min_length=2, max_length=64)

    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']

        if passwd != passwd_conf:
            raise serializers.ValidationError("las contrasenias deben coincidir")

        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=True)
        Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        verification_token = self.gen_verification_token(user)
        print(verification_token)

        # subject = 'welcome'
        # from_email = 'Mailgun Sandbox <postmaster@sandbox9b5fdd2743f244bab535e42f1ae80e8a.mailgun.org>'
        # content = "hey"#{'token' : verification_token, 'user':user}
        # # content = render_to_string(
        # #     'emails/user.account_verification.html',
        # #     {'token' : verification_token, 'user': user}
        # # )

        # # # msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        # msg = send_mail(subject, content, from_email, [user.email])
        # msg.attach_alternative(content, 'text/html')
        # msg.send()

    def gen_verification_token(self, user):
        exp_data = timezone.now() + timedelta(days = 3)
        payload = {
            'user': user.username,
            'exp': int(exp_data.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token


class AccountVerificationSerializer(serializers.Serializer):
    """ verification serializer """

    token = serializers.CharField()

    def validate_token(self, data):
        """ token is valid """
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('token expirado')
        except jwt.PyJWTError:
            raise serializers.ValidationError('invalid token')

        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('invalid token')

        self.context['payload'] = payload
        return data

    def save(self):
        """ update """
        payload = self.context['payload']
        user = User.objects.get(username = payload['user'])
        user.is_verified = True
        user.save()

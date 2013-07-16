from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from bars.models import Bar

def validate_email_unique(email):
    exists = User.objects.filter(email=email)
    if exists:
        raise ValidationError('Email address {} already exists'.format(email))

def validate_bar_unique(bar):
    try:
        exists = Bar.objects.get(name=bar.name, city=bar.city, state=bar.state, zip_code=bar.zip_code)
        if exists:
            raise ValidationError('Bar already exists.')
    except Bar.DoesNotExist:
        pass

import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    year_now = datetime.date.today().year
    if (value < 0) and (value > year_now):
        raise ValidationError('Введите корректный год')
    return value

import random
import string
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def generate_password(nom, prenom):
    pwd = nom[:3] + prenom[:3] + ''.join(str(random.randint(0, 9)) for _ in range(5))
    return pwd


def format_phone_number(value):
    value = value.replace("+1", "")
    formatted_phone = f'{value[:3]} {value[3:6]}-{value[6:]}'
    return formatted_phone


def check_date_birthday(birthday):
    if isinstance(birthday, str):
        try:
            birthday = datetime.strptime(birthday, "%Y-%m-%d").date()  # Format de date: 'YYYY-MM-DD'
        except ValueError:
            raise ValueError("Le format de la date est incorrect. Utilisez 'YYYY-MM-DD'.")

    age_limit = timezone.now().date() - relativedelta(years=18)
    if birthday > age_limit:
        return True
    return False


def generate_random_password(length=12, use_special_chars=True):
    # Définir les caractères de base : lettres et chiffres
    characters = string.ascii_letters + string.digits

    if use_special_chars:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    return password
from django import template

register = template.Library()

@register.filter
def format_solde(value):
    if value is None:
        return ""
    try:
        formatted_value = "{:,.2f}".format(float(value)).replace(",", " ")
        return formatted_value
    except (ValueError, TypeError):
        return value


@register.filter
def format_carte_credit(card_number):
    card_number = str(card_number).replace(" ", '')

    if len(card_number) != 16:
        return card_number  # Si le numéro n'est pas de 16 chiffres, retournez-le sans changement

    # Formater le numéro avec les parties visibles et cachées
    formatted_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return formatted_number
from celery import shared_task

from product.models import Product
from utils.sms import SMS
from user_management.models import Manager

@shared_task
def send_restock_and_sales_notification():
    phone_numbers = Manager.objects.values_list('phone', flat=True)

    products_list = list(Product.objects.needs_restock().values_list('name', flat=True))

    message = f"""
    Hi Manager this is the list of products that need restock:
    {products_list}

    """
    for phone in phone_numbers:
        sms = SMS(phone_number=phone, message=message)
        sms.send()
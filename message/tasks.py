from celery import shared_task
from insurance.models import Insurance
from .services import send_sms_service

@shared_task
def check_insurance_expiry():
    # Muddati 5 kun qolgan barcha sug'urtalarni filter qilamiz
    insurances = Insurance.objects.filter(remaining_days=5)

    for insurance in insurances:
        phone = insurance.phone_number
        message = f"Hurmatli mijoz, sug'urtangiz muddati tugashiga 5 kun qoldi."

        # SMS yuborish funksiyasini chaqiramiz
        send_sms_service(phone, message)

    return f"{insurances.count()} ta mijozga ogohlantirish yuborildi."
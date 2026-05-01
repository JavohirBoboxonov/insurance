import requests
import logging

logger = logging.getLogger(__name__)


def send_sms_service(phone_number, message):
    """
    Eskiz API orqali SMS yuborish funksiyasi
    """
    # 1. Eskiz.uz dan olingan Token (Buni .env faylda saqlash tavsiya etiladi)
    ESKIZ_TOKEN = "SIZNING_MAXFIY_TOKENINGIZ"
    URL = "https://notify.eskiz.uz/api/message/sms/send"

    # 2. Telefon raqam formatini tekshirish (faqat raqamlar qolishi kerak)
    # Masalan: +998901234567 -> 998901234567
    clean_phone = "".join(filter(str.isdigit, str(phone_number)))

    payload = {
        'mobile_phone': clean_phone,
        'message': message,
        'from': '4545',  # Eskiz tomonidan berilgan nickname yoki raqam
    }

    headers = {
        'Authorization': f'Bearer {ESKIZ_TOKEN}'
    }

    try:
        response = requests.post(URL, data=payload, headers=headers)

        if response.status_code == 200:
            logger.info(f"SMS muvaffaqiyatli yuborildi: {clean_phone}")
            return response.json()
        else:
            logger.error(f"SMS yuborishda xato: {response.text}")
            return None

    except Exception as e:
        logger.error(f"SMS servis bilan bog'lanishda xato yuz berdi: {e}")
        return None
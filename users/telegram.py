import hmac
import hashlib
import time
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest


def telegram_callback(request):
    data = request.GET.dict()
    hash_check = data.pop('hash', None)

    data_check_list = [f"{k}={v}" for k, v in sorted(data.items())]
    data_check_string = "\n".join(data_check_list)

    secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
    hmac_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if hmac_hash != hash_check or (time.time() - int(data['auth_date'])) > 86400:
        return HttpResponseBadRequest("Ma'lumotlar xato yoki eskirgan.")

    user, created = User.objects.get_or_create(
        username=f"tg_{data['id']}",
        defaults={'first_name': data.get('first_name', '')}
    )

    login(request, user)
    return redirect('home')
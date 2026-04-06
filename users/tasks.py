import hashlib
import logging
from celery import shared_task
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

def get_cache_keys(phone_number: str) -> dict:
    hashed = hashlib.md5(phone_number.encode()).hexdigest()
    return {
        'attempts': f'login_attempts_{hashed}',
        'blocked':  f'login_blocked_{hashed}',
    }

@shared_task(bind=True, max_retries=3)
def register_failed_login(self, phone_number: str):
    try:
        block_seconds = settings.LOGIN_BLOCK_HOURS * 60 * 60
        max_attempts = settings.LOGIN_MAX_ATTEMPTS
        keys = get_cache_keys(phone_number)

        attempts = cache.get(keys['attempts'], 0) + 1
        cache.set(keys['attempts'], attempts, timeout=block_seconds)

        logger.warning(f"Noto'g'ri urinish | raqam: {phone_number} | son: {attempts}")

        if attempts >= max_attempts:
            cache.set(keys['blocked'], True, timeout=block_seconds)
            cache.delete(keys['attempts'])

            unblock_user.apply_async(
                args=[phone_number],
                countdown=block_seconds
            )

            logger.warning(
                f"BLOKLANDI | raqam: {phone_number} | "
                f"{settings.LOGIN_BLOCK_HOURS} soatga"
            )

    except Exception as exc:
        logger.error(f"register_failed_login xatosi: {exc}")
        raise self.retry(exc=exc, countdown=5)


@shared_task(bind=True, max_retries=3)
def unblock_user(self, phone_number: str):
    try:
        keys = get_cache_keys(phone_number)
        cache.delete(keys['blocked'])
        cache.delete(keys['attempts'])

        logger.info(f"Blok ochildi | raqam: {phone_number}")

    except Exception as exc:
        logger.error(f"unblock_user xatosi: {exc}")
        raise self.retry(exc=exc, countdown=10)


@shared_task
def clear_successful_login(phone_number: str):
    keys = get_cache_keys(phone_number)
    cache.delete(keys['attempts'])
    cache.delete(keys['blocked'])
    logger.info(f"login raqam: {phone_number}")
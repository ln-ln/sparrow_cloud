import os
import logging
from django.core.cache import cache
from sparrow_cloud.utils.get_hash_key import get_hash_key
from sparrow_cloud.utils.get_settings_value import get_settings_value
from sparrow_cloud.restclient import rest_client

logger = logging.getLogger(__name__)


def get_user_token(user_id):
    """
    get user token
    REGISTRY_APP_CONF = {
        "SERVICE_ADDRESS": "sparrow-service-svc:8000",
        "PATH": "/api/get_app_token/",
        "ENABLE_TOKEN_CACHE": os.environ.get("ENABLE_TOKEN_CACHE", False)
    }
    :param user_id:
    :return:
    """
    user_token_key = get_hash_key(key_type="user", user_id=user_id)
    registry_app_conf = get_settings_value("REGISTRY_APP_CONF")
    enable_get_token_cache = registry_app_conf["ENABLE_TOKEN_CACHE"]
    if enable_get_token_cache:
        cache_user_token = cache.get(user_token_key)
        if cache_user_token:
            return cache_user_token["user_token"]
    try:
        data = {
            "uid": user_id
        }
        user_token = rest_client.post(service_address=registry_app_conf["SERVICE_ADDRESS"], api_path=registry_app_conf["PATH"], data=data)
        cache.set(user_token_key, {'user_token': user_token}, timeout=user_token["expires_at"]-120)
        return user_token
    except Exception as ex:
        raise Exception('get_user_token error, no token available in cache and registry_app_error, '
                        'message:{}'.format(ex.__str__()))


def get_app_token():
    """
    get app token
    REGISTRY_APP_CONF = {
        "SERVICE_ADDRESS": "sparrow-service-svc:8000",
        "PATH": "/api/get_app_token/",
        "ENABLE_TOKEN_CACHE": os.environ.get("ENABLE_TOKEN_CACHE", False)
    }
    :return:
    """
    app_token_key = get_hash_key(key_type="app")
    service_conf = get_settings_value("SERVICE_CONF")
    registry_app_conf = get_settings_value("REGISTRY_APP_CONF")
    enable_get_token_cache = registry_app_conf["ENABLE_TOKEN_CACHE"]
    if enable_get_token_cache:
        cache_app_token = cache.get(app_token_key)
        if cache_app_token:
            return cache_app_token["app_token"]
    try:
        app_token = rest_client.post(service_address=registry_app_conf["SERVICE_ADDRESS"],
                                     api_path=registry_app_conf["PATH"], data=service_conf)
        cache.set(app_token_key, {'app_token': app_token}, timeout=app_token["expires_at"]-120)
        return app_token
    except Exception as ex:
        raise Exception('get_app_token error, no token available in cache and registry_app_error, '
                        'message:{}'.format(ex.__str__()))


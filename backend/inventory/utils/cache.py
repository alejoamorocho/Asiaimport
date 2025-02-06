from django.core.cache import cache
from django.conf import settings
from functools import wraps
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
import hashlib
import json

def cache_response(timeout=None, key_prefix=''):
    """
    Decorador para cachear respuestas de viewsets.
    
    Args:
        timeout (int): Tiempo de vida del caché en segundos
        key_prefix (str): Prefijo para la clave de caché
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(viewset: ViewSet, request, *args, **kwargs):
            # No cachear para métodos no seguros
            if request.method not in ['GET', 'HEAD', 'OPTIONS']:
                return view_func(viewset, request, *args, **kwargs)

            # Construir clave de caché
            cache_key = _build_cache_key(
                view_func.__name__,
                request,
                key_prefix,
                viewset.__class__.__name__
            )

            # Intentar obtener del caché
            response_data = cache.get(cache_key)
            if response_data is not None:
                return Response(response_data)

            # Si no está en caché, ejecutar vista
            response = view_func(viewset, request, *args, **kwargs)
            
            # Cachear solo respuestas exitosas
            if response.status_code == 200:
                cache.set(
                    cache_key,
                    response.data,
                    timeout or settings.CACHE_TTL
                )

            return response
        return _wrapped_view
    return decorator

def _build_cache_key(view_name, request, prefix, viewset_name):
    """
    Construye una clave de caché única basada en la petición.
    """
    # Datos base para la clave
    key_parts = {
        'view_name': view_name,
        'viewset': viewset_name,
        'path': request.path,
        'query': request.GET.dict(),
        'user_id': request.user.id if request.user.is_authenticated else 'anonymous',
    }

    # Serializar y hashear
    key_string = json.dumps(key_parts, sort_keys=True)
    key_hash = hashlib.md5(key_string.encode()).hexdigest()

    return f"{settings.CACHE_KEY_PREFIX}:{prefix}:{key_hash}"

def invalidate_cache_patterns(*patterns):
    """
    Invalida patrones de caché específicos.
    
    Args:
        patterns (tuple): Patrones de clave a invalidar (usando *)
    """
    for pattern in patterns:
        keys = cache.keys(f"{settings.CACHE_KEY_PREFIX}:{pattern}")
        if keys:
            cache.delete_many(keys)

def clear_model_cache(model_name):
    """
    Limpia todo el caché relacionado con un modelo específico.
    
    Args:
        model_name (str): Nombre del modelo
    """
    invalidate_cache_patterns(f"*:{model_name}:*")

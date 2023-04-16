from flask_caching import Cache

from .config import ProductionConfig

cache = Cache(config={
    "CACHE_TYPE": ProductionConfig.CACHE_TYPE, 
    "CACHE_REDIS_HOST": ProductionConfig.CACHE_REDIS_HOST,
    "CACHE_REDIS_PORT": ProductionConfig.CACHE_REDIS_PORT,
    "CACHE_REDIS_DB": ProductionConfig.CACHE_REDIS_DB,
    "CACHE_REDIS_URL": ProductionConfig.CACHE_REDIS_URL,
    "CACHE_DEFAULT_TIMEOUT": ProductionConfig.CACHE_DEFAULT_TIMEOUT
})
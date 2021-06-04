# coding=utf-8
def key_hash(value):
    """hash缓存key，防止过长"""
    import hashlib
    return '%s' % hashlib.md5(value).hexdigest()


def cache2():
    """
    :param num1: 获取或者设置cache的标识
    :param num2：获取或者设置cache的标识
    :return: 缓存dict
    """
    from django.core.cache import cache
    import logging
    log = logging.getLogger(__name__)  # 日志
    # 去重并排序，增加缓存命中率
    # cache_key = 'num1={num1}&num2={num2}'.format(num1=num1, num2=num2)
    cache_key = 'testKey'

    # in cache, return cache
    # if cache.get(cache_key):
    #     log.debug('cache %s hitting ' % cache_key)
    #     return cache.get(cache_key)

    # not in cache, get result and set cache
    # ret = None
    # TODO do something get result
    ret = 'something'
    cache.set(cache_key, ret, 60 * 60 * 24)  # 一天过期
    return ret
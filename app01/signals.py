from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import User
import redis


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    # 获取Redis连接
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    # 删除用户在Redis中的数据
    # 假设你使用键名 'user:<user_id>' 来存储用户数据
    redis_key = f'user:{user.id}'
    redis_client.delete(redis_key)




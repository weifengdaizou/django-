import redis

poor = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=poor)

# r.setnx('age', 22)
#
# r.incrby('age')
#
# print(r.get('age'))

# r.hset('author', 'name', 'zs', {
#     'age': 23,
#     'sex': 'male'
# })

# print(r.hmget('author', ['age', 'name', 'sex']))




from django_redis import get_redis_connection

ONLINE_USERS_KEY = "online_users"
LAST_SEEN_PREFIX = "last_seen:"
TIMEOUT = 300  # 5 minutes


def track_user_activity(request):
    if request.user.is_authenticated:
        redis = get_redis_connection("default")
        user_id = request.user.id

        # Add to set
        redis.sadd(ONLINE_USERS_KEY, user_id)

        # Set TTL key
        redis.set(f"{LAST_SEEN_PREFIX}{user_id}", 1, ex=TIMEOUT)



def get_online_users():
    redis = get_redis_connection("default")
    all_members = redis.smembers(ONLINE_USERS_KEY)

    online_ids = []

    for uid in all_members:
        user_id = int(uid.decode())

        # Check if still active
        if redis.exists(f"{LAST_SEEN_PREFIX}{user_id}"):
            online_ids.append(user_id)
        else:
            # Cleanup stale user
            redis.srem(ONLINE_USERS_KEY, user_id)

    return online_ids


class OnlineUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # This runs BEFORE the view
        track_user_activity(request)

        # Call the next middleware / view
        response = self.get_response(request)

        # Optional: run logic AFTER view
        return response
    
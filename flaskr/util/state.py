_state = {}


def set_state(**kwargs):
    global _state
    if 'access_token' in kwargs:
        _state['access_token'] = kwargs['access_token']
    if 'refresh_token' in kwargs:
        _state['refresh_token'] = kwargs['refresh_token']
    if 'user' in kwargs:
        _state['user'] = kwargs['user']


def clear_state():
    set_state(
        access_token=None,
        refresh_token=None,
        user=None
    )


def state(key):
    global _state
    return _state.get(key)

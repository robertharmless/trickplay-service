subscribers = dict()


def subscribe(event_type: str, fn):
    if not event_type in subscribers:
        subscribers[event_type] = []
    subscribers[event_type].append(fn)


def post_event(event_type: str, who: str, data):
    """
    Post Event requires and event_type: str and data.
    """
    if not event_type in subscribers:
        return
    for fn in subscribers[event_type]:
        fn(who, data)

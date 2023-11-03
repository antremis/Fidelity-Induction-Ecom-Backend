def loginRequired():
    def decorator(*args, **kwargs):
        # Get JWT
        print(args, kwargs)
    return decorator
import asyncio


def wait_response(f):
    def decorator(view):
        async def wrapper(message):
            message._response_handler = f
            if asyncio.iscoroutinefunction(view):
                return await view(message)
            return view(message)
        return wrapper
    return decorator

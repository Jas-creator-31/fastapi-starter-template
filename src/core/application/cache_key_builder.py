from src.core.context.user_context import (
    user_context,
)


def cache_key_builder(
    func, namespace: str = "", *args, **kwargs
):
    context = user_context.get()
    user_id = (
        context.user_id
        if (context or context.user_id)
        else "guest"
    )
    return f"{namespace}:{func.__module__}:{func.__name__}:{user_id}:{args}:{kwargs}"

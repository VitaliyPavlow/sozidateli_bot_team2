import asyncio
from functools import wraps
from typing import Callable, Coroutine, Any, Union

from starlette.concurrency import run_in_threadpool

_F = Callable[[], None]
_P = Callable[[], Coroutine[Any, Any, None],]
_T = Callable[[Union[_F, _P]], _P]


def repeat_every(seconds: float) -> _F:
    def decorator(func: _F | _P) -> _P:
        is_coroutine = asyncio.iscoroutinefunction(func)

        @wraps(func)
        async def wrapped() -> None:
            async def loop() -> None:
                while True:
                    try:
                        if is_coroutine:
                            await func()
                        else:
                            await run_in_threadpool(func)
                    except Exception:
                        # Точную ошибку не отловить.
                        pass
                    await asyncio.sleep(seconds)

            asyncio.ensure_future(loop())

        return wrapped

    return decorator

import contextvars
from types import TracebackType

from django.http import HttpRequest
from .globals import _cv_request

class RequestContext:
    def __init__(self,request: HttpRequest):
        self.request = request
        self.session = request.session
        self._cv_tokens: list[tuple[contextvars.Token]] = []

    def push(self):
        #print("push self")
        self._cv_tokens.append((_cv_request.set(self),))
        pass

    def pop(self):
        clear_request = len(self._cv_tokens) == 1
        ctx = _cv_request.get()
        token, = self._cv_tokens.pop()
        _cv_request.reset(token)

        if ctx is not self:
            raise AssertionError(
                f"Popped wrong request context. ({ctx!r} instead of {self!r})"
            )
        #print("pop self")
        pass

    def __enter__(self) :
        self.push()
        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        tb,
    ) -> None:
        self.pop()

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__} {self.request.get_raw_uri()!r}"
            f" [{self.request.method}] of {self.request.method}>"
        )




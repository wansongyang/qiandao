from contextvars import ContextVar

from django.contrib.sessions.backends.base import SessionBase
from werkzeug.local import LocalProxy

from django.http import HttpRequest

_no_req_msg = """\
Working outside of request context.

This typically means that you attempted to use functionality that needed
an active HTTP request. Consult the documentation on testing for
information about how to avoid this problem.\
"""


_cv_request:ContextVar = ContextVar("django.request_ctx")

request_ctx = LocalProxy(  # type: ignore[assignment]
    _cv_request, unbound_message=_no_req_msg
)
# request 的代理对象，为当前生命周期的对象
request: HttpRequest = LocalProxy(
    _cv_request,"request",unbound_message=_no_req_msg
)

# session 的代理对象，为当前生命周期的对象
session: SessionBase = LocalProxy(
    _cv_request,"session",unbound_message=_no_req_msg
)

import functools
from urllib.parse import urlsplit, urlencode

from tornado.web import RequestHandler, HTTPError


def login_required(f):
    @functools.wraps(f)
    def wrapper(self: RequestHandler, *args, **kwargs):
        current_user = self.current_user
        if not current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlsplit(url).scheme:
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return f(self, *args, **kwargs)
    return wrapper

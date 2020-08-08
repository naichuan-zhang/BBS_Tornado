from handlers.base_handlers import BaseHandler


class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('index.html')

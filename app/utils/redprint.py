# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/20


class Redprint:
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f
        return decorator

    def register(self, bp, url_prefix=None):
        if url_prefix is None:
            url_prefix = '/' + self.name
        for f, rule, options in self.mound:
            # 这里的endpoint是: red_name + endpoint   注意之后flask把此红图注册到蓝图之上时会自动加上蓝图名
            endpoint = self.name + "+" + options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
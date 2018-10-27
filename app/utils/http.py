# encoding: utf-8
# __author__ = "wyb"
# date: 2018/10/27
# 向API发出请求
import requests


class http:
    @staticmethod
    def get(url, return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
             return {} if return_json else ''
        return r.json() if return_json else r.text
        # if r.status_code == 200:
        #     if return_json:
        #         return r.json()
        #     else:
        #         return r.text
        # else:
        #     if return_json:
        #         return {}
        #     else:
        #         return ""


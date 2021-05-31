#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    # uwsgi --http :8000 --wsgi-file test.py
    return [b'Hello World']

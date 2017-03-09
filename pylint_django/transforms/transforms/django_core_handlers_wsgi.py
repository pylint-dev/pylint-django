from django.core.handlers.wsgi import WSGIRequest as WSGIRequestOriginal


class WSGIRequest(WSGIRequestOriginal):
    status_code = None
    content = ''
    json = None

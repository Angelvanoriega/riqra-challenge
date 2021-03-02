from gevent.pywsgi import WSGIServer
from src.app import app

if __name__ == '__main__':
    print('Serving on 5000 port...')
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()

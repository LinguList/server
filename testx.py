def app(environ, start_response):
    start_response('200 OK', [('content-type', 'text/html')])
    return ['Hello world!']
if __name__ == '__main__':
    from http.server import HTTPServer
    HTTPServer.serve(app, host='127.0.0.1', port='8080')

from http.server import HTTPServer


class HttpServer(HTTPServer):
    is_ssl = False

    def __init__(self, server_address, handler_class, api_client, logger):
        self.api_client = api_client
        self.logger = logger
        super().__init__(server_address, handler_class)


class HttpsServer(HttpServer):
    is_ssl = True


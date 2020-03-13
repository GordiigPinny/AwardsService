import requests


class BaseApiRequestError(Exception):
    """
    Базовый класс для остальных эксепшнов
    """


class RequestError(BaseApiRequestError):
    def __init__(self, message: str = 'Request error'):
        self.message = message


class UnexpectedResponse(BaseApiRequestError):
    def __init__(self, response: requests.Response, message: str = 'Неожиданный ответ с сервера'):
        self.message = message
        self.response = response
        self.code = response.status_code
        try:
            self.body = response.json()
        except ValueError:
            self.body = response.text


class JsonDecodeError(BaseApiRequestError):
    def __init__(self, body_text: str, message: str = 'Couldn\'t decode response\'s body as json'):
        self.body_text = body_text
        self.message = message

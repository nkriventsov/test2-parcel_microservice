from fastapi import HTTPException


class BaseBaseException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BaseBaseException):
    detail = "Объект не найден"


class ObjectAlreadyExistsException(BaseBaseException):
    detail = "Похожий объект уже существует"


class IncorrectTokenException(BaseBaseException):
    detail = "Некорректный токен"


class DatabaseConnectionException(BaseBaseException):
    detail = "Ошибка подключения к базе данных"


class BaseHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ObjectNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Объект не найден"


class PackageNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Посылка не найдена"


class PackageTypeNotFoundHTTPException(BaseHTTPException):
    status_code = 404
    detail = "Тип посылок не найден"


class IncorrectTokenHTTPException(BaseHTTPException):
    detail = "Некорректный токен"


class NoAccessTokenHTTPException(BaseHTTPException):
    status_code = 401
    detail = "Вы не предоставили токен доступа"


class ObjectAlreadyExistsHTTPException(BaseHTTPException):
    status_code = 409
    detail = "Элемент уже существует"


class PackageRegistrationFailedHTTPException(BaseHTTPException):
    status_code = 500
    detail = "Ошибка при регистрации посылки"


class FetchingUSDRateHTTPException(BaseHTTPException):
    status_code = 500
    detail = "Ошибка обновления курса валют"


class DatabaseConnectionHTTPException(BaseHTTPException):
    status_code = 500
    detail = "База данных временно недоступна"

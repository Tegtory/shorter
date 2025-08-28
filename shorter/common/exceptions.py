class AppError(Exception):
    message = ""


class InvalidURLError(AppError):
    message = "Введите правильный url, https://...."


class BlackListError(AppError):
    message = "Данный url находиться в черном списке, попробуйте другой"

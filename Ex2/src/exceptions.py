class NabronirovalException(Exception):
    detail = 'Неожиданная ошибка'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = 'Объект не найден'


class AllRoomsAreBooked(NabronirovalException):
    detail = 'Не осталось свободных мест'


class UserAlredyRegistered(NabronirovalException):
    detail = 'Пользователь уже зарегестрирован'

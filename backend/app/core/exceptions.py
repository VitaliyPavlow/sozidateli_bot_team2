class ObjectIsNoneException(Exception):
    def __str__(self):
        return ("Отсутствуют данные по данному id. "
                "Проверьте правильность передачи данных в запросе.")


class UserAlreadyExists(Exception):
    def __str__(self):
        return """Пользователь уже существует!"""


class InvalidDate(Exception):
    def __str__(self):
        return "Дата собрания не может быть меньше текущей."


class MeetingClosed(Exception):
    def __str__(self):
        return "Закрытое собрание нельзя редактировать/удалять."

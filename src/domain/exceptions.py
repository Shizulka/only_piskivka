

class DomainError(Exception):
    """Базовий клас для всіх доменних помилок."""
    pass

class InvalidTimeRangeError(DomainError):
    def __init__(self):
        super().__init__("Час відкриття має бути раніше часу закриття.")

class InvalidEmailError(DomainError):
    def __init__(self):
        super().__init__("Некоректний формат email.")

class EmptyReviewError(DomainError):
    def __init__(self):
        super().__init__("Відгук не може бути порожнім.")

class UserAlreadyExistsError(DomainError):
    def __init__(self):
        super().__init__("Користувач з таким email або телефоном вже існує.")
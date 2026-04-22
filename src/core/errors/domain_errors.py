class DomainError(Exception):
    pass


class AuthenticationError(DomainError):
    pass

class ExpiredJwtSignatureError(DomainError):
    pass

class InvalidJwtSignatureError(DomainError):
    pass
 
class InvalidJwtTokenError(DomainError):
    pass

class NotHasPermissionError(DomainError):
    pass

class InternalServerError(DomainError):
    pass
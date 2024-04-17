from fastapi import HTTPException, status


class HTTPException_custom(HTTPException):
    status_code = 400
    detail = "Something went wrong"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExists(HTTPException_custom):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class UserNotFound(HTTPException_custom):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


class InvalidCredentials(HTTPException_custom):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid credentials"


class InvalidToken(HTTPException_custom):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid token"


class TokenExpired(HTTPException_custom):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


class TokenNotFound(HTTPException_custom):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Token not found"


class InvalidPassword(HTTPException_custom):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid password"


class InvalidEmail(HTTPException_custom):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid email"


class BookingNotFound(HTTPException_custom):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Booking not found"


class HotelNotFound(HTTPException_custom):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Booking not found"


class BookingNotAvailable(HTTPException_custom):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Booking not available"




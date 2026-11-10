from ninja import Schema


class MessageSchema(Schema):
    message: str

class UOMErrorMessageSchema(Exception):
    def __init__(self, status: str, code: int, message: str, details: str):
        self.status = status
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)

    def send(self):
        return {
            "status": self.status,
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }



class UOMMessageSchema(Schema):
    status: str
    code: str
    message: str
    details: str
    data : dict | list[dict]

    def __init__(self,status,message,details,data):
        self.data = status
        self.message = message
        self.details = details
        self.status = status
        self.data = data

    def send(self) :
        return {
            "status": self.status,
            "message": self.message,
            "details": self.details,
            "data": self.data
        }
from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(self, content=None, message='', **kwargs):
        custom_content = {
            'content': content,
            'message': message,
        }
        super(CustomResponse, self).__init__(
            data=custom_content,
            **kwargs
        )


class SuccessResponse(CustomResponse):
    def __init__(self, data=None, status=200, message='', **kwargs):
        super(SuccessResponse, self).__init__(
            content=data,
            status=status,
            message=message,
            **kwargs
        )


class ErrorResponse(CustomResponse):
    def __init__(self, error=None, status=400, message='Something went wrong', **kwargs):
        super(ErrorResponse, self).__init__(
            content=error,
            status=status,
            message=message,
            **kwargs
        )

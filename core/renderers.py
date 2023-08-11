from rest_framework import renderers


def get_meta(status='error', code=400, message='Something went wrong'):
    return {
        'status': status,
        'code': code,
        'message': message,
    }


class CustomJSONRenderer(renderers.JSONRenderer):
    def render(self, data=None, accepted_media_type=None, renderer_context=None):
        response = None
        status_code = renderer_context['response'].status_code
        exception = renderer_context['response'].exception

        try:
            content = data['content'] if data is not None else ''
            is_success = status_code // 100 == 2  # if status code is in 2** series
            message = data['message'] if data is not None else ''

            if is_success:
                # Success Response
                response = {
                    'data': content,
                    'meta': get_meta(status='success', code=status_code, message=message)
                }
            else:
                # Error Response
                response = {
                    'error': content or str(exception),
                    'meta': get_meta(code=status_code, message=message)
                }
        except KeyError:
            response = {
                'error': data,
                'meta': get_meta(code=status_code)
            }

        return super().render(response, accepted_media_type, renderer_context)

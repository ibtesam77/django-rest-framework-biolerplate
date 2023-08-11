from rest_framework import renderers


class CustomJSONRenderer(renderers.JSONRenderer):
    def render(self, data=None, accepted_media_type=None, renderer_context=None):
        response = None

        try:
            content = data['content'] if data is not None else ''
            status_code = renderer_context['response'].status_code
            exception = renderer_context['response'].exception
            is_success = status_code // 100 == 2  # if status code is in 2** series
            message = data['message'] if data is not None else ''

            if is_success:
                # Success Response
                response = {
                    'data': content,
                    'meta': {
                        'status': 'success',
                        'code': status_code,
                        'message': message,
                    }
                }
            else:
                # Error Response
                response = {
                    'error': content or str(exception),
                    'meta': {
                        'status': 'error',
                        'code': status_code,
                        'message': message,
                    }
                }
        except KeyError as e:
            response = {
                'error': str(e),
                'meta': {
                    'status': 'error',
                    'code': 500,
                    'message': 'Something went wrong',
                }
            }

        return super().render(response, accepted_media_type, renderer_context)

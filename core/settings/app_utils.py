from .environment import env

APP_UTILS = {
    'APP_NAME': env('APP_NAME', default='Test App'),
    'APP_LOGO': env('APP_LOGO', default='http://test.png'),
    'APP_URL': env('APP_URL', default='http://test.com'),
}

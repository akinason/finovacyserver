import environment

if environment.env() == environment.DEVELOPMENT:
    from .development import *
elif environment.env() == environment.PRODUCTION:
    from .production import *

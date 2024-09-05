import os

# For a production app, you should use a secret key set in the environment
# The recommended way to generate a 64char secret key is to run:
# python -c 'import secrets; print(secrets.token_hex())'
SECRET_KEY = os.getenv('SECRET_KEY', 'not-set')

# When deploying, set in the environment to the PostgreSQL URL
#connection_string = "postgresql://postgres:JojoPG99@localhost:5432/analysis"
#connection_string = "postgresql://jodi:lGtZlAMYChZLjKHNrSCS92ujMnbjO6pM@dpg-crcskc3qf0us73as8o7g-a.oregon-postgres.render.com/test_h0tm"
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

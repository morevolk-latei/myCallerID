# git clone https://morevolk@bitbucket.org/zzzeek/sqlalchemy.git
# Statement for enabling the development environment
DEBUG = True
ENV = "dev"

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
SQLALCHEMY_DATABASE_URI = 'mysql://dev_user:dev@User123@localhost/myCallerDB'
DATABASE_CONNECT_OPTIONS = {}
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one
# and performing background operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "very_secret_key@instahyre"

# Secret key for signing cookies
SECRET_KEY = JWT_SECRET_KEY = "very_secret_key@me"
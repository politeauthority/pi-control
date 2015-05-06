import os

# Statement for enabling the development environment
DEBUG = False

# Define the application directory
BASE_DIR           = os.path.abspath(os.path.dirname(__file__))  
UPLOAD_DIR         = BASE_DIR + '/uploads/'
CACHE_DIR          = BASE_DIR + '/cache/'
ALLOWED_EXTENSIONS = set( ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'] )
LOG_DIR            = BASE_DIR + '/logs/'
WEB_IP             = '0.0.0.0'
WEB_PORT           = 8081

# Define the database - we are working with
DB_USER = 'dev_app'
DB_PASS = 'cleancutt22'
DB_HOST = 'dbpostgres.local'
DB_PORT = '5432'
DB_NAME = 'carpi_dev'

SQLALCHEMY_DATABASE_URI = 'postgres://%s:%s@%s:%s/%s' % ( DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"



# INSTALL OPTIONS

# DEFAULT ADMIN LOGIN
ADMIN_EMAIL    = 'admin@politeauthority.com'
ADMIN_PASSWORD = 'cleancut'

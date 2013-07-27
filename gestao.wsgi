import sys
import logging

logging.basicConfig(stream=sys.stderr)

sys.path.insert(0, '/home/diego/gestao')
from gestao import app as application
application.secret_key = 'qwe123*'

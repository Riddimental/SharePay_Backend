import os
import sys

project_home = '/home/riddimental/Backend/SharePay_Backend'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

os.environ['DJANGO_SETTINGS_MODULE'] = 'backend_SharePay.settings'


from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


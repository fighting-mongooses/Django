import os
import sys


path = '/srv/webspace/wheybags/Django/Androkon/androkon'
if path not in sys.path:
	sys.path.append(path)


#raise Exception(str(sys.path))
os.environ['DJANGO_SETTINGS_MODULE'] = 'androkon.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

import os
import sys


sys.path.append('/home/WearWellWardrobe/WearWellWardrobe')
sys.path.append('/home/WearWellWardrobe/WearWellWardrobe/projectSite')


activate_this = '/home/WearWellWardrobe/.virtualenvs/WearWellWardrobe/bin/activate_this.py'
exec(open(activate_this).read(), dict(__file__=activate_this))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projectSite.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
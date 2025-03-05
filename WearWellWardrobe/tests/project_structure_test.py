import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class ProjectStructureTests(TestCase):

    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.WWW_app_dir = os.path.join(self.project_base_dir, 'WearWellWardrobe')

    def test_project_created(self):
        directory_exists = os.path.isdir(os.path.join(self.project_base_dir, 'projectSite'))
        urls_module_exists = os.path.isfile(os.path.join(self.project_base_dir, 'projectSite', 'urls.py'))

        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your projectSite configuration directory doesn't seem to exist. Did you use the correct name?{FAILURE_FOOTER}")
        self.assertTrue(urls_module_exists, f"{FAILURE_HEADER}Your project's urls.py module does not exist. Did you use the startproject command?{FAILURE_FOOTER}")

    def test_WWW_app_created(self):
        directory_exists = os.path.isdir(self.WWW_app_dir)
        is_python_package = os.path.isfile(os.path.join(self.WWW_app_dir, '__init__.py'))
        views_module_exists = os.path.isfile(os.path.join(self.WWW_app_dir, 'views.py'))

        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The WearWellWardrobe app directory does not exist. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(is_python_package, f"{FAILURE_HEADER}The WearWellWardrobe directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")
        self.assertTrue(views_module_exists, f"{FAILURE_HEADER}The WearWellWardrobe directory is missing files. Did you use the startapp command?{FAILURE_FOOTER}")

    def test_WWW_has_urls_module(self):
        module_exists = os.path.isfile(os.path.join(self.WWW_app_dir, 'urls.py'))

        self.assertTrue(module_exists, f"{FAILURE_HEADER}The WearWellWardrobe app's urls.py module is missing. Read over the instructions carefully, and try again. You need TWO urls.py modules.{FAILURE_FOOTER}")

    def test_is_WWW_app_configured(self):
        is_app_configured = 'WearWellWardrobe' in settings.INSTALLED_APPS

        self.assertTrue(is_app_configured, f"{FAILURE_HEADER}The WearWellWardrobe app is missing from your setting's INSTALLED_APPS list.{FAILURE_FOOTER}")
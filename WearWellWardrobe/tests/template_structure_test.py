import os
import re
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class TemplateStructureTests(TestCase):

    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.WearWellWardrobe_templates_dir = os.path.join(self.templates_dir, 'WearWellWardrobe')

    def test_templates_directory_exists(self):
        directory_exists = os.path.isdir(self.templates_dir)
        
        self.assertTrue(directory_exists, f"{FAILURE_HEADER}Your project's templates directory does not exist.{FAILURE_FOOTER}")
    """
    def test_WearWellWardrobe_templates_directory_exists(self):
        directory_exists = os.path.isdir(self.WearWellWardrobe_templates_dir)

        self.assertTrue(directory_exists, f"{FAILURE_HEADER}The WearWellWardrobe templates directory does not exist.{FAILURE_FOOTER}")
    """
    def test_template_dir_setting(self):
        variable_exists = 'TEMPLATE_DIR' in dir(settings)
        template_dir_value = os.path.normpath(settings.TEMPLATE_DIR)
        template_dir_computed = os.path.normpath(self.templates_dir)
        
        self.assertTrue(variable_exists, f"{FAILURE_HEADER}Your settings.py module does not have the variable TEMPLATE_DIR defined.{FAILURE_FOOTER}")
        self.assertEqual(template_dir_value, template_dir_computed, f"{FAILURE_HEADER}Your TEMPLATE_DIR setting does not point to the expected path. Check your configuration and try again.{FAILURE_FOOTER}")

    def test_template_lookup_path(self):
        lookup_list = settings.TEMPLATES[0]['DIRS']
        found_path = False

        for entry in lookup_list:
            entry_normalised = os.path.normpath(entry)

            if entry_normalised == os.path.normpath(settings.TEMPLATE_DIR):
                found_path = True

        self.assertTrue(found_path, f"{FAILURE_HEADER}Your project's templates directory is not listed in the TEMPLATES>DIRS lookup list. Check your settings.py module.{FAILURE_FOOTER}")

    def test_templates_exist(self):
        home_path = os.path.join(self.templates_dir, 'home.html')
        loggedInHome_path = os.path.join(self.templates_dir, 'loggedInHome.html')
        base_path = os.path.join(self.templates_dir, 'base.html')
        addPage_path = os.path.join(self.templates_dir, 'addPage.html')
        delete_path = os.path.join(self.templates_dir, 'delete.html')

        self.assertTrue(os.path.isfile(home_path), f"{FAILURE_HEADER}Your home.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(loggedInHome_path), f"{FAILURE_HEADER}Your loggedInHome.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(base_path), f"{FAILURE_HEADER}Your base.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(addPage_path), f"{FAILURE_HEADER}Your addPage.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")
        self.assertTrue(os.path.isfile(delete_path), f"{FAILURE_HEADER}Your delete.html template does not exist, or is in the wrong location.{FAILURE_FOOTER}")


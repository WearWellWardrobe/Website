import os
import importlib
from django.urls import reverse
from django.test import TestCase
from django.conf import settings

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class HomePageViewTests(TestCase):
    def setUp(self):
        self.views_module = importlib.import_module('WearWellWardrobe.views')
        self.views_module_listing = dir(self.views_module)
        self.project_urls_module = importlib.import_module('projectSite.urls')

    def test_view_exists(self):
        """
        Test that the home view exists and is accessible.
        """
        name_exists = 'home' in self.views_module_listing
        is_callable = callable(self.views_module.home)

        self.assertTrue(name_exists, f"{FAILURE_HEADER}The home() view for WearWellWardrobe does not exist.{FAILURE_FOOTER}")
        self.assertTrue(is_callable, f"{FAILURE_HEADER}Check that you have created the home() view correctly. It doesn't seem to be a function!{FAILURE_FOOTER}")
    
    def test_mappings_exists(self):
        home_mapping_exists = False
        
        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'home':
                    home_mapping_exists = True
        
        self.assertTrue(home_mapping_exists, f"{FAILURE_HEADER}The home URL mapping could not be found. Check your PROJECT'S urls.py module.{FAILURE_FOOTER}")
        self.assertEquals(reverse('WearWellWardrobe:home'), '/WearWellWardrobe/', f"{FAILURE_HEADER}The index URL lookup failed. Check WearWellWardrobes's urls.py module. You're missing something in there.{FAILURE_FOOTER}")
    
    def test_response(self):
        """
        Test if the response from the server contains the required string.
        """
        response = self.client.get(reverse('WearWellWardrobe:home'))
        
        self.assertEqual(response.status_code, 200, f"{FAILURE_HEADER}Requesting the home page failed. Check your URLs and view.{FAILURE_FOOTER}")

    def test_home_view_template(self):
        """
        Test that the home view uses the correct template.
        """
        response = self.client.get(reverse('WearWellWardrobe:home'))
        self.assertTemplateUsed(response, 'loggedInHome.html', f"{FAILURE_HEADER}The home view did not use the correct template.{FAILURE_FOOTER}")

    
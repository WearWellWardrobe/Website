# WearWellWardrobe/tests/template_tests.py

import os
import re
from django.test import TestCase
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string

FAILURE_HEADER = "\n\n\n================\nTwD TEST FAILURE =(\n================\n"
FAILURE_FOOTER = "\n"

class TemplateTests(TestCase):

    def get_template(self, path_to_template):
        """
        Helper method: returns the content of a template file as a string.
        """
        with open(path_to_template, 'r', encoding='utf-8') as f:
            return f.read()
        
    def test_home_template_exists(self):
        """
        Check that the main home template (loggedInHome.html) exists in the correct place.
        """
        home_template_path = os.path.join(settings.BASE_DIR, 'templates', 'loggedInHome.html')
        self.assertTrue(os.path.exists(home_template_path), f"{FAILURE_HEADER}We couldn't find 'loggedInHome.html' in your templates/ directory. " f"Make sure you have the correct template name and path.{FAILURE_FOOTER}")

    def test_home_view_uses_loggedInHome_template(self):
        """
        Checks that the 'home' view uses 'loggedInHome.html'.
        """
        response = self.client.get(reverse('WearWellWardrobe:home'))
        self.assertTemplateUsed(response, 'loggedInHome.html', f"{FAILURE_HEADER}The home view did not use 'loggedInHome.html'. " f"Check your view's render() call or the URL mapping for 'WearWellWardrobe:home'.{FAILURE_FOOTER}")
    
    """
    def test_home_has_title(self):
        response = self.client.get(reverse('WearWellWardrobe:home'))
        content = response.content.decode('utf-8')

        title_pattern = r'<title>(\s*)Wear Well Wardrobe - Home(\s*)</title>'
        self.assertTrue(re.search(title_pattern, content), f"{FAILURE_HEADER}We couldn't find '<title>WearWellWardrobe Home</title>' in the home page. " f"Ensure there is a <title> tag in 'loggedInHome.html'.{FAILURE_FOOTER}")
    """

    def test_home_includes_add_page_link(self):
        """
        Checks if there's a link on the home page to add a new Page.
        """
        response = self.client.get(reverse('WearWellWardrobe:home'))
        content = response.content.decode('utf-8')

        add_page_url = reverse('WearWellWardrobe:addPage')
        expected_link = f'href="{add_page_url}"'

        self.assertIn(expected_link, content, f"{FAILURE_HEADER}Couldn't find a hyperlink to the addPage view on the home page. " f"Add <a href=\"{{% url 'WearWellWardrobe:addPage' %}}\">Add a Page</a> in 'loggedInHome.html'.{FAILURE_FOOTER}")

    def test_base_template_exists(self):
        """
        Check if there is a base.html that the templates extend.
        """
        base_template_path = os.path.join(settings.BASE_DIR, 'templates', 'base.html')
        self.assertTrue(os.path.exists(base_template_path), f"{FAILURE_HEADER}Couldn't find a 'base.html' template in 'templates/'. " f"Check if it is named differently or if a base template is used.{FAILURE_FOOTER}")

    def test_loggedInHome_inherits_base(self):
        """
        Check if 'loggedInHome.html' extends 'base.html'.
        """
        home_template_path = os.path.join(settings.BASE_DIR, 'templates', 'loggedInHome.html')
        template_str = self.get_template(home_template_path)

        extend_pattern = r'{% extends\s+["\']base.html["\']\s+%}'
        self.assertTrue(re.search(extend_pattern, template_str), f"{FAILURE_HEADER}It doesn't look like 'loggedInHome.html' extends 'base.html'. " f"Check the '{{% extends \"base.html\" %}}' tag in 'loggedInHome.html'.{FAILURE_FOOTER}")

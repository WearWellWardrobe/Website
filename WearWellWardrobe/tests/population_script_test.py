import os
from django.test import TestCase
from django.conf import settings
from WearWellWardrobe.models import Category, Page

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class PopulateScriptTests(TestCase):
    def setUp(self):
        try:
            import populate
        except ImportError:
            raise ImportError(
                f"{FAILURE_HEADER}Could not import 'populate'. "
                f"Ensure it's in the correct location and named properly.{FAILURE_FOOTER}"
            )

        if not hasattr(populate, 'populate'):
            raise NameError(
                f"{FAILURE_HEADER}No 'populate()' function found in 'populate'.{FAILURE_FOOTER}"
            )

        populate.populate()

    def test_categories_exist(self):
        expected_cats = ["Access", "Storage", "Maintain", "Landfill", "Disposal", "Adaptation"]
        categories_in_db = Category.objects.all()
        cat_names_in_db = [cat.name for cat in categories_in_db]

        for cat_name in expected_cats:
            self.assertIn(
                cat_name,
                cat_names_in_db,
                f"{FAILURE_HEADER}Expected category '{cat_name}' not found in the database after running populate().{FAILURE_FOOTER}"
            )
    
    def test_pages_exist(self):

        expected_pages = [
            ("Access", "Access"),
            ("Access", "Rent"),
            ("Maintain", "Repair"),
            ("Disposal", "Responsible Disposal"),
        ]

        for (cat_name, page_title) in expected_pages:
            try:
                cat = Category.objects.get(name=cat_name)
            except Category.DoesNotExist:
                self.fail(
                    f"{FAILURE_HEADER}Category '{cat_name}' not found in database; "
                    f"cannot check pages.{FAILURE_FOOTER}"
                )
            try:
                Page.objects.get(category=cat, title=page_title)
            except Page.DoesNotExist:
                self.fail(
                    f"{FAILURE_HEADER}Page '{page_title}' in category '{cat_name}' was not found. "
                    f"Check your populate script data.{FAILURE_FOOTER}"
                )

    def test_page_count(self):
        page_count = Page.objects.count()
        self.assertEqual(
            page_count,
            20,
            f"{FAILURE_HEADER}Expected 20 pages from populate script, found {page_count}.{FAILURE_FOOTER}"
        )
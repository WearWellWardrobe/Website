import os
import warnings
import importlib
from WearWellWardrobe.models import Category, Page, UserProfile
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}TwD TEST FAILURE =({os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

class ModelTests(TestCase):
    """
    We are going to check whether the category and page models are set up correctly.
    """
    def setUp(self):
        self.category, _ = Category.objects.get_or_create(name='TestCategory')
        image_content = b'\x47\x49\x46\x38\x39\x61'
        self.uploaded_file = SimpleUploadedFile("test.gif", image_content, content_type="image/gif")

        self.page = Page.objects.create(
            category=self.category,
            title="Test Page",
            content1="Content part 1",
            content2="Content part 2",
            content3="Content part 3",
            content4="Content part 4",
            displayStyle=1,
            pageNotes="Notes about this page",
            deletable=True,
            img1=self.uploaded_file,
            
        )

        self.user= User.objects.create_user(username='testuser', password='testpassword')
        self.user_profile = UserProfile.objects.create(user=self.user, website="https://example.com")

    def test_category_creation(self):
        self.assertIsNotNone(self.category.ID, "Category ID (primary key) should not be None.")
        self.assertEqual(self.category.name, "TestCategory", "Category name did not match.")
        self.assertEqual(str(self.category), "TestCategory", "__str__ for Category should return its name.")
        self.assertEqual(self.category._meta.verbose_name_plural, "Categories", "Category's Meta.verbose_name_plural should be 'Categories'.")

    def test_page_creation(self):
        self.assertIsNotNone(self.page.page_id, "Page page_id (primary key) should not be None.")
        self.assertEqual(self.page.category, self.category, "Page.category should link to the correct Category.")
        self.assertEqual(self.page.title, "Test Page", "Page title did not match.")
        self.assertEqual(self.page.content1, "Content part 1", "Page content1 did not match.")
        self.assertEqual(self.page.content2, "Content part 2", "Page content2 did not match.")
        self.assertEqual(self.page.content3, "Content part 3", "Page content3 did not match.")
        self.assertEqual(self.page.content4, "Content part 4", "Page content4 did not match.")
        self.assertEqual(self.page.displayStyle, 1, "displayStyle is incorrect.")
        self.assertEqual(self.page.pageNotes, "Notes about this page", "pageNotes did not match.")
        self.assertTrue(self.page.deletable, "deletable should be True by default (or as assigned).")

    def test_str_method(self):
        self.assertEqual(str(self.category), 'TestCategory', f"{FAILURE_HEADER}The __str__() method in the Category class has not been implemented correctly.{FAILURE_FOOTER}")
        self.assertEqual(str(self.page), 'Test Page', f"{FAILURE_HEADER}The __str__() method in the Page class has not been implemented correctly. It should return its title{FAILURE_FOOTER}")

    def test_slug_generation(self):
        # The first Page in setUp() should have a slug based on "My First Page".
        self.assertTrue(self.page.slug.startswith("test-page"),
                        "Slug was not generated from the title 'Test Page' as expected.")

        # Create another page with the same title to test unique slug logic.
        page2 = Page.objects.create(
            category=self.category,
            title="Test Page"
        )
        self.assertNotEqual(page2.slug, self.page.slug, "Slugs for duplicate titles should be unique.")
        self.assertTrue(page2.slug.startswith("test-page-"), "Unique slug not appended correctly for duplicates.")
    
    def test_img1_field(self):
        """
        Check that the image field can store the uploaded file. (Optional)
        """
        self.assertIsNotNone(self.page.img1, "img1 field should store the uploaded file.")
        self.assertIn("test", self.page.img1.name, "img1 file name should contain 'test'.")
        self.assertTrue(self.page.img1.name.endswith(".gif"), "img1 file name should end with '.gif'.")

    def test_userprofile_creation(self):
        self.assertEqual(str(self.user_profile), self.user.username, "UserProfile's __str__() should return the associated username.")

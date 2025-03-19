
from WearWellWardrobe.models import Category, Page, UserProfile
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User

class AdminInterfaceTests(TestCase):
    """
    Tests for admin site accessibility and registration of Category, Page, and UserProfile.
    """

    def setUp(self):
        """
        Create a superuser and log them in.
        """
        self.superuser = User.objects.create_superuser(
            username='testadmin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.client.login(username='testadmin', password='adminpass123')

        # Create some objects to verify they appear in admin lists.
        self.category = Category.objects.create(name='Test Category')
        self.page = Page.objects.create(
            category=self.category,
            title='Test Page',
        )
        self.user_profile = UserProfile.objects.create(user=self.superuser)

    def test_admin_accessible(self):
        """
        Check if /admin/ is accessible with status code 200.
        """
        response = self.client.get('/admin/')
        self.assertEqual(
            response.status_code, 
            200, 
            "Admin site is not accessible at /admin/. Check your main urls.py for 'admin/' pattern."
        )

    def test_models_listed_in_admin_index(self):
        """
        Ensure Category, Page, and UserProfile are present in the admin index page.
        """
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        html = response.content.decode('utf-8')

        self.assertIn(
            'WearWellWardrobe', 
            html, 
            "The WearWellWardrobe app label wasn't listed in the admin index."
        )
        self.assertIn(
            'Categories', 
            html, 
            "The Category model wasn't listed in the admin index (check admin.py or verbose_name_plural)."
        )
        self.assertIn(
            'Pages', 
            html, 
            "The Page model wasn't listed in the admin index (check admin.py or verbose_name_plural)."
        )
        self.assertIn(
            'User profiles',
            html, 
            "The UserProfile model wasn't listed in the admin index (check admin.py or verbose_name_plural)."
        )

    def test_category_changelist(self):
        """
        Check the Category changelist page loads.
        """
        response = self.client.get('/admin/wearwellwardrobe/category/')
        self.assertEqual(
            response.status_code, 
            200, 
            "Could not load the Category changelist in admin."
        )

        html = response.content.decode('utf-8')
        self.assertIn(
            'Test Category',
            html,
            "Expected 'Test Category' not found in Category changelist. Is the object displayed?"
        )

    def test_page_changelist(self):
        """
        Check the Page changelist page loads and shows the test page.
        """
        response = self.client.get('/admin/wearwellwardrobe/page/')
        self.assertEqual(
            response.status_code, 
            200, 
            "Could not load the Page changelist in admin."
        )

        html = response.content.decode('utf-8')
        self.assertIn(
            'Test Page',
            html,
            "Expected 'Test Page' not found in Page changelist."
        )

    def test_userprofile_changelist(self):
        """
        Check the UserProfile changelist page loads and shows the test user's profile.
        """
        response = self.client.get('/admin/wearwellwardrobe/userprofile/')
        self.assertEqual(
            response.status_code,
            200,
            "Could not load the UserProfile changelist in admin."
        )

        html = response.content.decode('utf-8')
        # By default, the UserProfile __str__() returns the username.
        # So you might see 'testadmin' in the row.
        self.assertIn(
            'testadmin',
            html,
            "Expected 'testadmin' not found in UserProfile changelist."
        )

    def test_category_prepopulated_fields(self):
        """
        This checks that the slug is prepopulated from the name in CategoryAdmin.
        Django can include a data attribute like data-prepopulated-fields
        in the add/change forms so we will just check for that substring.
        """

        response = self.client.get('/admin/wearwellwardrobe/category/add/')
        self.assertEqual(response.status_code, 200)

        html = response.content.decode('utf-8')
        self.assertIn(
            'data-prepopulated-fields=',
            html,
            "Prepopulated fields for Category slug not detected. Did you set prepopulated_fields in CategoryAdmin?"
        )
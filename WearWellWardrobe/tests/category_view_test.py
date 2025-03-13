from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from WearWellWardrobe.models import Category, Page, UserProfile

class DoneCategoryTests(TestCase):
    """
    Tests for doneCategory() (just a simple template render).
    """
    def setUp(self):
        self.client = Client()

    def test_done_category_view(self):
        response = self.client.get(reverse('WearWellWardrobe:doneCategory'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categroyDone.html')


class EditCategoryTests(TestCase):
    """
    Tests for editCategory().
    """
    def setUp(self):
        self.client = Client()
        self.cat = Category.objects.create(name='Editable Cat', ID=99)
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_edit_category_get(self):
        response = self.client.get(reverse('WearWellWardrobe:editCategory', args=[self.cat.ID]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categoryeditPage.html')
        self.assertIn('form', response.context)
        self.assertIn('category', response.context)

    def test_edit_category_post(self):
        post_data = {
            'name': 'Renamed Category',
        }
        response = self.client.post(
            reverse('WearWellWardrobe:editCategory', args=[self.cat.ID]),
            post_data
        )
        self.assertRedirects(response, reverse('WearWellWardrobe:doneCategory'))
        self.cat.refresh_from_db()
        self.assertEqual(self.cat.name, 'Renamed Category')
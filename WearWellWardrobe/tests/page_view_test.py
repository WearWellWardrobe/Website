from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from WearWellWardrobe.models import Category, Page, UserProfile

'''
class ViewPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat = Category.objects.create(name='Category for View')
        self.page = Page.objects.create(
            category=self.cat,
            title='Page for Viewing',
            slug='page-for-viewing'
        )

    def test_view_page_found(self):
        response = self.client.get(reverse('WearWellWardrobe:viewPage', args=[self.page.slug]))

        self.assertEqual(response.status_code, 200 or 302 or 404)  
 
    def test_view_page_not_found(self):
        response = self.client.get(reverse('WearWellWardrobe:viewPage', args=['no-such-page']))

        self.assertTrue(response.status_code in [302, 404])
'''

class EditPageTests(TestCase):
    """
    Tests for the editPage() function.
    """
    def setUp(self):
        self.client = Client()
        self.cat = Category.objects.create(name='Edit Cat')
        self.page = Page.objects.create(
            category=self.cat,
            title='Old Title',
            slug='old-title'
        )
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_edit_page_get(self):
        """
        Check the GET request loads the itemPage.html template with a form.
        """
        response = self.client.get(reverse('WearWellWardrobe:editPage', args=[self.page.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'itemPage.html')
        self.assertIn('form', response.context)
        self.assertIn('page', response.context)

    def test_edit_page_post(self):
        """
        Post updated data to edit the page, then check redirect and updated title.
        """
        post_data = {
            'title': 'New Title',
            'content1': 'New content',
            'content2': '',
            'content3': '',
            'content4': '',
            'pageNotes': 'Updated notes',
            'category': self.cat.pk,
            'displayStyle': 1,
        }
        response = self.client.post(
            reverse('WearWellWardrobe:editPage', args=[self.page.slug]),
            post_data
        )
        self.assertRedirects(response, reverse('WearWellWardrobe:home'))
        self.page.refresh_from_db()
        self.assertEqual(self.page.title, 'New Title')
        self.assertEqual(self.page.pageNotes, 'Updated notes')


class AddPageTests(TestCase):
    """
    Tests for the addPage() function.
    """
    def setUp(self):
        self.client = Client()
        self.cat = Category.objects.create(name='Add Cat')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_add_page_post(self):
        """
        Submit a valid form to create a new Page.
        """
        post_data = {
            'title': 'Newly Added Page',
            'content1': 'Hello World',
            'category': self.cat.pk,
            'displayStyle': 1,
        }
        response = self.client.post(reverse('WearWellWardrobe:addPage'), post_data)
        self.assertRedirects(response, reverse('WearWellWardrobe:home'))
        new_page = Page.objects.get(title='Newly Added Page')
        self.assertIsNotNone(new_page)

class DeletePageTests(TestCase):
    """
    Tests for deletePage().
    """
    def setUp(self):
        self.client = Client()
        self.cat = Category.objects.create(name='Delete Cat')
        self.page = Page.objects.create(
            category=self.cat,
            title='Page to Delete',
            slug='delete-me'
        )
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_delete_page_get(self):
        """
        GET should load the confirmation template.
        """
        response = self.client.get(reverse('WearWellWardrobe:deletePage', args=[self.page.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete.html')
        self.assertIn('page', response.context)

    def test_delete_page_post(self):
        """
        POST should delete the page and redirect home.
        """
        response = self.client.post(reverse('WearWellWardrobe:deletePage', args=[self.page.slug]))
        self.assertRedirects(response, reverse('WearWellWardrobe:home'))
        with self.assertRaises(Page.DoesNotExist):
            Page.objects.get(slug='delete-me')


from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from WearWellWardrobe.models import Category, Page, UserProfile

class PageGetTests(TestCase):
    """
    Tests for the PageGet API view.
    """
    def setUp(self):
        self.client = Client()
        self.cat = Category.objects.create(name='API Cat')
        self.page1 = Page.objects.create(category=self.cat, title='API Page 1')
        self.page2 = Page.objects.create(category=self.cat, title='API Page 2')

    def test_page_get_api(self):
        response = self.client.get(reverse('WearWellWardrobe_api:item-list'))  

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = response.json()
        self.assertEqual(len(data), 2)
        titles = [item['title'] for item in data]
        self.assertIn('API Page 1', titles)
        self.assertIn('API Page 2', titles)
'''
Probably Redundant Code
class RecordDetailTests(TestCase):
    """
    Tests for the RecordDetail API view (if you're using it for an 'Item' model).
    """
    def setUp(self):
        self.client = Client()
        self.cat = Category.objects.create(name='Detail Cat')
        self.page = Page.objects.create(category=self.cat, title='Detail Page', slug='detail-page')

    def test_record_detail_found(self):
        response = self.client.get(reverse('WearWellWardrobe:record-detail', args=[self.page.page_id]))
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['title'], 'Detail Page')

    def test_record_detail_not_found(self):
        response = self.client.get(reverse('WearWellWardrobe:record-detail', args=[9999]))
        self.assertEqual(response.status_code, 404)
'''

# WearWellWardrobe/tests/forms_test.py

import os
from django.test import TestCase
from django import forms as django_fields
from django.contrib.auth.models import User
from django.test import Client
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from WearWellWardrobe.models import Page, Category, UserProfile
from WearWellWardrobe.forms import (PageForm, EditCategoryForm, EditPageForm, UserForm, UserProfileForm,)

FAILURE_HEADER = "\n\n\n================\nTwD TEST FAILURE =(\n================\n"
FAILURE_FOOTER = "\n"

class FormsClassTest(TestCase):
    """
    Tests for the forms in WearWellWardrobe.forms
    """

    def test_forms_py_exists(self):
        """
        Ensure forms.py is present in the WearWellWardrobe app.
        """
        project_path = os.getcwd()
        app_path = os.path.join(project_path, 'WearWellWardrobe')
        forms_module_path = os.path.join(app_path, 'forms.py')

        self.assertTrue(
            os.path.exists(forms_module_path),
            f"{FAILURE_HEADER}Could not find 'forms.py' in WearWellWardrobe. "
            f"Please ensure it exists and is in the correct location.{FAILURE_FOOTER}"
        )

    def test_page_form(self):
        """
        Check if PageForm references the Page model and has the expected fields
        """
        form = PageForm()
        self.assertEqual(
            type(form.instance), 
            Page, 
            f"{FAILURE_HEADER}PageForm does not link to the Page model. "f"Check the Meta class in PageForm.{FAILURE_FOOTER}")
        
        expected_fields = {
            'title': django_fields.CharField,
            'content1': django_fields.CharField,
            'content2': django_fields.CharField,
            'content3': django_fields.CharField,
            'content4': django_fields.CharField,
            'img1': django_fields.ImageField,
            'pageNotes': django_fields.CharField,
            'deletable': django_fields.BooleanField,
            'category': django_fields.ModelChoiceField,
            'displayStyle': django_fields.IntegerField,
        }

        actual_fields = form.fields
        for field_name, field_type in expected_fields.items():
            self.assertIn(
                field_name,
                actual_fields,
                f"{FAILURE_HEADER}The field '{field_name}' is missing from PageForm.{FAILURE_FOOTER}"
            )
            self.assertIsInstance(
                actual_fields[field_name],
                field_type,
                f"{FAILURE_HEADER}The field '{field_name}' in PageForm is not of type {field_type}.{FAILURE_FOOTER}"
            )

    def test_edit_category_form(self):
        """
        Check that EditCategoryForm references Category and has the expected fields.
        """
        form = EditCategoryForm()
        self.assertEqual(
            type(form.instance),
            Category,
            f"{FAILURE_HEADER}EditCategoryForm does not link to the Category model. "
            f"Check the Meta class in EditCategoryForm.{FAILURE_FOOTER}"
        )

        expected_fields = {
            'name': django_fields.CharField,
        }

        actual_fields = form.fields
        for field_name, field_type in expected_fields.items():
            self.assertIn(
                field_name,
                actual_fields,
                f"{FAILURE_HEADER}The field '{field_name}' is missing from EditCategoryForm.{FAILURE_FOOTER}"
            )
            self.assertIsInstance(
                actual_fields[field_name],
                field_type,
                f"{FAILURE_HEADER}The field '{field_name}' in EditCategoryForm is not of type {field_type}.{FAILURE_FOOTER}"
            )

    def test_edit_page_form(self):
        """
        Check that EditPageForm references Page and has the expected fields.
        """
        form = EditPageForm()
        self.assertEqual(
            type(form.instance),
            Page,
            f"{FAILURE_HEADER}EditPageForm does not link to the Page model. "f"Check your Meta class in EditPageForm.{FAILURE_FOOTER}"
        )

        expected_fields = {
            'title': django_fields.CharField,
            'displayStyle': django_fields.IntegerField,
            'content1': django_fields.CharField,
            'content2': django_fields.CharField,
            'content3': django_fields.CharField,
            'content4': django_fields.CharField,
            'img1': django_fields.ImageField,
            'pageNotes': django_fields.CharField,
            'category': django_fields.ModelChoiceField,
        }

        actual_fields = form.fields
        for field_name, field_type in expected_fields.items():
            self.assertIn(
                field_name,
                actual_fields,
                f"{FAILURE_HEADER}The field '{field_name}' is missing from EditPageForm.{FAILURE_FOOTER}"
            )
            self.assertIsInstance(
                actual_fields[field_name],
                field_type,
                f"{FAILURE_HEADER}The field '{field_name}' in EditPageForm is not of type {field_type}.{FAILURE_FOOTER}"
            )

    def test_user_form(self):
        """
        Check that UserForm references Django's User, or has the fields we expect (username, email, password).
        """
        form = UserForm()
        self.assertEqual(
            type(form.instance),
            User,
            f"{FAILURE_HEADER}UserForm does not link to the User model. "f"Check the Meta class in UserForm.{FAILURE_FOOTER}"
        )

        expected_fields = {
            'username': django_fields.CharField,
            'email': django_fields.EmailField,
            'password': django_fields.CharField,
        }

        actual_fields = form.fields
        for field_name, field_type in expected_fields.items():
            self.assertIn(
                field_name,
                actual_fields,
                f"{FAILURE_HEADER}The field '{field_name}' is missing from UserForm.{FAILURE_FOOTER}"
            )
            self.assertIsInstance(
                actual_fields[field_name],
                field_type,
                f"{FAILURE_HEADER}The field '{field_name}' in UserForm is not of type {field_type}.{FAILURE_FOOTER}"
            )

    def test_user_profile_form(self):
        """
        Check that UserProfileForm references UserProfile and has expected fields.
        """
        form = UserProfileForm()
        self.assertEqual(
            type(form.instance),
            UserProfile,
            f"{FAILURE_HEADER}UserProfileForm does not link to the UserProfile model. "f"Check your Meta class in UserProfileForm.{FAILURE_FOOTER}"
        )

        self.assertEqual(
            len(form.fields), 0, f"{FAILURE_HEADER}UserProfileForm was expected to have no fields, but found some. "f"Update the code or this test accordingly.{FAILURE_FOOTER}"
        )

class AddPageAncillaryTests(TestCase):
    """
    Checks the 'addPage' view, URL, template, and form functionality.
    """

    def setUp(self):
        """
        Creates a Category object so we have something to associate pages with, and a client to make test requests.
        """
        self.client = Client()
        self.category = Category.objects.create(name="Test Category")

    def test_add_page_url_mapping(self):
        """
        `WearWellWardrobe/urls.py` has `path('addPage/', views.addPage, name='addPage')`. This test is to see if reversing 'WearWellWardrobe:addPage' has the expected path '/WearWellWardrobe/addPage/'.
        """
        url = reverse('WearWellWardrobe:addPage')

        self.assertEqual(url, '/WearWellWardrobe/addPage/', f"{FAILURE_HEADER}Reverse lookup for 'WearWellWardrobe:addPage' did not return '/WearWellWardrobe/addPage/'. "f"Check the urls.py to ensure the route matches this pattern.{FAILURE_FOOTER}")

    def test_home_link_to_add_page(self):
        """
        Checks whether the home page (loggedInHome.html) contains a link to addPage.
        """
        home_url = reverse('WearWellWardrobe:home')
        response = self.client.get(home_url)
        self.assertEqual(response.status_code, 200, "{FAILURE_HEADER}Could not load the home page via 'WearWellWardrobe:home'.{FAILURE_FOOTER}")

        content = response.content.decode('utf-8')
        add_page_url = reverse('WearWellWardrobe:addPage')
        self.assertIn(f'href="{add_page_url}"', content, f"{FAILURE_HEADER}No hyperlink to addPage found in the home page. "f"Please add a link (e.g. <a href=\"{add_page_url}\">Add a new Page</a>) in loggedInHome.html.{FAILURE_FOOTER}")

    def test_add_page_template(self):
        """
        Checks if 'addPage.html' is used by the addPage() view.
        """
        add_page_url = reverse('WearWellWardrobe:addPage')
        response = self.client.get(add_page_url)
        self.assertTemplateUsed(response, 'addPage.html', f"{FAILURE_HEADER}The addPage.html template is not used by the addPage() view. "f"Please ensure it is returning render(request, 'addPage.html', ...).{FAILURE_FOOTER}")

    def test_add_page_form_response(self):
        """
        Checks whether the addPage.html template includes a <form> and points to the correct action URL (WearWellWardrobe:addPage).
        """
        add_page_url = reverse('WearWellWardrobe:addPage')
        response = self.client.get(add_page_url)
        content = response.content.decode('utf-8')

        self.assertIn("<form", content, f"{FAILURE_HEADER}Could not find a <form> element in addPage.html. "f"There should be <form method='POST' ...> in the template.{FAILURE_FOOTER}")

        self.assertIn(f'action="{add_page_url}"', content, f"{FAILURE_HEADER}The <form> action does not match '{add_page_url}'. " f"Please set action=\"{{% url 'WearWellWardrobe:addPage' %}}\" in addPage.html.{FAILURE_FOOTER}")

    def test_add_page_functionality(self):
        """
        Submits the form with valid data. Expecting a new Page object to be created and a redirect to 'WearWellWardrobe:home'.
        """
        add_page_url = reverse('WearWellWardrobe:addPage')

        post_data = {
            'title': 'New Page Title',
            'content1': 'Some content',
            'displayStyle': 1,
            'category': self.category.pk,
        }
        
        response = self.client.post(add_page_url, post_data)

        self.assertRedirects(response, reverse('WearWellWardrobe:home'), msg_prefix=f"{FAILURE_HEADER}After posting valid data to addPage, expected a redirect to home. {FAILURE_FOOTER}")

        created_page = Page.objects.filter(title='New Page Title').first()
        self.assertIsNotNone(created_page, f"{FAILURE_HEADER}A new Page with title 'New Page Title' was not created. " f"Ensure the addPage view calls form.save() or page.save()!{FAILURE_FOOTER}")

        self.assertEqual(created_page.content1, 'Some content', f"{FAILURE_HEADER}The newly created Page doesn't have the expected 'content1' value. {FAILURE_FOOTER}")
        self.assertEqual(created_page.category, self.category, f"{FAILURE_HEADER}The newly created Page isn't linked to the correct Category. {FAILURE_FOOTER}")
        self.assertEqual(created_page.displayStyle, 1, f"{FAILURE_HEADER}displayStyle was not saved correctly on the newly created Page. {FAILURE_FOOTER}")
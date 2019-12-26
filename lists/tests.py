from django.test import TestCase

from lists.views import home_page


class HomePageTest(TestCase):
    """description"""
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

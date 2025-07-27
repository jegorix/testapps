from django.test import TestCase, SimpleTestCase
from django.urls import reverse

# Create your tests here.

# TESTS RESPONSE FROM URLS THAT THEY ARE EXISTS
class HomepageTests(SimpleTestCase):
    # TESTS RESPONSE FROM URLS THAT THEY ARE EXISTS
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        
    # TESTS ACCESS BY URLS NAME
    def test_url_available_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        
    # TESTS THAT SOME TEMPLATE USED
    def test_template_name_correct(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "blog/index.html")
        
    # TEST SEARCHES CONTENT IN RESPONSED TEMPLATE
    def test_template_content(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Index")
        
        
        

class AboutpageTests(SimpleTestCase):
    # TESTS RESPONSE FROM URLS THAT THEY ARE EXISTS
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/info/")
        self.assertEqual(response.status_code, 200)
       
    # TESTS ACCESS BY URLS NAME
    def test_url_available_by_name(self):
        response = self.client.get(reverse("info"))
        self.assertEqual(response.status_code, 200)
        
    # TESTS THAT SOME TEMPLATE USED  
    def test_template_name_correct(self):
        response = self.client.get(reverse("info"))
        self.assertTemplateUsed(response, "blog/info.html")
        
    # TEST SEARCHES CONTENT IN RESPONSED TEMPLATE
    def test_template_content(self):
        response = self.client.get(reverse("info"))
        self.assertContains(response, "О нас")
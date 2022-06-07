from django.test import SimpleTestCase
from manager_app.views import *
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views


class TestUrls(SimpleTestCase):

    def test_index_view_url_resolves(self):
        url = reverse('index-view')
        self.assertEqual(resolve(url).func.view_class, IndexView)

    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func.view_class, SignUpView)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)

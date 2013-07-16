import json

from django.test import TestCase
from django.conf import settings

class TestBarsNotLoggedIn(TestCase):

    fixtures = ['test_fixtures.json']

    def setUp(self):
        pass

    def test_mybar_no_auth(self):
        resp = self.client.get('/bars/mybar/')
        self.assertEqual(resp.status_code, 403)

    def test_login_bad_payload(self):
        resp = self.client.post(
            '/auth/login/bytoken/',
            data={},
        )
        self.assertEqual(resp.status_code, 401)

    def test_barlis(self):
        resp= self.client.get('/bars/bars/')
        self.assertEqual(resp.status_code, 200)

    def test_barlist_post(self):
        resp = self.client.post('/bars/bars/')
        self.assertEqual(resp.status_code, 405)

    def test_barprofile(self):
        resp = self.client.get('/bars/bar/1/')
        self.assertEqual(resp.status_code, 200)

    def test_barprofile_post(self):
        resp = self.client.post('/bars/bar/1/')
        self.assertEqual(resp.status_code, 405)

class TestBarsLoggedIn(TestCase):

    fixtures = ['test_fixtures.json']

    def setUp(self):
        resp = self.client.post(
            '/auth/login/bytoken/',
            data = {
                settings.LOGIN_TOKEN_KEY: "7iOyhHkUX1nAyhnP6zIGa4",
            }
        )
        self.assertEqual(resp.status_code, 200)
        assert resp.data[settings.LOGIN_TOKEN_KEY]

    def test_mybar_get(self):
        resp = self.client.get('/bars/mybar/')
        self.assertEqual(resp.status_code, 200)

    def test_mybar_post(self):
        resp = self.client.post('/bars/mybar/')
        self.assertEqual(resp.status_code, 405)

    def test_mybar_edit(self):
        resp = self.client.put(
            '/bars/mybar/',
            data='{"name":"changed"}',
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['name'], 'changed')
        resp = self.client.get('/bars/mybar/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['name'], 'changed')

    def test_initiate_bar(self):
        self.client.post('/auth/logout/')
        self.client.post(
            '/auth/login/bytoken/',
            data = {
                "login_token":"7iOyhHkUX1nAxlnP6zIGa4"
            }
        )
        resp = self.client.post(
            '/bars/mybar/initiate/',
            data = {
                "name":"Trinity",
                "address1":"Main st.",
                "city":"Charlottesville",
                "state":"Virginia",
                "zip_code":"22903"
            }
        )
        data = json.loads(resp.content)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['id'], 2)
        self.assertEqual(data['name'], 'Trinity')







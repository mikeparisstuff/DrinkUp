from django.test import TestCase
import json

class TestUsersNotLoggedIn(TestCase):

    fixtures = ['test_fixtures.json']

    def setUp(self):
        pass

    def test_not_logged_in(self):
        resp = self.client.get('/users/myprofile/')
        self.assertEqual(resp.status_code, 403)

    def test_login_bad_payload(self):
        resp = self.client.post(
            '/auth/login/bytoken/',
            data={},
        )
        self.assertEqual(resp.status_code, 401)

    def test_login_new_user(self):
        resp = self.client.post(
            '/auth/login/newuser/',
            data={
                "email":"test@example.com",
                "role":"user",
                "first_name": "John",
                "last_name": "Doe",
                "password": "test_secret"
            }
        )
        self.assertEqual(resp.status_code, 201)
        assert resp.data['login_token']

class TestUsersLoggedIn(TestCase):

    fixtures = ['test_fixtures.json']

    def setUp(self):
        resp = self.client.post(
            '/auth/login/bytoken/',
            data={
                "login_token": "7iOyhHkUt1nAylnP6zIGa4",
            }
        )
        print('Response code {}'.format(resp.status_code))
        self.assertEqual(resp.status_code, 200)
        assert resp.data['login_token']

    def test_log_out_post(self):
        resp = self.client.post('/auth/logout/')
        self.assertEqual(resp.status_code, 200)

    def test_log_out_get(self):
        resp = self.client.get('/auth/logout/')
        self.assertEqual(resp.status_code, 200)

    def test_login_while_already_logged_in(self):
        resp = self.client.post(
            '/auth/login/bytoken/',
            data={},
        )
        self.assertEqual(resp.status_code, 200)
        assert resp.data['login_token']

    def test_login_with_email_while_already_logged_in(self):

        # Giving valid data
        resp = self.client.post(
            '/auth/login/byemail/',
            data = {
                "email": "janedoe@example.com",
                "password": "password"
            }
        )
        self.assertEqual(resp.status_code, 200)
        assert resp.data['login_token']

        # Giving invalid data
        resp = self.client.post(
            '/auth/login/byemail/',
            data = {},
        )
        self.assertEqual(resp.status_code, 200)
        assert resp.data['login_token']

    def test_my_profile_view(self):
        resp = self.client.get('/users/myprofile/')
        self.assertEqual(resp.status_code, 200)

    def test_my_profile_put(self):
        # NOTE: the data payload is a little different for the PUT call compared
        # to the POST calls for the django client.  According to this
        # stackoverflow post...
        #
        # http://stackoverflow.com/questions/15153048/
        #
        # ...it looks like it's due to changes in the client class since 1.5
        resp = self.client.put(
            '/users/myprofile/',
            data = '{"first_name": "TestName"}',
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/users/myprofile/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['user']['first_name'], "TestName")

    def test_my_profile_put_bad_payload(self):
        resp = self.client.put(
            '/users/myprofile/',
            data='{"user":"BOGUS"}',
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, 400)

    def test_profile_list(self):
        resp = self.client.get(
            '/users/users/',
        )
        self.assertEqual(resp.status_code, 200)

    def test_profile_bad_method(self):
        resp = self.client.post(
            '/users/users/',
            data={}
        )
        self.assertEqual(resp.status_code, 405)
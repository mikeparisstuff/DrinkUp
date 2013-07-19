from django.test import TestCase


class TestChargeCustomers(TestCase):

    fixtures = ['test_fixtures.json']

    def setUp(self):
        # Create a new Customer
        resp = self.client.post(
            '/auth/login/newuser/',
            data = {
                "email":"test_customer@payments.com",
                "password":"password",
                "first_name":"Paying",
                "last_name":"Customer"
            }
        )
        self.assertEqual(resp.status_code, 201)
        assert resp.data['login_token']
        login_token = resp.data['login_token']

        resp = self.client.post(
            '/auth/login/bytoken/',
            data={
                "login_token": "{}".format(login_token),
            }
        )
        print('Response code {}'.format(resp.status_code))
        self.assertEqual(resp.status_code, 200)
        assert resp.data['login_token']

        # Update customers credit card
        resp = self.client.post(
            '/customers/update/card/',
            data = {
                "stripeToken": "tok_2DpPQbTv7UNqoB"
            }
        )
        self.assertEqual(resp.status_code, 302)
        print resp.content

    def test_charge_customer(self):
        resp = self.client.post(
            '/customers/charge/new/',
            data = {
                "amount": 20.00,
                "description": "Test Charge"
            }
        )
        self.assertEqual(resp.status_code, 200)

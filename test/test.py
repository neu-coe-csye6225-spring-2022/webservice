from django.test import TestCase


class Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_healthz(self):
        response = self.client.get('/healthz/')
        self.assertEqual(response.status_code, 200)

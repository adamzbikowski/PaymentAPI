from django.test import TestCase
import requests
from .views import GetFormFields
from .models import User, Transaction, Billing

# Create your tests here.
URL = 'https://sc20aaz.pythonanywhere.com'
# URL = 'http://127.0.0.1:8000'
class TestGetFormFields(TestCase):

    def test_get_form_fields(self):
        response = requests.get(f'{URL}/payment/form')
        data = response.json()
        self.assertEqual(data, {'fields' : {'Username':'String', 'Password':'String'}})

class TestMakeTransaction(TestCase):

    def setUp(self) -> None:
        User.objects.create(user_id=1,
                            username='adam',
                            email='azbik314@gmail.com',
                            password='7b91a768d920d7ed49995239d948522db110f21d03f561e175993f2b3635c213',
                            salt='22yLUkKC&c88',
                            balance=1_000_000.0,
                            currency_id=1)
        
    # three test cases designed to check how the endpoint handles incorrectly formatted payloads
    def test_check_payload(self):
        # empty  payload
        payload = {}
        response = requests.post(f'{URL}/payment/pay',json=payload)
        data = response.json()
        print(data)
        self.assertEqual(data.get('status'), 'failed')
        self.assertEqual(data.get('error'), 'Incorrect payload')

        # missing fields
        payload = { 'transaction':
                   {'amount':100,'currency':'GBP', 'recipient account':'airline', 'reference':'21231231'}}
        response = requests.post(f'{URL}/payment/pay',json=payload)
        data = response.json()
        print(data)
        self.assertEqual(data.get('status'), 'failed')
        self.assertEqual(data.get('error'), 'Incorrect payload')

        # missing transaction
        payload = {'fields':{'Username':'azbik314@gmail.com','Password':'hashtest'},
                        }
        response = requests.post(f'{URL}/payment/pay',json=payload)
        data = response.json()
        print(data)
        self.assertEqual(data.get('status'), 'failed')
        self.assertEqual(data.get('error'), 'Incorrect payload')



    def test_check_credentials(self):

         # correct credentials usign email as username
        payload = {'fields':{'Username':'azbik314@gmail.com','Password':'hashtest'},
                         'transaction':
                         {'amount':100,'currency':'GBP', 'recipient account':'airline', 'reference':'21231231'}}
        response = requests.post(f'{URL}/payment/pay',json=payload)
        data = response.json()
        print(response.json())
        self.assertEqual(data.get('status'), 'success')

      
        # username does not exist in database
        payload = {'fields':{'Username':'notauser','Password':'wrongpassword'},
                         'transaction':
                         {'amount':100,'currency':'GBP', 'recipient account':'airline', 'reference':'21231231'}}
        response = requests.post(f'{URL}/payment/pay',json=payload)
        data = response.json()
        print(data)
        self.assertEqual(data.get('status'), 'failed')
        self.assertEqual(data.get('error'), 'User does not exist')

        # incorrect password
        payload = {'fields':{'Username':'adam','Password':'wrongpassword'},
                         'transaction':
                         {'amount':100,'currency':'GBP', 'recipient account':'airline', 'reference':'21231231'}}
        response = requests.post(f'{URL}/payment/pay',json=payload)
        data = response.json()
        print(data)
        self.assertEqual(data.get('status'), 'failed')
        self.assertEqual(data.get('error'), 'Incorrect password')



    def test_make_payment(self):
        # correct credentials
        payload = {'fields':{'Username':'adam','Password':'hashtest'},
                         'transaction':
                         {'amount':100,'currency':'GBP', 'recipient account':'airline', 'reference':'21231231'}}
        response = requests.post(f'{URL}/payment/pay',json=payload)
        data = response.json()
        print(response.json())
        self.assertEqual(data.get('status'), 'success')

        # test payment with currency exchange
        payload = {'fields':{'Username':'adam','Password':'hashtest'},
                         'transaction':
                         {'amount':100,'currency':'USD', 'recipient account':'airline', 'reference':'21231231'}}
        response = requests.post(f'{URL}/payment/pay',json=payload)
        data = response.json()
        print(response.json())
        self.assertEqual(data.get('status'), 'success')

        

class TestRefundTransaction(TestCase):
    pass
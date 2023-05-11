from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from hashlib import sha256
from .models import User, Billing, Transaction
import json
import requests

# Create your views here.
BANK_URL = 'https://sc19jt.pythonanywhere.com'

@require_http_methods(['GET'])
def GetFormFields(request):
    return JsonResponse({'fields' : {'Username':'String', 'Password':'String'}})

@csrf_exempt
@require_http_methods(['POST'])
def MakeTransaction(request):
    try:
        data = json.loads(request.body)
        fields = data.get('fields')
        username = fields.get('Username')
        password = fields.get('Password')
        recipient_account = fields.get('recipient account')

        # check if user exists
        user_object = None
        try:
            user_object = User.objects.get(username=username)
        except:
            return JsonResponse({'status':'failed','error':'User does not exist'})

        # authenticate user
        salt = user_object.salt
        # print(salt)
        password_bytes = bytes(f'{password}{salt}','utf-8')
        password_hash = sha256(password_bytes).hexdigest()
    
        if password_hash != user_object.password:
            # print('incorrect password')
            return JsonResponse({'status':'failed','error':'Incorrect password'}) 

        
        transaction = data.get('transaction')
        currency = transaction.get('currency')
        amount = transaction.get('amount')
        if currency != 'GBP':
            
            try:
                response = requests.get(f'{BANK_URL}/bank/exchange/{currency}/{amount}')
                print(response)
            except:
                # return JsonResponse(response)
                return JsonResponse({'status':'failed','error':'Could not contact bank'}) 

        
        if user_object.balance < amount:
            return JsonResponse({'status':'failed','error':'Balance is too low'})


        # send request to bank
        try:
            payload = {'amount':amount, 'companyName':recipient_account}
            # response = requests.post(f'{BANK_URL}/bank/pay', json=payload)
            # data = response.json()
            # print(data)
        except:
            return JsonResponse({'status':'failed','error':'Could not contact bank'}) 

        # remove money from payers account 
        user_object.balance -= amount
        user_object.save()

        # add transaction to database
        t = Transaction(user_id=user_object.user_id,
                        amount=amount,
                        currency_id=currency,
                        fee=0,
                        confirmed=True,
                        recipient_id=1)
        t.save()
        transaction_id = t.transaction_id
        return JsonResponse({'status':'success', 'TransactionID':transaction_id})
    except:
        return JsonResponse({'status':'failed','error':'Incorrect payload'})


@csrf_exempt
@require_http_methods(['POST'])
def RefundPayment(request):
    try:

        data = json.loads(request.body)
        transaction_id = data.get('TransactionID')
        booking_id = data.get('BookingID')

        try:

            pass
        except:
            return JsonResponse({'status':'failed','error':'Transaction does not exist'})
        return JsonResponse({'status':'success'})
    except:
        return JsonResponse({'status':'failed','error':'Incorrect payload'})
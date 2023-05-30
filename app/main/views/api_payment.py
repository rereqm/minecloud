import hashlib
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from main.views.payment import *
from project.settings import TOKEN, YOOMONEY_SECRET_KEY, ACCOUNT_ID
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from main.models import User


@login_required(login_url='/login/')
def create_payment(request):
    if request.method == 'POST':
        payment = Payment(TOKEN, YOOMONEY_SECRET_KEY, ACCOUNT_ID)
        payment_id = request.user.id
        amount = request.POST['amount']
        url = payment.quickpay(amount, payment_id)
        print(url)
        return redirect(url)
    else:
        raise PermissionDenied


@csrf_exempt
def yoomoney(request):
    if request.method == 'POST':
        data = request.POST.dict()
        print(data)
        sha1_check = f'{data["notification_type"]}&{data["operation_id"]}&' \
                     f'{data["amount"]}&{data["currency"]}&{data["datetime"]}&{data["sender"]}' \
                     f'&{data["codepro"]}&{YOOMONEY_SECRET_KEY}&{data["label"]}'
        hash_check = hashlib.sha1(sha1_check.encode()).hexdigest()
        if str(hash_check) == str(data['sha1_hash']):
            user = User.objects.get(id=data["label"])
            user.money += float(data['amount'])
            user.save()
        return JsonResponse({'status': 200})
    else:
        raise PermissionDenied

import logging

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages
from decimal import Decimal

from braintree import Customer
from django_common.http import JsonResponse
from django_common.helper import form_errors_serialize
from django_common.decorators import ssl_required

from django_braintree.forms import UserCCDetailsForm
from django_braintree.forms import SubmerchantForm
from django_braintree.models import UserVault
import braintree





BAD_CC_ERROR_MSG = 'Oops! Doesn\'t seem like your Credit Card details are correct. Please re-check and try again.'
BAD_PAY_ERROR_MSG='NO FAIL TO PAY'
@ssl_required()
@login_required


def webhooks(request):
    if request.method=="GET":
        bt_challenge_param=request.GET['bt_challenge_param']
        braintree.WebhookNotification.verify(bt_challenge_param)
    elif request.method =="POST":
        bt_signature_param=request.POST['bt_signature_param']
        bt_payload_param=request.POST['bt_payload_param']
    
        notification = braintree.WebhookNotification.parse(
          bt_signature_param,
          bt_payload_param
        )
        notification.kind == braintree.WebhookNotification.Kind.SubMerchantAccountDeclined
    print notification.message
def registerForm(request):
    form = SubmerchantForm(request.POST)
    
def submit(request):
    if request.method == "POST":
        amount=request.POST['amount']
        merchant_id=str(request.POST['merchant'])
        number=str(request.POST['number'])
        expiration_date=str(request.POST['expiration_date'])
        fee=amount*0.1
        result = braintree.Transaction.sale({
                  "amount": str(amount),
                  "merchant_account_id": merchant_id,
                  "credit_card": {
                    "number": str(number),
                    "expiration_date": str(expiration_date),
                  },
                  "options": {
                    "submit_for_settlement": True,
                    "hold_in_escrow": True,
                  },
                  "service_fee_amount": fee
            })
        if result.is_success:
            return render(request, "success.html")
        else:
            return JsonResponse(success=False, errors=[BAD_CC_ERROR_MSG])
def pay_bill(request,template1='django_braintree/fragments/pay.html'):
    d={}
    #d['current_cc_info']=['00']
    d['cc_form_post_url']=""
    d['cc_form'] = UserCCDetailsForm(request.user)
    if request.method == 'POST':
        print UserVault.objects.all()
        if UserVault.objects.is_in_vault(request.user):
            try:
                vault=UserVault.objects.get_user_vault_instance_or_none(request.user)
                response=vault.charge(Decimal(10))
                if response.is_success:
                    messages.add_message(request, messages.SUCCESS, 'Your credit card information has been securely saved.')
                    return JsonResponse()
                else:
                    return JsonResponse(success=False, errors=[BAD_CC_ERROR_MSG])
   
            except Exception, e:
                logging.error('Unable to get vault information for user from braintree. %s' % e)
            d['cc_form'] = UserCCDetailsForm(request.user)
        else:
            '''
            user=request.user        
            form= UserCCDetailsForm(request.user, True, request.POST)
            #vault = UserVault.objects.create(user=user, vault_id="1cf373103e6657b96421348a")
            # Credit Card is being changed/updated by the user
            result=braintree.transaction.sale({
                                                   "amount":"1000",
                                                   "credit_card":{
                                                                  number:request.form["number"]
                                                                  }
                                                   })
       
            '''
    return render(request, template1, d)                 
def payments_billing(request, template='django_braintree/pay.html'):
    """
    Renders both the past payments that have occurred on the users credit card, but also their CC information on file
    (if any)
    """
    d = {}
    
    if request.method == 'POST':
        # Credit Card is being changed/updated by the user
        form = UserCCDetailsForm(request.user, True, request.POST)
        if form.is_valid():
            response = form.save()# actually ,here ,we create a vault 
            print response.is_success
            print response
           
            
           
            if response.is_success:
                messages.add_message(request, messages.SUCCESS, 'Your credit card information has been securely saved.')
                return JsonResponse()
            else:
                return JsonResponse(success=False, errors=[BAD_CC_ERROR_MSG])
        return JsonResponse(success=False, data={'form': form_errors_serialize(form)})
    else:
        if UserVault.objects.is_in_vault(request.user):
            try:
                response = Customer.find(UserVault.objects.get_user_vault_instance_or_none(request.user).vault_id)
                d['current_cc_info'] = response.credit_cards[0]
                print d['current_cc_info']
            except Exception, e:
                logging.error('Unable to get vault information for user from braintree. %s' % e)
        d['cc_form'] = UserCCDetailsForm(request.user)
    return render(request, 'django_braintree/payments_billing.html', d)

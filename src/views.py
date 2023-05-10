from django.shortcuts import render
import razorpay
from .models import Coffee
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

def home(request):
    if request.method == "POST":
        name = request.POST.get("name")
        amount = int(request.POST.get("amount"))*100
        key,secret = "rzp_test_neXHIjM8IeaR1s","xcggAF7xvuK85FLT8G382mB0"
        client= razorpay.Client(auth = ( key,secret ))
        payment = client.order.create({'amount':amount, 'currency':'INR',
                              'payment_capture':'1' })
        print(payment)
        coffee = Coffee(name = name , amount =amount , payment_id = payment['id'])
        coffee.save()
        return render(request, 'index.html' ,{'payment':payment,'key':key})
    return render(request,"index.html")




@csrf_exempt
def success(request):
    if request.method == "POST":
        a =  (request.POST)
        order_id = ""
        for key , val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
    
        user = Coffee.objects.filter(payment_id = order_id).first()
        user.paid = True
        user.save()
        return render(request, "success.html")
from django.shortcuts import render

# Create your views here.
def registration(request):
    return render(request, 'user/Registration.html')

def entrance(request):
    return render(request, 'user/entrance.html')
from urllib import request
from django.http import HttpResponseRedirect
from django.shortcuts import  render, redirect
from django.urls import reverse
from . forms import NewUserForm
from django.contrib.auth import login, authenticate ,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.views.generic.detail import DetailView

from . utilities import find_car,create_dataset
from .models import mylist

def car_detail(request,id):
    id = int(id)
    df = create_dataset()
    df = df.loc[df['id'] == id]
    object = list(df.values[0])

    
    context= {'object':object}

    return render(request, 'details.html',context)

def mycar_list(request,username):
    mylist_cars = mylist.objects.filter(user = request.user)
    for i in mylist_cars:
        print(i.id)
    

    context ={'mylist_cars':mylist_cars} 
    return render(request, 'mylist.html',context)
def addlist(request,id):
    id = int(id)
    df = create_dataset()

    df = df.loc[df['id'] == id]
    
    add_car = mylist(user= request.user,id =df.iloc[0].id,model=df.iloc[0].model,company=df.iloc[0].company,year=df.iloc[0].year ,price=df.iloc[0].price ,transmission=df.iloc[0].transmission ,mileage=df.iloc[0].mileage,fueltype=df.iloc[0].fuelType ,tax=df.iloc[0].tax ,mpg=df.iloc[0].mpg ,enginesize=df.iloc[0].engineSize)
    add_car.save()


    return redirect('recommend')

def recommend(request):

    df = create_dataset()

    price = request.session['price'] 
    company = request.session['company'] 
    fuelType = request.session['fuelType'] 
    
    rec_cars = find_car(df,price,company,fuelType)
    
    rec1 = [rec_cars.iloc[0]['id'],rec_cars.iloc[0]['company'],rec_cars.iloc[0]['model'],rec_cars.iloc[0]['price'],rec_cars.iloc[0]['fuelType'],rec_cars.iloc[0]['year']]
    rec2 = [rec_cars.iloc[1]['id'],rec_cars.iloc[1]['company'],rec_cars.iloc[1]['model'],rec_cars.iloc[1]['price'],rec_cars.iloc[1]['fuelType'],rec_cars.iloc[1]['year']]
    rec3 =  [rec_cars.iloc[2]['id'],rec_cars.iloc[2]['company'],rec_cars.iloc[2]['model'],rec_cars.iloc[2]['price'],rec_cars.iloc[2]['fuelType'],rec_cars.iloc[2]['year']]
    rec4 = [rec_cars.iloc[3]['id'],rec_cars.iloc[3]['company'],rec_cars.iloc[3]['model'],rec_cars.iloc[3]['price'],rec_cars.iloc[3]['fuelType'],rec_cars.iloc[3]['year']]    

    mylist_cars = mylist.objects.filter(user = request.user)
    carsids= []
    for car in mylist_cars:
        carsids.append(int(car.id))
    print(carsids)
    context = {
        'data': [rec1,rec2,rec3,rec4],
        'cars':carsids
    }

    return render(request, 'recommend.html',context)
    
def homepage(request):
    if request.method == "POST":
        

        price= int(request.POST["price"])
        company =str(request.POST["company"]) 
        fuelType = str(request.POST["fuelType"])

        request.session['price'] = price
        request.session['company'] = company
        request.session['fuelType'] = fuelType
        return redirect("recommend")
    
    return render(request, 'index.html')

    
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                print("hello")
                login(request, user)
                
                return redirect("homepage")
            else:
                print("hello2")
                messages.error(request,"Invalid username or password.")
        else:
            print("heell")
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})


def logout_view(request):
    logout(request)
    return redirect('login')
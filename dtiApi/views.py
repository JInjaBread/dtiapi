import requests
import json
import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework import permissions, generics, filters
import django_filters.rest_framework
from .models import Products, Concern, Data
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ProductSerializer, ConcernSerializers, DataSerializer
from .resource import ProductResource
from tablib import Dataset

from .EmailBackend import EmailBackEnd

class ProductsListView(generics.ListCreateAPIView):
    search_fields = ['product_name']
    filter_backends = (filters.SearchFilter,)
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

@api_view(['GET'])
def getProductsBasic(request):
    basic_products = Products.objects.filter(main_category = 'BASIC NECESSITIES')
    serializer = ProductSerializer(basic_products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getProductsPrime(request):
    prime_products = Products.objects.filter(main_category = 'PRIME COMMODITIES')
    serializer = ProductSerializer(prime_products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getConcern(request):
    concern = Concern.objects.all()
    serializer = ConcernSerializers(concern, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getPDF(request):
    data_pdf = Data.objects.all().order_by('-publish_at')
    serializer = DataSerializer(data_pdf, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@parser_classes([MultiPartParser])
@parser_classes([FormParser])
def sendConcern(request):
    serializer = ConcernSerializers(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print("success")
        return Response(serializer.data)
    else:
        print(serializer.errors)
        return Response(serializer.errors)

@api_view(['POST'])
def api_login(request):
    data = request.data
    try:
        email = data['email']
        password = data['password']
        user = EmailBackEnd.authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            global current_email
            current_email = email
            return Response("Validated")
        else:
            return Response("Failed")
    except Exception as e:
        print(e)
        return Response("Invalid Credentials")

@api_view(['GET'])
def current_user(request):
    user = request.user
    return Response({
        'email': current_email,
})

#generics views

def home(request):
    return render(request, "home.html")

def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if user != None:
            login(request, user)
            #return HttpResponse("Email: "+request.POST.get('email')+ " Password: "+request.POST.get('password'))
            if user.is_superuser == True:
                return redirect('dashboard')
            else:
                return redirect('home')
        else:
            return redirect('home')

def logout_user(request):
    logout(request)
    return redirect('home')

def dashboard(request):
    products = Products.objects.all().count
    complains = Concern.objects.all().count

    context = {
        "products": products,
        "complains": complains
    }

    return render(request, "dashboard.html", context)

def products(request):

    products =[]

    if 'table_search' in request.GET:
        table_search = request.GET['table_search']
        q = Q(product_name__icontains=table_search)
        products_data = Products.objects.filter(q)
        if products_data.count() == 0:
            messages.error(request, "No Data Found!")
            print("NO DATA FOUND")
        else:
            for product in products_data:
                products.append(product)
    else:
        products_data = Products.objects.all()
        for product in products_data:
            products.append(product)
    context = {
        "products": products,
    }
    return render(request, "products.html", context)


def add_products(request):
    category = request.POST.get('product_category')
    product_name = request.POST.get('product_name')
    product_price = request.POST.get('product_price')
    product_unit = request.POST.get('product_unit')
    product_description = request.POST.get('product_description')
    main_category = request.POST.get('main_category')
    product_category = ProductCategory.objects.get(id=category)

    if len(request.FILES) != 0:
        product_image = request.FILES['product_image']
        fs = FileSystemStorage()
        filename = fs.save(product_image.name, product_image)
        product_image_url = fs.url(filename)
    else:
        product_image_url = None

    try:
        product = Products(product_name=product_name, prooduct_price=product_price, product_image=product_image_url, product_unit=product_unit, product_description=product_description, main_category=main_category, product_category=product_category)
        product.save()
        print('Product Save')
        return redirect('products')
    except Exception as e:
        print(e)
        return redirect('products')

def add_products_resource(request):
    product_resource = ProductResource()
    dataset = Dataset()
    data_object = request.FILES["resource"]

    message = 'As of ' + str(datetime.datetime.now()) + ' dti app updated its prices you may now view updated prices in the app'

    staff_user = User.objects.filter(is_staff=True)

    staff = []

    for staff_user in staff_user:
        check = User.objects.get(id=staff_user.id)
        if check.is_superuser == False:
            staff.append(check)
        else:
            pass

    if data_object.name.endswith('xlsx'):
        try:
            imported_data = dataset.load(data_object.read(), format='xlsx')
            for data in imported_data:
                txt = data[0]
                x = txt.split(",")
                print(x[0])
                check = Products.objects.filter(product_name = x[0], product_unit=x[1]).exists()
                if check == False:
                    date = str(data[15])
                    product = Products(product_name=x[0], product_srp=data[1],supermarket_price=data[3], wetmarket_price=data[5], product_unit=x[1], main_category=data[14], as_of=data[15])
                    product.save()
                else:
                    product = Products.objects.get(product_name = x[0], product_unit=x[1])
                    product.product_srp = data[1]
                    product.supermarket_price = data[3]
                    product.wetmarket_price = data[5]
                    product.as_of = datetime.datetime.now()
                    product.save()
            for staff in staff:
                send_mail(
                    'DTI APP PRICES UPDATE',message,'examplefordti@gmail.com',[staff.email]
                )
            messages.success(request, "Add/Update of products success!")
            return redirect('products')
        except:
                messages.success(request, "Add/Update of products success!")
                return redirect('products')
    else:
        print("this is the error")
        messages.error(request, "Error please check your resource file!")
        return redirect('products')


def delete_products(request, product_id):

    product = Products.objects.get(id=product_id)

    try:
        product.delete()
        return redirect('products')
    except:
        print('failed to delete')
        return redirect('products')

def update_image(request, product_id):

    if len(request.FILES) != 0:
        product_image = request.FILES['product_image']
        fs = FileSystemStorage()
        filename = fs.save(product_image.name, product_image)
        product_image_url = fs.url(filename)
    else:
        product_image_url = None

    try:
        product = Products.objects.get(id=product_id)
        product.product_image = product_image_url
        product.save()
        messages.success(request, "Product Image Upload Succesfully!")
        return redirect('products')
    except Exception as e:
        print(e)
        messages.error(request, "Product Image Upload Failed!")
        return redirect('products')

def complains(request):
    complains = Concern.objects.all()

    complains_unreplied = Concern.objects.filter(concern_adress=False)

    complains_replied = Concern.objects.filter(concern_adress=True)

    context = {
        "complains": complains,
        "complains_unreplied": complains_unreplied,
        "complains_replied": complains_replied
    }

    return render(request, "complains.html", context)

def address_complains(request, complains_id):
    complains = Concern.objects.get(id=complains_id)

    store = User.objects.get(email=complains.complainant_email)
    context = {
        "complains": complains,
        "store": store
    }

    return render(request, "address_complains.html", context)

def address_complains_send(request, complains_id):
    complains = Concern.objects.get(id=complains_id)
    subject = request.POST.get('subject')
    message = request.POST.get('messages')
    email = request.POST.get('email')

    try:
        send_mail(
            subject,message,'examplefordti@gmail.com',[email]
        )
        complains.concern_adress = True
        complains.save()
        messages.success(request, "Reply Sent")
        return redirect('/address_complains/' + str(complains.id))
    except:
        messages.error(request, "Please Complete the Form!")
        return redirect('/address_complains/' + str(complains.id))

def data(request):

    data = Data.objects.all()

    context ={
        "data": data
    }
    return render(request, "data.html", context)

def data_save(request):

    if len(request.FILES) != 0:
        data_file = request.FILES['resource']
        fs = FileSystemStorage()
        filename = fs.save(data_file.name, data_file)
        data_file_url = fs.url(filename)
    else:
        data_file_url = None

    try:
        data = Data(data_file=data_file_url)
        data.save()
        return redirect('data')
    except:
        print('error')
        return redirect('data')

def categories(request):

    categories = ProductCategory.objects.all()

    context = {
        "categories": categories
    }
    return render(request, "categories.html", context)

def categories_save(request):
    category = request.POST.get('product_category')

    try:
        pc = ProductCategory(category_name=category)
        pc.save()
        print('saved')
        return redirect('categories')
    except:
        print('error')
        return redirect('categories')

def accounts(request):
    staff_user = User.objects.filter(is_staff=True)

    staff = []

    for staff_user in staff_user:
        check = User.objects.get(id=staff_user.id)
        if check.is_superuser == False:
            staff.append(check)
        else:
            pass

    context = {
        "staff": staff
    }
    return render(request, "accounts.html", context)

def save_account(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    url = "https://api.apilayer.com/email_verification/check?email=" + email

    payload = {}
    headers= {
      "apikey": "ApvDrCuwpz8hiq3RWg2lrw9xpmcwM3Iv"
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    result = response.json()
    smtp_check = result["smtp_check"]

    if smtp_check == True:
        try:
            user = User.objects.create_user(username, email, password)
            user.is_staff = True
            user.save()
            messages.success(request, "User save succesfully!")
            return redirect('accounts')
        except:
            messages.error(request, "Email Already Exist!")
            return redirect('accounts')
    else:
        messages.error(request, "Email Is Not Valid!")
        return redirect('accounts')

def delete_account(request, store_id):
    staff_user = User.objects.get(id = store_id)

    try:
        staff_user.delete()
        messages.success(request, "Store succesfully deleted!")
        return redirect('accounts')
    except:
        messages.error(request, "Unsucessfull Deeletion of Account!")
        return redirect('accounts')

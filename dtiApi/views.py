from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny
from .models import Products, Concern, ProductCategory, Data
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ProductSerializer, ConcernSerializers, DataSerializer
from .resource import ProductResource
from tablib import Dataset

from .EmailBackend import EmailBackEnd

@api_view(['GET'])
def getData(request):
    products = Products.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

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
            messages.error(request, "Invalid Login Credentials!")
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
    products = Products.objects.all()
    category = ProductCategory.objects.all()

    context = {
        "products": products,
        "category": category
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

    if data_object.name.endswith('xlsx'):
        try:
            imported_data = dataset.load(data_object.read(), format='xlsx')
            for data in imported_data:
                category = ProductCategory.objects.get(category_name=data[6])
                print(data[2])
                product = Products(product_name=data[0], prooduct_price=data[1], product_image=data[2], product_unit=data[3], product_description=data[4], main_category=data[5], product_category=category)
                product.save()
            print('Saved')
            return redirect('products')
        except Exception as e:
                print(e)
                return redirect('products')


def delete_products(request, product_id):

    product = Products.objects.get(id=product_id)

    try:
        product.delete()
        return redirect('products')
    except:
        print('failed to delete')
        return redirect('products')

def update_price(request, product_id):

    product_price = request.POST.get('price')

    try:
        product = Products.objects.get(id=product_id)
        product.prooduct_price = product_price
        product.save()
        print('Updated')
        return redirect('products')
    except Exception as e:
        print(e)
        return redirect('products')

def complains(request):
    complains = Concern.objects.all()

    context = {
        "complains": complains
    }

    return render(request, "complains.html", context)

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
        print('saved')
        return redirect('data')
    except:
        print('error')
        return redirect('data')

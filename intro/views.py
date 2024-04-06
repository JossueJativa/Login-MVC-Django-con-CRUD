from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import products

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return render(request, 'home.html', {
                'user': user,
                'products': products.objects.all(),
            })
        else:
            return render(request, 'login.html', {'error': 'Invalido usuario o contraseña'})
    else:
        return render(request, 'login.html')

def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name')
            price = request.POST.get('price')
            stock = request.POST.get('stock', 0)
            photo = request.FILES.get('photo')

            product = products(name=name, price=price, stock=stock, photo=photo)
            product.save()

            return render(request, 'home.html', {
                'products': products.objects.all(),
            })
        else:
            return render(request, 'home.html', {
                'products': products.objects.all(),
            })
    else:
        return render(request, 'login.html', {'error': 'Necesitas estar logeado para ingresar'})
    
def edit(request, id):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'error': 'Necesitas estar logeado para ingresar'})
    
    product = products.objects.get(id=id)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock', 0)
        photo = request.FILES.get('photo')
        if photo:
            product.photo = photo
        
        product.save()
        
        return render(request, 'home.html', {
            'products': products.objects.all(),
        })
    else:
        return render(request, 'edit.html', {
            'product': product,
        })
    
def delete(request, id):
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'error': 'Necesitas estar logeado para ingresar'})
    
    product = products.objects.get(id=id)
    product.delete()
    return render(request, 'home.html', {
        'products': products.objects.all(),
    })
    
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'login.html', {'error': 'Has salido de la aplicación'})
    else:
        return render(request, 'login.html', {'error': 'No puedes salir si no has ingresado'})
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password == password2:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                user = authenticate(request, username=username, password=password)
                login(request, user)
                return render(request, 'home.html')
            except:
                return render(request, 'register.html', {'error': 'El usuario ya existe'})
        else:
            return render(request, 'register.html', {'error': 'Las contraseñas no coinciden'})
    return render(request, 'register.html')
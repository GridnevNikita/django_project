from django.shortcuts import render
from catalog.models import Product, Contact


def home(request):
    last_products = Product.objects.order_by('-created_at')[:5]
    for prod in last_products:
        formatted_date = prod.created_at.strftime("%d.%m.%Y %H:%M")
        print(f"Название: {prod.name} | Цена: ${prod.price:,.2f} | Создано: {formatted_date}")
    return render(request, 'catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        user_message = request.POST.get('message')
        Contact.objects.create(name=name, phone=phone, message=user_message)
        return render(request, 'catalog/thanks.html', {'name': name})

    all_contacts = Contact.objects.all()
    return render(request, 'catalog/contacts.html', {'contacts': all_contacts})

from django.shortcuts import render
from products.models import Product
from .amazon import FetchfromAmazon
from .flipkart import Fetchfromflipkart
from .snapdeal import FetchfromSnapdeal


def clean(query):
    flipkart_data = Fetchfromflipkart(query)
    amazon_data = FetchfromAmazon(query)
    snapdeal_data = FetchfromSnapdeal(query)
    data = [flipkart_data, snapdeal_data, amazon_data]
    return data


def do_search(request):
    print(request.POST)
    query = request.POST['q']

    form = clean(query)
    Flipkart_product = form[0]
    for item_details in Flipkart_product:
        product_details_flip = Product.objects.create(brand=item_details[0],name=item_details[1]+' | '+query.capitalize(),price=item_details[2],rating=item_details[3],
                                                      image=item_details[4],url=item_details[5],seller="Flipkart")
    Snapdeal_product = form[1]
    for item_details in Snapdeal_product:
        product_details_snap = Product.objects.create(brand=item_details[0],name=item_details[1]+' | '+query.capitalize(),price=item_details[2],rating=item_details[3],
                                                      image=item_details[4],url=item_details[5],seller="Snapdeal")
    Amazon_product = form[2]
    for item_details in Amazon_product:
        product_details_Amzn = Product.objects.create(brand=item_details[0],name=item_details[1]+' | '+query.capitalize(),price=item_details[2],rating=item_details[3],
                                                          image=item_details[4],url=item_details[5],seller="Amazon")
    products = Product.objects.filter(name__icontains=query).distinct()
    context = {
        "products": products,
    }
    return render(request,"search/result.html",context)



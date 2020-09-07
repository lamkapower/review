from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from .models import Product, Review
from .forms import ReviewForm


def product_list_view(request):
    template = 'app/product_list.html'
    products = Product.objects.all()

    context = {
        'product_list': products,
    }

    return render(request, template, context)


def product_view(request, pk):
    template = 'app/product_detail.html'
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        # логика для добавления отзыва
        new_review = Review(text=request.POST.get('text'), product=product, user=request.user)
        new_review.save()
        return redirect('main_page')

    reviews = Review.objects.filter(product=product)
    product_user_reviews = Review.objects.filter(product=product, user=request.user)
    # reviews_users_id = list(map(lambda x: x.__dict__.get('user_id'), reviews))  # второй вариант
    form = ReviewForm

    context = {
        # 'is_review_exist': True if request.user.id in reviews_users_id else False,  # второй вариант
        'is_review_exist': True if len(product_user_reviews) > 0 else False,
        'reviews': reviews,
        'form': form,
        'product': product
    }

    return render(request, template, context)

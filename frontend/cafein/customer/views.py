from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from customer.forms import customerPostForm
from cafe.models import Cafe, Cafe_review, Cafe_comment

def customerHome(request):
    if request.session.get('user'):
        cafe = Cafe.objects.all()
        return render(request, 'customerHome.html', {'cafe': cafe})
    else:
        return redirect('/')


def signup(request):
    if not(request.session.get('user')):
        if request.method == 'POST':
            form = customerPostForm(request.POST, request.FILES)
            if form.is_valid():
                if not form.check_email():
                    return render_with_error(request, 'signup.html', form, ['email'])
                if not (form.check_password1() and form.check_password()):
                    return render_with_error(request, 'signup.html', form, ['password'])
                if not form.check_phone():
                    return render_with_error(request, 'signup.html', form, ['phone'])
                
                form.save()
                # Save 성공시에는 Redirect
                request.session['user'] = request.POST.get('email')
                request.session['is_owner'] = False
                return redirect('/customer/home')
        else:
            form = customerPostForm()
            return render(request, 'signup.html', {'form': form})
    return redirect('/')

def cafeHome(request, cafeName):
    cafe = Cafe.objects.get(name=cafeName)
    
    return render(request, 'cafeHome.html', {'cafe': cafe})

def cafeReview(request, cafeName):
    
    cafe_reviews = Cafe_review.objects.filter(cafe=Cafe.objects.get(name=cafeName))

    paginator = Paginator(cafe_reviews, 2)

    page_number = request.GET.get('page')
    page_reviews = paginator.get_page(page_number)

    return render(request, 'cafeReview.html', {'reviews': page_reviews, 'cafeName': cafeName})

def cafeReviewDetail(request, cafeName, reviewid):
    cafe = Cafe.objects.get(name=cafeName)
    cafe_review = Cafe_review.objects.get(cafe=cafe, review_id=reviewid)
    cafe_comment = Cafe_comment.objects.get(review=reviewid)
    
    contents = {
        'cafe_review' : cafe_review,
        'cafe_comment': cafe_comment,
        'cafeName': cafeName,
    }
    return render(request, 'cafeReviewDetail.html', {'contents': contents})

def createReview(request, cafeName):
    pass

def render_with_error(request, html, form, error_type):
    error_flg = {}
    for error in error_type:
        error_flg[error] = True
    return render(request, html, {'form': form, 'error_flg': error_flg})
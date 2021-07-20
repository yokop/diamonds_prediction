from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .data_loader import load_new_data
from .predictor import fit as predictor_fit
from .predictor import predict as predictor_predict
from .models import Diamond,Diamond_predicted,MyLog
import json
from django.core import serializers
from .forms import Diamond_prediction_form,Diamond_prediction_feedback_form



# Create your views here.
def home(request):
    return render(request,'diamonds/home.html')




def signup_user(request):
    if request.method == 'GET':
        return render(request, 'diamonds/signup_user.html',{'form':UserCreationForm})
    else: #POST
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'diamonds/signup_user.html',{'form':UserCreationForm,'err':'That username has already been taken. Please Choose a new username'})
        else:
            # error message
            return render(request, 'diamonds/signup_user.html',{'form':UserCreationForm,'err':'Passwords did not match'})



def login_user(request):
    if request.method == 'GET':
        return render(request, 'diamonds/login_user.html',{'form':AuthenticationForm})
    else: #POST
        user = authenticate(request,username=request.POST['username'],password= request.POST['password'])
        if user is None:
             return render(request, 'diamonds/login_user.html',{'form':AuthenticationForm,'err':'username and password did not match'})
        else:
            login(request,user)
            return redirect('home')


def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')



def dataset(request):

    all_diamonds = Diamond.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(all_diamonds, 100)
    try:
        diamonds = paginator.page(page)
    except PageNotAnInteger:
        print("222")
        diamonds = paginator.page(1)
    except EmptyPage:
        print("333")
        diamonds = paginator.page(paginator.num_pages)
    start = max(1,int(page) - 5)
    end = min(int(page) +5,paginator.num_pages)

    pages_range = range(start,end+1)
    info_str = f"{paginator.count} Records in {paginator.num_pages} Pages"
    return render(request, 'diamonds/dataset.html', { 'diamonds_dataset': diamonds,"pages_range": pages_range,"info_str":info_str})

def predict(request):
    if request.method == 'GET':
        is_post = request.session.get('after_prediction',False)
        if False:
            print(f"post prediction. after_prediction {request.session.get('after_prediction',False)}")
            request.session['after_prediction'] = 'no'
            pk_of_record = request.session.get('pk',None)
            if pk_of_record:
                print(f"pk is {pk_of_record}")
                prediction_entry = Diamond_predicted.objects.get(pk=pk_of_record)
                return render(request, 'diamonds/predict_result.html',{'prediction':prediction_entry})
            else:
                print("ERROR pk is none")
        else:
            print("pre prediction")
            return render(request, 'diamonds/predict.html',{'form':Diamond_prediction_form()})

            
    else:
        form = Diamond_prediction_form(request.POST)
        
        if form.is_valid():
            print('--------------')
            values = form.cleaned_data
            price = predictor_predict(values)
            print('--------------')
            new_prodected = Diamond_predicted.objects.create(carat  = values["carat"],
                                                                cut = values["cut"],
                                                                color = values["color"],
                                                                clarity = values["clarity"],
                                                                depth = values["depth"],
                                                                table = values["table"],
                                                                x = values["x"],
                                                                y = values["y"],
                                                                z = values["z"],
                                                                price_predicted = price)
            print(new_prodected.id)
            # new_prodected.carat = values["carat"]
            # new_prodected.cut = values["cut"]
            # new_prodected.color = values["color"]
            # new_prodected.clarity = values["clarity"]
            # new_prodected.depth = values["depth"]
            # new_prodected.table = values["table"]
            # new_prodected.x = values["x"]
            # new_prodected.y = values["y"]
            # new_prodected.z = values["z"]
            # new_prodected.price_predicted = price
            # new_prodected.save()
        request.session['after_prediction'] = 'yes'
        request.session['pk'] = new_prodected.id
        print(request.path)
        return redirect('/predict_result/')
        #return render(request, 'diamonds/predict_result.html',{'values':values,'prediction':price,'prediction_row_id':new_prodected.id})

def predict_result(request):
    if request.method == 'GET':
        print('predict_result start')
        perdict_id = request.session.get('pk')
        print(f"predict id in get= {perdict_id}")
        prediction_entry = Diamond_predicted.objects.get(pk=perdict_id)
        return render(request, 'diamonds/predict_result.html',{'prediction':prediction_entry,'form':Diamond_prediction_feedback_form})
    else:
        perdict_id = request.session.get('pk')
        prediction_entry = Diamond_predicted.objects.get(pk=perdict_id)

        form = Diamond_prediction_feedback_form(request.POST)
        if form.is_valid():
            values = form.cleaned_data
            prediction_entry.real_price_feedback = values["real_price_feedback"]
            prediction_entry.price_feedback =  values["price_feedback"]
            prediction_entry.imported_to_dataset = values["imported_to_dataset"]
            if prediction_entry.imported_to_dataset:
                new_diamond = Diamond.objects.create(carat  = prediction_entry.carat,
                                                    cut = prediction_entry.cut,
                                                    color = prediction_entry.color,
                                                    clarity = prediction_entry.clarity,
                                                    depth = prediction_entry.depth,
                                                    table = prediction_entry.table,
                                                    x = prediction_entry.x,
                                                    y = prediction_entry.y,
                                                    z = prediction_entry.z,
                                                    price = values["real_price_feedback"])
                prediction_entry.pointer_to_dataset = new_diamond
                prediction_entry.save()
        print(f"predict id in post= {perdict_id}")
        return redirect('/')

def my_admin_predicted_items(request):
    all_predicted = Diamond_predicted.objects.all()
    return render(request, 'diamonds/my_admin_predicted_items.html',{'predicted_dataset': all_predicted})

def my_admin_log(request):
    all_logs = MyLog.objects.all()
    return render(request, 'diamonds/my_admin_log.html',{"logs":all_logs})

def my_admin(request):
    return render(request, 'diamonds/my_admin.html')

def fit(request):
    return render(request,'diamonds/fit.html')

def ajax_load_new_dataset(request):
    print("in ajax_load_dataset")
    if request.method == 'GET':
        records_count,pages_count = load_new_data()
        info_str = f"{records_count} Records in {pages_count} Pages"
        return JsonResponse({"info":info_str})

def ajax_fit(request):
    if request.method == 'GET':
        score = predictor_fit()
        #info_str = f"Done, score is {score}"
        info_str = "Done, score is {0:.3f} %".format(100 * score)
        return JsonResponse({"info":info_str})
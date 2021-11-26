from django.shortcuts import redirect, render
from django.http import HttpResponse
from . import templates
from .forms import search_filters, signup_form, signin_form, new_property, update_form, update_login_form, photo_form
from .models import Property, User, Photo
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


# Helpers
def extract_properties(limit):
    return Property.objects.all().order_by('-id')[:limit]

# Write your views here
def index(request):
    last_two = extract_properties(2)
    return render(request, 'index.html', context={ 'properties': last_two })

@login_required
def bookmark(request, id):

    # extract property id from request
    # verify if the property exists in the db; if it does not, raise error
    property = Property.objects.filter(id=id)

    if not property.exists():
        return HttpResponse('error')
    else:
        # create an object instance of the property
        property = property.first()

    # save bookmark
    property.bookmarks.add(request.user)

    return HttpResponse('success')

def search(request):
    if request.method == 'GET':
        return render(request, 'search.html')

    elif request.method == 'POST':

        form = search_filters(request.GET)

        if form.is_valid():
            search_input = form.cleaned_data["search_input"]
            properties = Property.objects.filter(address__icontains=search_input)

            return render(request, 'search.html', context={
                'search_input': search_input,
                'properties': properties
            })

        else:
            return HttpResponse(form.errors)
            last_10 = extract_properties(10)

            return render(request, 'search.html', context={'properties': last_10})

def property(request, pk):
    try:
        property = Property.objects.get(pk=pk)
        if property:
            return render(request, 'property.html', context={'property': property})

    except Property.DoesNotExist:
        return render(request, 'property.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html')

    elif request.method == 'POST':

        form = signup_form(request.POST)

        if not form.is_valid():
            return render(request, 'signup.html', context={'form': form})

        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        postcode = form.cleaned_data["postcode"]
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        create_user = User(username=email, first_name=first_name, last_name=last_name, postcode=postcode, email=email, password=make_password(password))
        create_user.save()

        return redirect('/')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')

    elif request.method == 'POST':
        signin_instance = signin_form(request.POST)

        if signin_instance.is_valid():
            username = signin_instance.cleaned_data['email']
            password = signin_instance.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    next = request.GET.get('next')
                    if next:
                        return redirect('/' + next)
                    else:
                        return redirect('EstatelyApp:index')
            else:
                error = 'Password or email is invalid'
                return render(request, 'signin.html', context={'error':error})

def signout(request):
    logout(request)
    return redirect('EstatelyApp:index')

@login_required
def update(request):
    if request.method == 'GET':
        return render(request, 'update.html')

    if request.method == 'POST':

        user_id = request.user.id

        form = update_form(request.POST)

        if not form.is_valid():
            return render(request, 'update.html', context = { 'form': form })

        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        postcode = form.cleaned_data['postcode']

        p = User.objects.get(id=user_id)
        p.first_name = first_name
        p.last_name = last_name
        p.postcode = postcode
        p.save()

        return render(request, 'update.html', context={'success': 'We have updated your details'})

@login_required
def update_login(request):
    if request.method == 'GET':
        return render(request, 'update_login.html')

    if request.method == 'POST':

        form = update_login_form(data=request.POST or None, user=request.user)

        if not form.is_valid():
            # return HttpResponse(form.errors.items())
            return render(request, 'update_login.html', context={'form': form})

        # current_password = form.cleaned_data['current_password']
        # new_password = form.cleaned_data['new_password']
        # confirm_password = form.cleaned_data['confirm_password']

    return HttpResponse('continue this later')

@login_required
def delete_account(request):
    if request.method == 'GET':
        return render(request, 'delete_account.html')

    if request.method == 'POST':

        User.objects.filter(pk=request.user.id).delete()

        logout(request)

        return redirect("EstatelyApp:index")

@login_required
def dashboard(request):
    auth_id = request.user.id

    properties = Property.objects.filter(user_id = auth_id).exists()

    if properties:
        properties = Property.objects.filter(user_id = auth_id)
        return render(request, 'dashboard.html', context={'properties': properties})
    else:
        return render(request, 'dashboard.html')

@login_required
def post(request):
    if request.method == 'GET':
        return render(request, 'post.html')

    elif request.method == 'POST':

        # Instantiate forms
        property_form = new_property(request.POST or None)
        photo_instance = photo_form(request.POST or None, request.FILES or None)

        user_id = request.user.id

        # Form validation
        if not property_form.is_valid() or not photo_instance.is_valid():
            return render(request, 'post.html', context={'message': 'One or more inputs are invalid'})

        # Add the new property post to the db
        title = property_form.cleaned_data['title']
        type = property_form.cleaned_data['type']
        price = property_form.cleaned_data['price']
        furnish_type = property_form.cleaned_data['furnish_type']
        contract_type = property_form.cleaned_data['contract_type']
        no_bedrooms = property_form.cleaned_data['no_bedrooms']
        no_bathrooms = property_form.cleaned_data['no_bathrooms']
        features = property_form.cleaned_data['features']
        description = property_form.cleaned_data['description']
        address = property_form.cleaned_data['address']

        property_entry = Property(user_id=user_id, title=title, type=type,
            price=price, furnish_type=furnish_type, contract_type=contract_type,
            no_bedrooms=no_bedrooms, no_bathrooms=no_bathrooms,
            features=features, description=description, address=address)

        property_entry.save()

        # Add the property photo to the db (it is a different db)
        # You need to create a relationship between the db
        # using the id of the property post
        photo = photo_instance.cleaned_data['photo']

        photo_entry = Photo(property=property_entry, photo=photo)
        photo_entry.save()

        return render(request, 'post.html', context={'message': 'Your property is now up'})

@login_required
def edit(request, id):

    # Authorization:
    # Verify if the authenticated user id matches the value
    # of the 'user_id' column of the current post
    id_of_user = request.user.id

    if not Property.objects.filter(pk=id).exists():
        return render(request, 'edit.html', context = {'error': 'Sorry, we could not find this property'})

    user_id_column = Property.objects.get(pk=id).user_id

    if user_id_column != id_of_user:
        return render(request, 'edit.html', context = {'error': 'Sorry, you can not edit this property'})

    # Logic
    if request.method == 'GET':

        property = Property.objects.get(pk=id)

        return render(request, 'edit.html', context={'property': property})

    if request.method == 'POST':

        # If there is a db entry, extract the cleaned data from the form
        property = new_property(request.POST)

        if not property.is_valid():
            return render(request, 'edit.html', context = {'error': 'Sorry'})

        title = property.cleaned_data['title']
        type = property.cleaned_data['type']
        price = property.cleaned_data['price']
        furnish_type = property.cleaned_data['furnish_type']
        contract_type = property.cleaned_data['contract_type']
        no_bedrooms = property.cleaned_data['no_bedrooms']
        no_bathrooms = property.cleaned_data['no_bathrooms']
        features = property.cleaned_data['features']
        description = property.cleaned_data['description']
        address = property.cleaned_data['address']

        # Update the db entry
        # Use try when you do not have any other way if the function was successfully executed
        try:
            Property.objects.filter(pk=id).update(title=title, type=type,
                    price=price, furnish_type=furnish_type, contract_type=contract_type,
                    no_bedrooms=no_bedrooms, no_bathrooms=no_bathrooms,
                    features=features, description=description, address=address)
        except:
            return render(request, 'edit.html', context = {'error': 'Sorry, something went wrong. Try again.'})

        # Return success message
        return render(request, 'edit.html', context = {'success': 'We have updated your property :)'})

@login_required
def delete(request, id):
    # Verify if the user is authorised to delete the post
    # (meaning that the post has been posted by him)
    auth_id = request.user.id

    property = Property.objects.filter(pk=id, user_id = auth_id).exists()

    if not property:
        return render(request, 'property.html', context={'error': 'Oops, something went wrong :('})

    # If it does, display a warning message

    # Delete the post from the db
    instance = Property.objects.filter(pk=id, user_id = auth_id)
    instance.delete()

    # Return user to dashboard with success message
    return render(request, 'property.html', context={'success': 'You have deleted this property'})

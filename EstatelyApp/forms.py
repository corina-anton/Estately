from django import forms
from .models import User, Photo
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxValueValidator

class new_property(forms.Form):

    CONTRACT_TYPE_CHOICES = [
        ('rent', 'To rent'),
        ('buy', 'To buy')
    ]

    PROP_TYPE_CHOICES = [
        ('house', 'house'),
        ('flat / apartment', 'flat / apartment'),
        ('bungalow', 'bungalow'),
        ('land', 'land'),
        ('commercial property', 'commercial property'),
        ('other', 'other')
    ]

    FURNISH_TYPE_CHOICES = [
        ('F', 'furnished'),
        ('UF', 'unfurnished'),
        ('PF', 'partially furnished')
    ]

    NO_BEDROOMS_CHOICES = [
        ('0', 'studio'),
        ('1', '1 bedroom'),
        ('2', '2 bedrooms'),
        ('3', '3 bedrooms'),
        ('4', '4 bedrooms'),
        ('5', '5 bedrooms')
    ]

    title = forms.CharField(max_length=150)
    type = forms.TypedChoiceField(choices=PROP_TYPE_CHOICES)
    price = forms.IntegerField()
    furnish_type = forms.TypedChoiceField(choices=FURNISH_TYPE_CHOICES)
    contract_type = forms.TypedChoiceField(choices=CONTRACT_TYPE_CHOICES)
    no_bedrooms = forms.TypedChoiceField(choices=NO_BEDROOMS_CHOICES)
    no_bathrooms = forms.IntegerField(validators=[MaxValueValidator(15)])
    features = forms.CharField(widget=forms.Textarea)
    description = forms.CharField(widget=forms.Textarea)
    address = forms.CharField(max_length=150)


class search_filters(forms.Form):

    CONTRACT_TYPE_CHOICES = [
        ('rent', 'To rent'),
        ('buy', 'To buy')
    ]

    PROP_TYPE_CHOICES = [
        ('house', 'house'),
        ('flat / apartment', 'flat / apartment'),
        ('bungalow', 'bungalow'),
        ('land', 'land'),
        ('commercial property', 'commercial property'),
        ('other', 'other')
    ]

    FURNISH_TYPE_CHOICES = [
        ('F', 'furnished'),
        ('UF', 'unfurnished'),
        ('PF', 'partially furnished')
    ]

    NO_BEDROOMS_CHOICES = [
        ('0', 'studio'),
        ('1', '1 bedroom'),
        ('2', '2 bedrooms'),
        ('3', '3 bedrooms'),
        ('4', '4 bedrooms'),
        ('5', '5 bedrooms')
    ]

    search_input = forms.CharField(max_length=100, required=False)
    type = forms.TypedChoiceField(choices=PROP_TYPE_CHOICES, required=False)
    furnish_type = forms.TypedChoiceField(choices=FURNISH_TYPE_CHOICES, required=False)
    no_bedrooms = forms.TypedChoiceField(choices=NO_BEDROOMS_CHOICES, required=False)

class signup_form(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    postcode = forms.CharField(max_length=15, required=False)
    email = forms.EmailField(max_length=40, required=True)
    password = forms.CharField(required=True, validators=[MinLengthValidator(5)])
    confirm_password = forms.CharField(required=True, validators=[MinLengthValidator(5)])

    # Write your CUSTOM form validation here
    # Verify if the email already exists in the database:
    def clean_email(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if User.objects.all().filter(email=email).exists():
            raise ValidationError("There already is an account that uses this email address")
        else:
            return email

    # Check if passwords match:
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Passwords do not match")
        else:
            return cleaned_data

class update_form(forms.Form):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    postcode = forms.CharField(max_length=15, required=False)

class update_login_form(forms.Form):

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user')
         super(update_login_form, self).__init__(*args, **kwargs)

    current_password = forms.CharField(required=True, validators=[MinLengthValidator(5)])
    new_password = forms.CharField(required=True, validators=[MinLengthValidator(5)])
    confirm_password = forms.CharField(required=True, validators=[MinLengthValidator(5)])

    def clean_current_password(self):
        # Ectract user id and check whether the authenticated user has logged in
        # using this password

        cleaned_data = super().clean()
        current_password = self.cleaned_data.get('current_password')

        if not self.user.check_password(current_password):
            raise ValidationError('Current password is invalid')
        else:
            return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise ValidationError('Passwords do not match')
        else:
            return cleaned_data

class signin_form(forms.Form):
    email = forms.EmailField(max_length=40, required=True)
    password = forms.CharField(required=True)

class photo_form(forms.ModelForm):

     class Meta:
        model = Photo
        fields = ('photo',)

from django.forms import DateField
from django.forms.widgets import SelectDateWidget


from django import forms
from django.contrib.auth.forms import  AuthenticationForm

from django.contrib.auth.models import User

from .models import CustomUser, Preference, Profile


class CustomUserForm(forms.ModelForm):
    
    # username 		= forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email 			= forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}))
    name 			= forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of Bride / Groom'}))
    phone 			= forms.CharField(label='Phone', widget=forms.TextInput(attrs={'class': 'form-control'}))

    city 			= forms.CharField(label='City', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your city'}))
    address 		= forms.CharField(label='Address', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact address'}))
    date_of_birth 	= forms.DateField(widget=SelectDateWidget(years=range(1950, 2010), attrs={'class': 'form-control'}))
    caste           = forms.CharField(label='Caste', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your caste'}))
    age 			= forms.IntegerField(label='Age', widget=forms.NumberInput(attrs={'class': 'form-control'}))


    about_myself	= forms.CharField(label='About Myself', widget=forms.Textarea(attrs={'class': 'form-control'}))
    # photo 			= forms.ImageField(label='Photo', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    password1 		= forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}),)
    password2 		= forms.CharField(label='Password confirmation',strip=False,widget=forms.PasswordInput(attrs={'class': 'form-control'}),)
  

    class Meta:
        
        photo = forms.ImageField()
        model = CustomUser
        fields = ['email', 'name','gender', 'height', 'motherTongue', 'date_of_birth', 'religion', 'caste','maritalStatus', 'country', 'state', 'city', 'address', 'phone','age', 'weight', 'education','occupation','complexion','phsyicalStatus', 'bloodGroup','eatingHabits','employedIn', 'about_myself']
        
        
        widgets = {
                'gender' : forms.Select(attrs={'class':'form-control'}),
                'motherTongue' : forms.Select(attrs={'class':'form-control'}),
                'religion' : forms.Select(attrs={'class':'form-control'}),
                'maritalStatus' : forms.Select(attrs={'class':'form-control'}),
                'education' : forms.Select(attrs={'class':'form-control'}),
                'occupation' : forms.Select(attrs={'class':'form-control'}),

                'complexion' : forms.Select(attrs={'class':'form-control'}),
                'phsyicalStatus' : forms.Select(attrs={'class':'form-control'}),
                'bloodGroup' : forms.Select(attrs={'class':'form-control'}),
                'eatingHabits' : forms.Select(attrs={'class':'form-control'}),
                'employedIn' : forms.Select(attrs={'class':'form-control'}),
                'country' : forms.Select(attrs={'class':'form-control'}),
                'state' : forms.Select(attrs={'class':'form-control'}),
                'height' : forms.Select(attrs={'class':'form-control'}),
                'weight' : forms.Select(attrs={'class':'form-control'}),
  
        }   

        
        
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
        

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class signinform(AuthenticationForm):
    def confirm_login_allowed(self, user):
        email = forms.EmailField(max_length=254,widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control'}))
        password = forms.CharField(label="Password",strip=False,widget=forms.PasswordInput(attrs={'class': 'form-control'}),)
        pass
    
    

class userprofileform(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ['gender', 'email','phone', 'religion', 'motherTongue', 'country','maritalStatus','height', 'weight', 'city','age','about_myself']



class userprofileeditform(forms.ModelForm):
    
    class Meta:
        photo = forms.ImageField()
        model=CustomUser
        fields=['age','email','phone','motherTongue', 'country','maritalStatus','country','maritalStatus','height','city','age','education','occupation','about_myself','photo']



class PreferenceForm(forms.ModelForm):
    min_height = forms.IntegerField(label='Minimum height', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_height = forms.IntegerField(label='Maximum height', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    min_age = forms.IntegerField(label='Min age', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max_age = forms.IntegerField(label='Max age', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    
    class Meta:
        model = Preference
        fields = ['preferred_gender','preferred_religion','preferred_motherTongue','preferred_maritalstatus','min_height','max_height','min_age','max_age']
        
        
    widget={
        'preferred_gender' : forms.Select(attrs={'class':'form-control'}),
        'preferred_religion' : forms.Select(attrs={'class':'form-control'}),
        'preferred_motherTongue' : forms.Select(attrs={'class':'form-control'}),
        'preferred_maritalstatus' : forms.Select(attrs={'class':'form-control'}),
    }

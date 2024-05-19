from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, View
from .forms import CustomUserForm, PreferenceForm, signinform, userprofileeditform
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, Preference, Profile, MaritalStatus
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from datetime import datetime,timedelta



# PAGINATION
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.contrib.auth import get_user_model

User = get_user_model()


# Create your views here.


class signupview(CreateView):
    
  template_name = "register_page.html"
  form_class	= CustomUserForm
  success_url 	= reverse_lazy('login') # Redirect to login page after successful registration
    
  

  def form_valid(self, form):
      response = super().form_valid(form)

      # Generate profile ID for the user
      user = self.object
      profile_id = generate_profile_id(user)  # Implement your profile ID generation logic
      user.profile.profile_id = profile_id
      user.profile.save()

      # Log in the user
      login(self.request, user)

      return response



  def generate_profile_id(user):
      # Implement your profile ID generation logic here
      # You can use UUID, random strings, or any other method to generate a unique profile ID
      # For example:
      import uuid
      return str(uuid.uuid4())[:10]
  
     






class loginview(LoginView):
    template_name = 'login_page.html'  # Replace 'your_template_name.html' with your actual template name
    form_class = signinform

    def get_success_url(self):
        return reverse_lazy('home')  # Replace 'your_success_url' with your actual success URL name




# PROFILE FILTER VIEW


class profilefilterview(View):
    
    def get(self,request):
      
        if request.method == 'GET':

            age_minn = request.GET.get('age_min')
            age_maxx = request.GET.get('age_max')
            
            if age_minn and age_maxx:
                users = CustomUser.objects.filter(age__gte=age_minn, age__lte=age_maxx)
            else:
                users = CustomUser.objects.all()
        
        cuser=CustomUser.objects.all()
        gen=CustomUser.objects.values_list("gender__gender",flat=True).distinct()
        rel=CustomUser.objects.values_list("religion__religion",flat=True).distinct()
        com=CustomUser.objects.values_list("motherTongue__motherTongue",flat=True).distinct()
              
        
        ages = range(18, 100)
        try:
                user_pref = Preference.objects.get(user=request.user)

        # Get specific fields
                gender = user_pref.preferred_gender
                religion = user_pref.preferred_religion
                motherTongue = user_pref.preferred_motherTongue
                maritalstatus = user_pref.preferred_maritalstatus
                min_height = user_pref.min_height 
                max_height = user_pref.max_height
                age_min = user_pref.min_age
                age_max = user_pref.max_age

                users = CustomUser.objects.all()
                
                if age_min:
                    users = users.filter(age__gte=age_min)
                    
                if age_max:
                    users = users.filter(age__lte=age_max)
                    
                if gender:
                    users = users.filter(gender__gender=gender)
                    
                if religion:
                    users = users.filter(religion__religion=religion)
                    
                if motherTongue:
                    users = users.filter(motherTongue__motherTongue=motherTongue)
                    
                if maritalstatus:
                    users = users.filter(maritalstatus=maritalstatus)

                
                context = {
                    'profiles': users,
                    'users': users,
                    'gen':gen,
                    'rel':rel,
                    'com':com,
                    'ages': ages
                }

                return render(request,"quicksearch.html", context)
            
        except:
            context = {
                    
                    'users': users,
                    'gen':gen,
                    'rel':rel,
                    'com':com,
                    'ages': ages
                }

            return render(request,"quicksearch.html", context)




# PROFILE SHOW / RESULTS AFTER CLICKING SEACH


class filtershow(View):

    def get(self, request):
        
        age_min = request.GET.get('age_min')
        age_max = request.GET.get('age_max')
        gender = request.GET.get('gender')
        religion = request.GET.get('religion')
        motherTongue = request.GET.get('motherTongue')
        
        users = CustomUser.objects.all()
        
        if age_min:
            users = users.filter(age__gte=age_min)
            
        if age_max:
            users = users.filter(age__lte=age_max)
            
        if gender:
            users = users.filter(gender__gender=gender)
            
        if religion:
            users = users.filter(religion__religion=religion)
            
        if motherTongue:
            users = users.filter(motherTongue__motherTongue=motherTongue)

        
        paginator = Paginator(users, 5)  # Show 5 users per page
        

        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            users = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            users = paginator.page(paginator.num_pages)


        ages = range(18, 100)
        gen = CustomUser.objects.values_list('gender', flat=True).distinct()
        rel = CustomUser.objects.values_list('religion', flat=True).distinct()
        com = CustomUser.objects.values_list('motherTongue', flat=True).distinct()
             
        context = {
            'users': users,
            'ages': ages,
            'gen': gen,
            'rel': rel,
            'com': com,
            'paginator_count': paginator.count  # Add paginator count to context
        }
        
        return render(request, 'fres.html', context)




# ADVANCED SEARCH VIEW 


class advanced_search_view(View):
    
    def get(self, request):
      
        if request.method == 'GET':

            # Get query parameters from the request URL
            age_min 			= request.GET.get('age_min')
            age_max 			= request.GET.get('age_max')
            gender 				= request.GET.get('gender')
            religion 			= request.GET.get('religion')
            motherTongue 		= request.GET.get('motherTongue')
            # maritalStatus 		= request.GET.get('maritalStatus')
            education 			= request.GET.get('education')
            occupation 			= request.GET.get('occupation')
            complexion 			= request.GET.get('complexion')
            salary 				= request.GET.get('salary')
            country 			= request.GET.get('country')
            state 				= request.GET.get('State')
            city 				= request.GET.get('city')

            # Filter users based on query parameters
            users = CustomUser.objects.all()

            if age_min:
                users = users.filter(age__gte=age_min)

            if age_max:
                users = users.filter(age__lte=age_max)

            if gender:
                users = users.filter(gender__gender=gender)

            if religion:
            	users = users.filter(religion__religion=religion)

            if motherTongue:
            	users = users.filter(motherTongue__motherTongue=motherTongue)	
                
            # if maritalStatus:
            #     users = users.filter(maritalStatus=maritalStatus)

            if education:
                users = users.filter(education__education=education)

            if occupation:
                users = users.filter(occupation__occupation=occupation)

            if complexion:
                users = users.filter(complexion__complexion=complexion)

            if salary:
                users = users.filter(salary=salary)
            
            if country:
                users = users.filter(country__country=country)
            
            if state:
                users = users.filter(state=state)
            
            if city:
                users = users.filter(city__city=city)

            # Fetch additional data for dropdown menus
            gen 				= CustomUser.objects.values_list("gender__gender", flat=True).distinct()
            rel 				= CustomUser.objects.values_list("religion__religion", flat=True).distinct()
            com 				= CustomUser.objects.values_list("motherTongue__motherTongue", flat=True).distinct()
            # marital_statuses 	= MaritalStatus.objects.all()          
            # marital_statuses 	= CustomUser.objects.values_list("maritalStatus", flat=True).distinct()
            educations 			= CustomUser.objects.values_list("education__education", flat=True).distinct()
            occupations 		= CustomUser.objects.values_list("occupation__occupation", flat=True).distinct()
            complexions 		= CustomUser.objects.values_list("complexion__complexion", flat=True).distinct()
            salaries 			= CustomUser.objects.values_list("salary__salary", flat=True).distinct()
            countries 			= CustomUser.objects.values_list("country__country", flat=True).distinct()
            states 				= CustomUser.objects.values_list("state__state", flat=True).distinct()
            cities 				= CustomUser.objects.values_list("city", flat=True).distinct()

            # Generate age range
            ages = range(18, 100)

            context = {
                'users': users,
                'gen': gen,
                'rel':rel,
                'com':com,
                # 'marital_statuses': marital_statuses,
                'educations': educations,
                'occupations': occupations,
                'complexions': complexions,
                'salaries':salaries,
                'countries': countries,
                'states': states,
                'cities': cities,
                'ages': ages
            }

            return render(request, "advanced_search.html", context)


# ADVANCED SEARCH SHOW VIEW 


class ShowAdvancedSearchResults(View):

    def get(self, request):
        age_min 		= request.GET.get('age_min')
        age_max 		= request.GET.get('age_max')
        gender 			= request.GET.get('gender')
        religion 		= request.GET.get('religion')
        motherTongue 	= request.GET.get('motherTongue')
        # maritalStatus 	= request.GET.get('maritalStatus')
        education 		= request.GET.get('education')
        occupation 		= request.GET.get('occupation')
        complexion 		= request.GET.get('complexion')
        salary 			= request.GET.get('salary')
        country 		= request.GET.get('country')
        state 			= request.GET.get('State')
        city 			= request.GET.get('city')

        # Filter users based on query parameters
        users = CustomUser.objects.all()

        if age_min:
            users = users.filter(age__gte=age_min)

        if age_max:
            users = users.filter(age__lte=age_max)

        if gender:
            users = users.filter(gender__gender=gender)

        if religion:
            users = users.filter(religion__religion=religion)

        if motherTongue:
            users = users.filter(motherTongue__motherTongue=motherTongue)

        # if maritalStatus:
        #     users = users.filter(maritalStatus=maritalStatus)

        if education:
            users = users.filter(education__education=education)

        if occupation:
            users = users.filter(occupation__occupation=occupation)

        if complexion:
            users = users.filter(complexion__complexion=complexion)

        if salary:
            users = users.filter(salary=salary)

        if country:
            users = users.filter(country__country=country)

        if state:
            users = users.filter(state=state)

        if city:
            users = users.filter(city__city=city)


        paginator = Paginator(users, 5)  # Show 5 users per page
        

        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            users = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            users = paginator.page(paginator.num_pages)
                

        # Generate age range
        ages = range(18, 100)

        # Fetch additional data for dropdown menus
        gen 				= CustomUser.objects.values_list("gender__gender", flat=True).distinct()
        rel 				= CustomUser.objects.values_list("religion__religion", flat=True).distinct()
        com 				= CustomUser.objects.values_list("motherTongue__motherTongue", flat=True).distinct()
        # marital_statuses 	= MaritalStatus.objects.all()

        educations 			= CustomUser.objects.values_list("education__education", flat=True).distinct()
        occupations 		= CustomUser.objects.values_list("occupation__occupation", flat=True).distinct()
        complexions 		= CustomUser.objects.values_list("complexion__complexion", flat=True).distinct()
        salaries 			= CustomUser.objects.values_list("salary__salary", flat=True).distinct()
        countries 			= CustomUser.objects.values_list("country__country", flat=True).distinct()
        states 				= CustomUser.objects.values_list("state__state", flat=True).distinct()
        cities 				= CustomUser.objects.values_list("city", flat=True).distinct()


        context = {
            'users': users,
            'gen': gen,
            'rel': rel,
            'com': com,
            # 'marital_statuses': marital_statuses,
            'educations': educations,
            'occupations': occupations,
            'complexions': complexions,
            'salaries': salaries,
            'countries': countries,
            'states': states,
            'cities': cities,
            'ages': ages,
            'paginator_count': paginator.count  # Add paginator count to context
        }

        return render(request, "advancedfres.html", context)






# id search view


def idsearch(request):
    if 'profile_id' in request.GET:
        profile_id = request.GET['profile_id']
        profiles = Profile.objects.filter(profile_id=profile_id)
        
        if profiles.count() == 1:
            # If only one profile found, redirect to its detail page
            return redirect('idsearchshow', profile_id=profile_id)
    
    return render(request, 'idsearch.html')



# id search show view


def idsearchshow(request, profile_id):
    profile = get_object_or_404(Profile, profile_id=profile_id)
    return render(request, 'show_view.html', {'profile': profile})




def userprofileview(request):

  if not request.user.is_authenticated:
    return redirect('login')

  context = {
    'user': request.user
  }

  return render(request, 'profile.html', context)




def profiledetails(request, id):
  user = CustomUser.objects.get(id=id)
  context = {'user': user}
  return render(request, 'user_details.html', context)        





class profileeditview(View):
    
   def get(self,request):
       
       updateform=userprofileeditform()
       return render(request,'useredit.html',{'update':updateform})
   
   def post(self,request):

        user=request.user
  
        updateform=userprofileeditform(request.POST,request.FILES,instance=user)

        if updateform.is_valid():
      
          form_data = updateform.cleaned_data

          photo = form_data['photo']

          user = updateform.save(commit=False)
          user.photo = photo 
          user.save()

          return redirect('myprofile')

        else:
          messages.error(request,'invalid credentials')
          return redirect('useredit')








class preferenceview(View):
    
    def get(self,request):
        
        form=PreferenceForm()
        
        return render(request,'preference.html',{'form':form})
    
    
    def post(self,request):
      preference = Preference.objects.filter(user=request.user).first()
    
      if not preference:
        preference = Preference(user=request.user)
  
      form = PreferenceForm(request.POST, instance=preference)
  
      if form.is_valid():
        preference = form.save(commit=False)  
        preference.user = request.user
        preference.save()
        return redirect('quicksearch')

      else:
        messages.error(request,'invalid input')
        return redirect('preference')




def preferenceshowview(request):

    if request.method=='GET':
        
        user_pref = Preference.objects.get(user=request.user)

        # Get specific fields
        gender = user_pref.preferred_gender
        religion = user_pref.preferred_religion
        motherTongue = user_pref.preferred_motherTongue
        maritalstatus = user_pref.preferred_maritalstatus
        min_height = user_pref.min_height 
        max_height = user_pref.max_height
        age_min = user_pref.min_age
        age_max = user_pref.max_age

        users = CustomUser.objects.all()
        
        if age_min:
            users = users.filter(age__gte=age_min)
            
        if age_max:
            users = users.filter(age__lte=age_max)
            
        if gender:
            users = users.filter(gender__gender=gender)
            
        if religion:
            users = users.filter(religion__religion=religion)
            
        if motherTongue:
            users = users.filter(motherTongue__motherTongue=motherTongue)
            
        if maritalstatus:
            users = users.filter(maritalstatus=maritalstatus)
        
        ages = range(18, 100)
        gen = CustomUser.objects.values_list('gender', flat=True).distinct()
        rel = CustomUser.objects.values_list('religion', flat=True).distinct()
        com = CustomUser.objects.values_list('motherTongue', flat=True).distinct()
        
        context = {'profiles': users}
        
        return render(request, 'quicksearch.html', context)




class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('login')
















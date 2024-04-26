from django.shortcuts import render
from django.views import View

# Create your views here.


from user.models import CustomUser


from django.contrib.auth import get_user_model


User = get_user_model()


class HomeView(View):
    
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
                    'ages': ages,

                }

                return render(request,"home_page.html", context)
            
        except:
            context = {
                    
                    'users': users,
                    'gen':gen,
                    'rel':rel,
                    'com':com,
                    'ages': ages
                }

            return render(request,"home_page.html", context)



def membership_page(request):
	return render(request, 'membership.html')	

def payment_page(request):
	return render(request, 'payment_page.html')

def about_page(request):
    return render(request,"about_page.html")

def contact_page(request):
    return render(request,"contact_page.html")

def terms_page(request):
    return render(request,"terms_page.html")

def privacy_page(request):
    return render(request,"privacy_page.html")
















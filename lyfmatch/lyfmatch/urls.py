"""
URL configuration for lyfmatch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static


from django.contrib import admin
from django.urls import path, include


from . views import (
                    HomeView, contact_page, about_page,  membership_page, payment_page, 
                    terms_page, privacy_page
                    ) #, home_page

from user.views import (
                        userprofileview, profileeditview, profilefilterview, 
                        preferenceview, preferenceshowview, filtershow, 
                        profiledetails, signupview, loginview, 
                        advanced_search_view, ShowAdvancedSearchResults,
                        Logout,
                        idsearch, idsearchshow
                        )


urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # USERS PERSONAL PROFILE WHEN HE LOG'S IN

    path('myprofile/',userprofileview,name='myprofile'),
    path('editprofile',profileeditview.as_view(),name='useredit'),


    # USER'S PARTNER PREFERENCE

    path('preferedprofile',preferenceview.as_view(),name="preference"),
    path('prefrenceresult',preferenceshowview,name='prefrenceresult'),
    

    # USERS SEARCH PROFILE WHEN SOMEONE SEARCHED THEM

    path('users/<int:id>/', profiledetails, name='user-detail'),


    # TYPES OF SEARCHES WITH FILTERS

    path('quicksearch', profilefilterview.as_view(),name='quicksearch'),
    path('idsearch', idsearch,name='idsearch'),
    path('advancesearch', advanced_search_view.as_view(),name='advancesearch'),

    # path('advanced', advanced_search_view.as_view(), name='advanced'),


    # SHOW PROFILE ON QUICK SEARCH

    path('filterresult',filtershow.as_view(),name='fushow'),


    # SHOW PROFILE ON ADVANCE SEARCH
    
    path('advancedfres',ShowAdvancedSearchResults.as_view(),name='advancedfres'),


    # SHOW PROFILE ON ID SEARCH

    path('profile/<str:profile_id>/', idsearchshow, name='idsearchshow'),


    # GENERIC REQUIRED PAGES

    path('membership/', membership_page, name='membership'),
    path('payment/', payment_page, name='payment'),
    path('contact/', contact_page, name='contact'),
    path('about/', about_page, name='about'),
    path('terms/', terms_page, name='terms'),
    path('privacy/', privacy_page, name='privacy'),    

 
    # AUNTHETICATION PAGES

    path('login/', loginview.as_view(),name='login'),
    path('logout',Logout.as_view(),name='logout'),
    path('register/', signupview.as_view(),name="register"),
    path('admin/', admin.site.urls),    
    
]


if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
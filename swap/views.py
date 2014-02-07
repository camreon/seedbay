from django.template import Context, loader, RequestContext, Template
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,render_to_response
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import login as default_login_view
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from models import SeedType, Item
from forms import RegisterForm, ItemForm, SeedTypeForm, SearchForm

class Database:
    """ Singleton object that is used in querying the database """
    instance = None

    def get_rows(self, table):
        """ Uses Django ORM to return the objects (rows) associated with the
            table in the database."""
        return table.objects

    def __new__(cls, *args, **kwargs):
        """ Instead of instantiating a new Database object during
            initialization, instead check if there is one that already
            exists and, if so, use that one instead.
            
            This is like Singleton.getInstance() in Java"""
        if cls.instance is None:
            cls.instance = super(Database, cls).__new__(cls, *args, **kwargs)

        return cls.instance


def home(request):
    retDict={}
    db = Database()
    retDict['manifest'] = db.get_rows(User).all() 
    return render_to_response("home.html", retDict,
                              context_instance=RequestContext(request))
def search(request):
    if request.method == 'POST': # If the form has been submitted

        form = SearchForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            name = form.cleaned_data['name']
            sci_name = form.cleaned_data['sci_name']
            region = form.cleaned_data['region']
            
            return HttpResponseRedirect('/search/results/%s&%s&%s' % (name,sci_name,region)) # Redirect after POST
    else:
        form = SearchForm() # An unbound form

    return render(request, 'search.html', {
        'form': form,
    })

def searchResults(request, query): #handles searches
    retDict = {}

    name, sci_name, region = query.split('&')
    
    #gets users with seeds that match query
    db = Database()
    users = db.get_rows(User).filter(
        Q(userprofile__inventory__item__kind__name__icontains=name) |
        Q(userprofile__inventory__item__kind__sci_name__icontains=sci_name) |
        Q(userprofile__inventory__item__kind__region__icontains=region))

    items = [db.get_rows(Item).filter(inventory__user_profile__user=user) for user in users]
    results = [(user,item) for user,item in zip(users,items)]    
    retDict['results'] = results
    retDict['name'] = name
    retDict['sci_name'] = sci_name
    retDict['region'] = region

    
    return render_to_response("search_results.html", retDict,
                              context_instance=RequestContext(request))
    

def guide(request):
    retDict={}
    return render_to_response("guide.html", retDict,
                              context_instance=RequestContext(request))

def about(request):
    retDict={}
    return render_to_response("about.html", retDict,
                              context_instance=RequestContext(request))

@login_required
def profile(request):
    retDict={}
    retDict['profile'] = request.user.get_profile()
    return render_to_response("profile.html", retDict,
                              context_instance=RequestContext(request))
    
def login(request):
    if request.user.is_authenticated():
        return profile(request)

    return default_login_view(request, loader.get_template("login.html"))

def logout(request): #basic logout functionality
    return logout_then_login(request)

def register(request):
    if request.method == 'POST': # If the form has been submitted
        
        submit = request.POST.get('cancel', None)
        
        if submit: #if cancel button was clicked
            return HttpResponseRedirect('/')
        
        else:
            form = RegisterForm(request.POST) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                # Process the data in form.cleaned_data
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                email = form.cleaned_data['email']
                
                fullname = form.cleaned_data['fullname']
                address = form.cleaned_data['address']
                region = form.cleaned_data['region']
                interests = form.cleaned_data['interests']
                
                db = Database()
                db.get_rows(User).create_user(username, email, password)

                user = authenticate(username=username, password=password)
                user_profile = user.get_profile()
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                
                user_profile.fullname = fullname
                user_profile.address = address
                user_profile.region = region
                user_profile.interests = interests
                user_profile.save()
                
                return HttpResponseRedirect('/my/profile') # Redirect after POST
    else:
        form = RegisterForm() # An unbound form

    return render(request, 'register.html', {
        'form': form,
    })

def add_item(request):
    if request.method == 'POST': # If the form has been submitted
        
        submit = request.POST.get('cancel', None)
        item = Item(inventory = request.user.get_profile().inventory)
        
        if submit: #if cancel button was clicked
            return HttpResponseRedirect('/my/profile')
        
        else:
            form = ItemForm(request.POST, instance=item) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                form.save()               
                return HttpResponseRedirect('/my/profile') # Redirect after POST
    else:
        form = ItemForm() # An unbound form

    return render(request, 'add_item.html', {
        'form': form,
    })

def add_seedtype(request):
    if request.method == 'POST': # If the form has been submitted
        
        submit = request.POST.get('cancel', None)
        seed = SeedType(verified = False)
        
        if submit: #if cancel button was clicked
            return HttpResponseRedirect('/my/profile')
        
        else:
            form = SeedTypeForm(request.POST, instance=seed) # A form bound to the POST data
            if form.is_valid(): # All validation rules pass
                form.save()               
                return HttpResponseRedirect('/my/profile') # Redirect after POST
    else:
        form = SeedTypeForm() # An unbound form

    return render(request, 'add_seedtype.html', {
        'form': form,
    })
   
def userSeeds(request, requested_user_id):
    retDict = {}
    db = Database()
    listed_user = db.get_rows(User).get(id=requested_user_id)
    retDict['listing_user'] = listed_user
    retDict['has_seeds'] = False
    retDict['seeds'] = []
    
    
    retDict['seeds'] = listed_user.get_profile().inventory.item_set.all()
    retDict['has_seeds'] = bool(retDict['seeds'])
    
    return render_to_response("user_seeds.html", retDict,
                              context_instance=RequestContext(request))

def seedInfo(request, requested_seed_id):
    retDict = {}

    db = Database()
    retDict['seed_type'] = db.get_rows(SeedType).get(id=requested_seed_id)

    return render_to_response("seed_info.html", retDict,
                              context_instance=RequestContext(request))

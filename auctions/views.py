from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib import messages
from django.contrib.messages import get_messages
from django.forms import ModelForm


from .models import *

class NewListing(ModelForm):
    class Meta:
        model = Listing
        fields = ['title','description','starting_bid','image_url', 'category']

class NewBid(ModelForm):
    class Meta:
        model = Bid
        fields = ['value']

class NewComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ToWatchlist(forms.Form):
    listing = forms.IntegerField()
    value = forms.CharField(max_length=6)

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(opened=True)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='login')
def create(request):
    # If user tried to access by a get request
    if request.method =="GET":
        categories = Category.objects.all()
        return render(request,"auctions/create.html", {
            "categories": categories
        })
    
    # If user tried to access by a post request
    else:
        if request.POST['category'] == "none":
            form = NewListing({
                'title': request.POST['title'],
                'description': request.POST['description'],
                'image_url': request.POST['image_url'],
                'starting_bid': request.POST['starting_bid'],
            })
        
        else:
            form = NewListing(request.POST)

        if form.is_valid():
            # Being valid, get a data dict with each input value
            data = form.cleaned_data

            # Create and save listing instance with data parameters
            instance = form.save(commit=False)
            instance.announcer = request.user
            instance.save()

            messages.success(request, 'Listing posted!')

            return HttpResponseRedirect(reverse("index"))

        # If not valid
        else:
            messages.error(request, 'Not valid ')
            return render(request,"auctions/create.html")

@login_required(login_url='login')
def listing(request, listing_id):
    
    listing = Listing.objects.get(pk=listing_id)    

    # If user accessed through get request
    if request.method == "GET":
        watchlist = Watchlist.objects.filter(
            owner=request.user, item=listing)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlist": watchlist.first()
        } )

    else:
        if listing.opened:
            listing.opened = False
        else:
            listing.opened = True
            listing.bids.all().delete()
            listing.comments.all().delete()
        listing.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def bid(request, listing_id):
    if request.method == "POST":
        
        form = NewBid(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            last = Listing.objects.get(pk=listing_id).bids.all().last()

            if last:
                last = last.value
            else:
                last = Listing.objects.get(pk=listing_id).starting_bid
            
            if data["value"] > last:
                instance = form.save(commit=False)
                instance.bidder = request.user
                instance.listing = Listing.objects.get(pk=listing_id)
                instance.save()

                messages.success(request, 'Bid made!')
            
            else:
                messages.error(request, 'Invalid bid value.')

        else:
            messages.error(request, 'Invalid input.')

    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

@login_required(login_url='login')
def comment(request, listing_id):
    if request.method == "POST":
        form = NewComment(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.listing = Listing.objects.get(pk=listing_id)
            instance.save()

            messages.success(request, 'Comment posted!')

        else:
            messages.error(request, 'Invalid input')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def watchlist(request):
    if request.method == "GET":
        items = Watchlist.objects.filter(owner=request.user)
        return render(request, "auctions/watchlist.html", {
            "items": items
        })
    
    else:
        form = ToWatchlist(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            item = Listing.objects.get(pk=data["listing"])
            owner = request.user

            if data["value"] == "add":
                w = Watchlist(owner=owner, item=item)
                w.save()
                messages.success(request, "Added to watchlist!")
            
            elif data["value"] == "remove":
                Watchlist.objects.filter(owner=owner, item=item).delete()
                messages.success(request, "Removed from watchlist!")

            else:
                messages.error(request, "Invalid operation")

        else:
            messages.error(request, "Invalid data")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='login')
def categories(request):
    categories = Category.objects.all()

    if request.method == "GET":
        return render(request, "auctions/categories.html", {
            'categories': categories
        })

@login_required(login_url='login')
def category(request, category):
    listings = Listing.objects.filter(
        category=Category.objects.get(name=category))

    if request.method == "GET":
        return render(request, "auctions/category.html", {
            'category': category,
            'listings': listings
        })
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Listing, Category, Comment, Bid

from .models import User


def index(request):
    all_product = Listing.objects.filter(isActive=True)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "content_placeholder": all_product,
        "category_placeholder": all_categories
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


def createListing(request):
    if request.method == 'GET':
        all_categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "category_placeholder": all_categories
        })
    else:
        #get the data from the form
        new_title = request.POST["title_data"]
        new_desciption = request.POST["description_data"]
        new_image = request.POST["image_data"]
        new_price = request.POST["price_data"]
        new_category = request.POST["category_data"]

        #who is the user
        current_user = request.user

        #get all info about the particular category
        category_data = Category.objects.get(category_name=new_category)

        #Create a bid object
        bid_price = Bid(
            bid = float(new_price),
            user = current_user
        )

        bid_price.save()

        #create a new listing
        new_listing = Listing(
            title = new_title,
            description = new_desciption,
            imageURL = new_image,
            price = bid_price,
            owner = current_user,
            category = category_data
        )

        #insert the object in our database
        new_listing.save()

        #redirect the index page
        return HttpResponseRedirect(reverse(index))
    

def display_category(request):
    if request.method == 'POST':
        category_from_form = request.POST["category_data"]
        current_category = Category.objects.get(category_name=category_from_form)
        current_listing = Listing.objects.filter(isActive=True, category=current_category)
        all_categories = Category.objects.all()
        return render(request, "auctions/special_category.html", {
        "content_placeholder": current_listing,
        "category_placeholder":all_categories
    })



def listing_function(request, id):
    listing_data = Listing.objects.get(pk = id)
    is_listing_in_watchlistlist = request.user in listing_data.watchlist.all()
    all_comments = Comment.objects.filter(listing=listing_data)
    is_owner = request.user.username == listing_data.owner.username
    new_bid_no = listing_data.bid_no
    return render(request, "auctions/listing.html", {
        "listing_content_placeholder": listing_data,
        "is_listing_in_watchlistlist_placeholder": is_listing_in_watchlistlist,
        "all_comments_placeholder": all_comments,
        "is_owner_placeholder": is_owner,
        "update_placeholder": "kuch_bhi_nhi",
        "bid_no_placeholder": new_bid_no
    })


def Watchlist(request):
    current_user = request.user
    listing = current_user.listing_watchlist_related_name.all()
    return render(request, "auctions/watchlist.html", {
        "content_placeholder": listing
    })


def Remove(request, id):
    listing_data = Listing.objects.get(pk = id)
    current_user = request.user
    listing_data.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def Add(request, id):
    listing_data = Listing.objects.get(pk = id)
    current_user = request.user
    listing_data.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def add_comment(request, id):
    current_user = request.user
    listing_data = Listing.objects.get(pk=id)
    new_message = request.POST["new_comment_data"]

    new_comment = Comment(
        author = current_user,
        listing = listing_data,
        message = new_message
    )

    new_comment.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))


def placing_bid(request,id):
    # retriving data from blace bid page
    new_bid = request.POST["bidding_data"]
    listing_data = Listing.objects.get(pk=id)
    if float(new_bid) > listing_data.price.bid:
        updated_bid = Bid(
            user = request.user,
            bid = float(new_bid)
        )
        updated_bid.save()
        listing_data.price = updated_bid
        listing_data.bid_no = listing_data.bid_no + 1
        listing_data.save()
        #retrieving the new bid number from models
        new_bid_no = listing_data.bid_no
        return render(request,"auctions/listing.html", {
            "listing_content_placeholder": listing_data,
            "message_placeholder": "Bid is updated Successfully",
            "update_placeholder": "True",
            "bid_no_placeholder": new_bid_no
        })
    else:
        return render(request,"auctions/listing.html", {
            "listing_content_placeholder": listing_data,
            "message_placeholder": "Bidding Failed",
            "update_placeholder": "False"
        })
    

def ending_bid(request,id):
    listing_data = Listing.objects.get(pk=id)
    listing_data.isActive = False
    listing_data.winner = listing_data.price.user
    listing_data.save()
    # other parameters for sending
    is_owner = request.user.username == listing_data.owner.username
    return render(request,"auctions/listing.html", {
        "listing_content_placeholder": listing_data,
        "message_placeholder": "Congratulations! Your auction is closed",
        "update_placeholder": "True",
        "is_owner_placeholder": is_owner
    }) 

def won_bid(request):
    current_user = request.user
    my_won_product = Listing.objects.filter(winner=current_user)
    return render(request, "auctions/won_product.html", {
        "content_placeholder": my_won_product ,
    })
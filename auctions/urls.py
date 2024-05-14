from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="create_kr"),
    path("display_category", views.display_category, name="display_specific_category"),
    path('listing/<int:id>', views.listing_function, name="listing"),
    path("watchlist", views.Watchlist, name="watchlist"),
    path("remove/<int:id>", views.Remove, name="remove"),
    path("add/<int:id>", views.Add, name="add"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("bid_placing/<int:id>", views.placing_bid, name="bid_daal"),
    path("bid_end/<int:id>", views.ending_bid, name="bid_khatam"),
    path("my_won_bid", views.won_bid, name="buyed_product"),
]

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone



class User(AbstractUser):
    

    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=50)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(max_length=2000, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL , related_name="products", null=True, blank=True)
    announcer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="announcements")
    date = models.DateTimeField(default=timezone.now)
    opened = models.BooleanField(default=True)

    def __str__(self):
        return f"Listing {self.id} by user {self.announcer}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    value = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Bid {self.id} by user {self.bidder} on {self.listing}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment {self.id} by user {self.author} on {self.listing}"

class Watchlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchings")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchers")

    def __str__(self):
        return f"{self.owner.username} watches {self.item.title}"


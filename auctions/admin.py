from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "announcer")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("listing", "content", "author", "date")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

class BidAdmin(admin.ModelAdmin):
    list_display = ("listing", "value", "bidder")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing,ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist)
admin.site.register(Category, CategoryAdmin)
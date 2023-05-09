from django.conf import settings
from store.models import Product
from . models import Wishlist


class Wishlistitem(object):

    def __init__(self, request):
        wishlist = Wishlist.objects.filter(user_id=request.user.id)
        self.wishlist = wishlist

    def __len__(self):
        """
        Count all items in the wishlist.
        """
        return sum(item['quantity'] for item in self.wishlist.values())



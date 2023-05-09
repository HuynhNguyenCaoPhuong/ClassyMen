from decimal import Decimal
from django.conf import settings
from . models import Product


class Wishlist(object):

    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get(settings.WISHLIST_SESSION_ID)
        if not wishlist:
            # save an empty wishlist in the session
            wishlist = self.session[settings.WISHLIST_SESSION_ID] = {}
        self.wishlist = wishlist

    def __iter__(self):
        """
        Iterate over the items in the wishlist and get the products
        from the database.
        """
        product_ids = self.wishlist.keys()
        # get the product objects and add them to the wishlist
        products = Product.objects.filter(id__in=product_ids)

        wishlist = self.wishlist.copy()
        for product in products:
            wishlist[str(product.id)]['product'] = product

        for item in wishlist.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the wishlist.
        """
        return sum(item['quantity'] for item in self.wishlist.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the wishlist or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.wishlist:
            self.wishlist[product_id] = {'quantity': quantity, 'price': str(product.price)}
        else:
            self.wishlist[product_id]['quantity'] += int(quantity)
        self.save()

    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the wishlist.
        """
        product_id = str(product.id)
        if product_id in self.wishlist:
            del self.wishlist[product_id]
            self.save()

    def clear(self):
        # remove wishlist from session
        del self.session[settings.WISHLIST_SESSION_ID]
        self.save()



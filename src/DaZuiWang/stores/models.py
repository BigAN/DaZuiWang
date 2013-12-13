#! -*- coding:utf-8 -*- 
from django.db import models
# Create your models here.
from datetime import date

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import locale

locale.setlocale(locale.LC_ALL, '')


class Store(models.Model):
    name = models.CharField(max_length=255,verbose_name="名称")
    image = models.ImageField(upload_to='store_images')
    ads_image=models.ImageField(upload_to='store_images',verbose_name='宣传照片（尺寸:880×230）')
    description=models.TextField()
    store_quantitiy=models.IntegerField()
    telphone=models.CharField(max_length=255,verbose_name="电话")
    
    lat=models.DecimalField(max_digits=10,decimal_places=6)
    lon=models.DecimalField(max_digits=10,decimal_places=6)
    def __unicode__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='product_images')
    quantity = models.IntegerField()
    store = models.ForeignKey(Store)
    cuisine=models.CharField(max_length=50, choices=[(t,t) for t in ('chinese', 'europe', 'japan', 'franch','italy','tailand')],
                                        null=True)
    def price_string(self):
         print self.price;
         return self.price; 
         return locale.currency(self.price, grouping=True)
    
    def __unicode__(self):
        return self.name

class ProductQuantities(models.Model):
    product = models.ForeignKey('Product')
    order = models.ForeignKey('Order')
    quantity = models.IntegerField()
    def product_price(self):
        print "nihs"
        print "hehe "+str(self.product.price)
        return self.product.price*self.quantity
class Order(models.Model):

    user = models.ForeignKey(User)
    products = models.ManyToManyField(Product, through=ProductQuantities)
    store = models.ForeignKey(Store)

    name_on_card = models.CharField(max_length=255, null=True)
    credit_card_type = models.CharField(max_length=50, 
                                        choices=[(t,t) for t in ('Visa', 'MasterCard', 'American Express', 'Discover')],
                                        null=True)
    credit_card_number = models.CharField(max_length=20, null=True)
    
    security_number = models.CharField(max_length=4, null=True)
    expiration_month = models.IntegerField(choices=[(m, m) for m in xrange(1,13)], null=True)

    _current_year = date.today().year
    expiration_year = models.IntegerField(choices=[(y, y) for y in xrange(_current_year, _current_year + 20)], null=True)
    address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    zip_code = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=10, null=True)

    ordered_on = models.DateTimeField(null=True)
    shipped_on = models.DateTimeField(null=True)
    send_time=models.DateTimeField(null=True)
    pay_way = models.CharField(max_length=50, 
                                        choices=[(t,t) for t in ('pay_offline', 'pay_online')],
                                        null=True)
    notes=models.CharField(max_length=255, null=True)
    status=models.CharField(max_length=50, 
                                        choices=[(t,t) for t in ('ing','accepted', 'finished', 'unfinished')],
                                        null=True)
    def cancel_order(self):
        try:
            self.status="unfinished"
            self.save()
        except Exception, e:
            print e
    def agree_order(self):
        try:
            self.status="accepted"
            self.save()
        except Exception, e:
            print e
    def finish_order(self):
        try:
            self.status="finished"
            self.save()
        except Exception, e:
            print e
    def total_num(self):
        t=0
        for pq in self.productquantities_set.all():
            t+=pq.quantity
        return t
    def total(self):
        t=0
#        print "total"
        for pq in self.productquantities_set.all():
            t+=pq.product.price*pq.quantity
        return t
        #return locale.currency(t, grouping=True)
       

    def add_product(self, product):
        product_quantity = None
        try:
            product_quantity = ProductQuantities.objects.get(order=self, product=product)
            product_quantity.quantity += 1
            product_quantity.save()
        except ProductQuantities.DoesNotExist:
            product_quantity = ProductQuantities.objects.create(order=self, product=product, quantity=1)

    def remove_product(self, product):
        try:
            product_quantity = ProductQuantities.objects.get(order=self, product=product)
            product_quantity.quantity -= 1
            if product_quantity.quantity > 0:
                product_quantity.save()
            else:
                product_quantity.delete()
        except ProductQuantities.DoesNotExist:
            pass

    @classmethod
    def get_cart(cls, store, user):
        cart, created = cls.objects.get_or_create(store=store, user=user, ordered_on__isnull=True)
        return cart

   
    def __unicode__(self):
        return "%s %s - %s" % (self.id, self.user.username, self.ordered_on)

def main():
    print locale.currency(12, grouping=True)
    print "1"
if __name__ == '__main__':
    main()
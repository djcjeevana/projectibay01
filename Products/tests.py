from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from Products.models import *


class TestCategoriesModel(TestCase):

    def setUp(self):
        self.data1 = Category.objects.create(title='django', slug='django')
        self.data2 = SubCategory.objects.create(title='django',slug='django',category_id=1)
        self.data3 = MiniCategory.objects.create(title='django', slug='django',category_id=1,subcategory_id=1)

    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """
        data1 = self.data1
        data2 = self.data2
        data3 = self.data3
        
        self.assertTrue(isinstance(data1, Category))
        self.assertTrue(isinstance(data2, SubCategory))
        self.assertTrue(isinstance(data3, MiniCategory))
        self.assertEqual(str(data1), 'django')
        self.assertEqual(str(data2), 'django')
        self.assertEqual(str(data3), 'django')
        
        
class TestProductsModel(TestCase):
    def setUp(self):
        Category.objects.create(title='django', slug='django')
        SubCategory.objects.create( title='django',slug='django',category_id=1)
        MiniCategory.objects.create(title='django', slug='django',category_id=1,subcategory_id=1)
       
        self.data1 = Product.objects.create(category_id=1,sub_category_id=1,mini_category_id=1, title='django beginners',
                                            slug='django-beginners', new_price='20.00', image='django',image_hover="jnago",amount=23,detail='ladjflkdsjfldslkfj')
        #self.data2 = Product.products.create(category_id=1, title='django advanced', created_by_id=1,
        #                                     slug='django-advanced', price='20.00', image='django', is_active=False)

    def test_products_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')
        
        
        
    def test_products_url(self):
            """
            Test product model slug and URL reverse
            """
            data = self.data1
            url = reverse("Stores:product_single", kwargs=[data.slug])
            self.assertEqual(url, '/django-beginners')
            response = self.client.post(
                reverse("Stores:product_single", kwargs=[data.slug]))
            self.assertEqual(response.status_code, 200)
            

from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
from django.conf import settings

   
class Post(models.Model): # Post model is seems to represent a book model
    title = models.CharField(max_length=255)    
    description = models.TextField()
    book_price = models.DecimalField(decimal_places=2, max_digits=20, default=0.00)
    quantity = models.IntegerField(default=1)        
    category = models.ManyToManyField(Category)
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    image = models.ImageField(upload_to='posts/media/uploads/', blank = True, null = True)    

    def __str__(self):
        return self.title

    


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)



class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=50)    
    email = models.EmailField()
    comment = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f"Review by {self.name}"
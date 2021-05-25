from django.db import models
import re

class Usermanager(models.Manager):
    # this is where we check that the inputs are valid
    def basic_validator(self, postData):
        errors = {}

        if len(postData["first_name"]) <2:
            errors["first_name"] = "Please use your whole name"

        if len(postData["last_name"]) <2:
            errors["Last_name"] = "We like pancakes. Do you like pancakes? And names with more than two letters?"

        if postData["password"] != postData["confirm_password"]:
            errors["password"] = "Your confirmation password does not agree with your original. They are fighting. Please, pick a winner."

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "Invalid email address!"
        
        if User.objects.filter(email = postData['email']):
            errors['email'] = "Email is already registered"
            
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=90)
    upvote_total = models.IntegerField(null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # upvoted_by =models.ForeignKey(User, related_name= "user_upvote", on_delete = models.CASCADE)

    objects = Usermanager()

class Video(models.Model):
    video_id = models.CharField(max_length=20)
    search = models.CharField(max_length=45)
    Dinner = 'D'
    Lunch = 'L'
    Breakfast = 'B'
    Snack = 'S'
    Dessert = 'De'
    meal_CHOICES = [
        (Dinner, 'Dinner'),
        (Lunch, 'Lunch'),
        (Breakfast, 'Breakfast'),
        (Snack, 'Snack'),
        (Dessert, 'Dessert'),
    ]
    meal = models.CharField(
        max_length=2,
        choices=meal_CHOICES,
        default=Dinner,
        null = True,
        blank = True,
    )
    # recipe = models.ArrayField()
    upvoted_total = models.IntegerField(default=0)
    upvoted_by =models.ForeignKey(User, related_name= "video_upvote", null = True, blank = True, on_delete = models.CASCADE)

class Review(models.Model):
    article = models.TextField()
    yummy = models.IntegerField(null = True, blank = True)
    easy = models.IntegerField(null = True, blank = True)
    good = models.IntegerField(null = True, blank = True)
    entertaining = models.IntegerField(null = True, blank = True)
    healthy = models.IntegerField(null = True, blank = True)
    video = models.ForeignKey(Video, related_name="review_of_video", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name= "review_by_user", on_delete = models.CASCADE)



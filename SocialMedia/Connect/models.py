from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class userdatabase(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    whatsapp_number = models.IntegerField(null=True, blank=True)
    image = models.ImageField(null=True,)
    about = models.TextField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    degree = models.CharField(max_length=100, null=True, blank=True)
    website = models.CharField(max_length=30, null=True, blank=True)
    experiance = models.CharField(max_length=100, null=True, blank=True)
    company = models.CharField(max_length=100, null=True, blank=True)
    profile_title = models.CharField(max_length=50, null=True, blank=True)

    fb_link = models.CharField(max_length=30, null=True, blank=True)
    insta_link = models.CharField(max_length=30, null=True, blank=True)
    linked_In_link = models.CharField(max_length=30, null=True, blank=True)


    def __str__(self):
        return f"{self.name}"

class Connections(models.Model):
    ## here we shall use same userdb , once for sender and another for receiver!!
    '''ERRORS:
Connect.Connections.receiver: (fields.E304) Reverse accessor 'userdatabase.connections_set' for 'Connect.Connections.receiver' clashes with reverse accessor for 'Connect.Connections.sender'.
        HINT: Add or change a related_name argument to the definition for 'Connect.Connections.receiver' or 'Connect.Connections.sender'.
Connect.Connections.sender: (fields.E304) Reverse accessor 'userdatabase.connections_set' for 'Connect.Connections.sender' clashes with reverse accessor for 'Connect.Connections.receiver'.
        HINT: Add or change a related_name argument to the definition for 'Connect.Connections.sender' or 'Connect.Connections.receiver'.

System check identified 2 issues (0 silenced).
(ENV) PS E:\SocialMedia\socialmedia> python manage.py makemigrations Connect
SystemCheckError: System check identified some issues:

ERRORS:
Connect.Connections.receiver: (fields.E304) Reverse accessor 'userdatabase.connections_set' for 'Connect.Connections.receiver' clashes with reverse accessor for 'Connect.Connections.sender'.
        HINT: Add or change a related_name argument to the definition for 'Connect.Connections.receiver' or 'Connect.Connections.sender'.
Connect.Connections.sender: (fields.E304) Reverse accessor 'userdatabase.connections_set' for 'Connect.Connections.sender' clashes with reverse accessor for 'Connect.Connections.receiver'.
        HINT: Add or change a related_name argument to the definition for 'Connect.Connections.sender' or 'Connect.Connections.receiver'.
'''
    ## to by-pass--> use related name..like below.
    sender = models.ForeignKey(userdatabase, related_name="sender", on_delete=models.CASCADE,null=True,blank=True)
    receiver = models.ForeignKey(userdatabase,related_name="receiver",on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(max_length=20,null=True,blank=True,default="Sent")
    date = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return f"Sender=>{self.sender} -and- receiver=> {self.receiver}- status -{self.status}"


class Company_Model(models.Model):
    usr = models.ForeignKey(User,on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True,)
    logo = models.ImageField(max_length=20, null=True, blank=True, )
    number = models.IntegerField( null=True, blank=True, )
    email = models.EmailField(max_length=20, null=True, blank=True, )
    website = models.CharField(max_length=20, null=True, blank=True, )
    address = models.CharField(max_length=20, null=True, blank=True, )
    company_title =  models.CharField(max_length=50, null=True, blank=True, )

    map_embad = models.TextField(null=True, blank=True, )


    def __str__(self):
        return f"{self.name}"


class Blogs_Model(models.Model):
    usr = models.ForeignKey(User,on_delete=models.CASCADE, null=True,blank=True)
    blog_title = models.CharField(max_length=200,null=True,blank=True,)
    blog_content = models.TextField(null=True, blank=True, )
    blog_image = models.ImageField(null=True,)
    blog_files =models.FileField(null=True,)
    youtube_videos = models.TextField(null=True, blank=True, )
    date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f"{self.blog_title}"


class BlogLiked(models.Model):
    usr = models.ForeignKey(User,on_delete=models.SET_NULL, null=True,blank=True) ##who is going to like or dislike
    blog = models.ForeignKey(Blogs_Model, on_delete=models.CASCADE, null=True, blank=True)

class BlogDisliked(models.Model):
    usr = models.ForeignKey(User,on_delete=models.SET_NULL, null=True,blank=True) ##who is going to like or dislike
    blog = models.ForeignKey(Blogs_Model, on_delete=models.CASCADE, null=True, blank=True)



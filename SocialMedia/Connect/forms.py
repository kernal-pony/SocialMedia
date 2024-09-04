from django import forms
from .models import *

class AddUser_Form(forms.ModelForm):
    class Meta:
        model = userdatabase
        exclude = ("usr", "dob", "location", "Degree", "website", "experience", "company", "profile_title")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": ""}),
            "email": forms.EmailInput(attrs={"class": "form-control", }),
            "whatsapp_number":forms.NumberInput(attrs={"class": "form-control", }),
            "image": forms.FileInput(attrs={"class": "form-control", "onchange": "loadFile(event)"}),
            "about": forms.Textarea(attrs={"class": "form-control", "rows": "5"}),

        }
### above are during registration time!


class Edit_User_Details(forms.ModelForm):
    class Meta:
        model = userdatabase
        exclude = ("usr",)
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": ""}),

            "email": forms.EmailInput(attrs={"class": "form-control", "required": ""}),
            "whatsapp_number": forms.NumberInput(attrs={"class": "form-control", }),
            "about": forms.Textarea(attrs={"class": "form-control", "rows": "8", "column": "12"}),
            "dob": forms.DateInput(attrs={"class": "form-control", "required": ""}),
            "location": forms.TextInput(attrs={"class": "form-control",}),
            "Degree": forms.TextInput(attrs={"class": "form-control", }),
            "website": forms.TextInput(attrs={"class": "form-control", }),
            "experiance": forms.TextInput(attrs={"class": "form-control", }),
            "company": forms.TextInput(attrs={"class": "form-control", }),
            "profile_title": forms.TextInput(attrs={"class": "form-control", "required": ""}),
            "fb_link": forms.TextInput(attrs={"class": "form-control", }),
            "insta_link": forms.TextInput(attrs={"class": "form-control", }),
            "linked_In_link": forms.TextInput(attrs={"class": "form-control", }),

        }## these are during editing time!



class StartCompany_Form(forms.ModelForm):
    class Meta:
        model = Company_Model
        exclude = ("usr", )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": ""}),
            "logo": forms.FileInput(attrs={"class": "form-control","onchange":"loadFile(event)"}),
            "number": forms.NumberInput(attrs={"class": "form-control", "required": ""}),

            "email": forms.EmailInput(attrs={"class": "form-control", }),
            "website": forms.TextInput(attrs={"class": "form-control", }),
            "address": forms.TextInput(attrs={"class": "form-control", }),
            "company_title": forms.TextInput(attrs={"class": "form-control", "required": ""}),

            "map_embad": forms.Textarea(attrs={"class": "form-control",}),


        }

class UserBlog_Form(forms.ModelForm):
    class Meta:
        model = Blogs_Model
        exclude = ("usr", )
        widgets = {
            "blog_title": forms.TextInput(attrs={"class": "form-control", "required": ""}),
            "blog_content": forms.Textarea(attrs={"class": "form-control", "required": ""}),
            "blog_image": forms.FileInput(attrs={"class": "form-control", }),
            "blog_files": forms.FileInput(attrs={"class": "form-control", }),

            "youtube_videos": forms.Textarea(attrs={"class": "form-control"}),


        }

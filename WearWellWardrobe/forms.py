from django import forms

from django.forms.widgets import ClearableFileInput
from WearWellWardrobe.models import Page, Category, UserProfile
from django.contrib.auth.models import User



class CustomImageInput(ClearableFileInput):
    template_name = "widgets/customImageForm.html"

class PageForm(forms.ModelForm):
#form for adding pages

    title = forms.CharField(max_length=128, label="Page Title", empty_value="Untitled",required=False, widget=forms.TextInput( attrs={'class': "titleStlye"}))
    content1 = forms.CharField(max_length=8000, label="Content 1", empty_value="", required=False, widget=forms.TextInput( attrs={'class': "textStyle"}))
    content2 = forms.CharField(max_length=8000, label="Content 2", empty_value="", required=False, widget=forms.TextInput( attrs={'class': "textStyle"}))
    content3 = forms.CharField(max_length=8000, label="Content 3", empty_value="", required=False, widget=forms.TextInput( attrs={'class': "textStyle"}))
    content4 = forms.CharField(max_length=8000, label="Content 4", empty_value="", required=False, widget=forms.TextInput( attrs={'class': "textStyle"}))
    img1 = forms.ImageField(
        label="Image 1",
        required=False,
        widget=CustomImageInput(attrs={'class': 'imgContent hideMe'})
    ) 
    
    pageNotes = forms.CharField(max_length=4096, label="Notes for the page", empty_value="",required=False,  widget=forms.TextInput(attrs={'class': 'pageNotes'}),)
    displayStyle = forms.IntegerField(
        label="Display Style (Min 1, Max 6)",
        required=True,
        widget=forms.NumberInput(attrs={'class': 'numberField', 'min':1 , 'max': 6}),
        ) 
    category = forms.ModelChoiceField(queryset=Category.objects.all(),  label="Category", empty_label="Select a Category", required=True,)
    
    
    class Meta:
        model = Page
        fields = (
            "title",
            "content1",
            "content2",
            "content3",
            "content4",
            "img1",
            "pageNotes",
            "deletable",
            "category",
            "displayStyle",
                 
        )

class EditCategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, label="Category Title", required=False, widget=forms.TextInput( attrs={'class': "catNameStyle"}))
    
    class Meta:
        model = Category
        fields = ("name",)



class EditPageForm(forms.ModelForm):
# form for editing pages. 

# choices for the display style so the dropdown looks nicer
    STYLE_CHOICES = [(1, "Style 1"),(2, "Style 2"),(3, "Style 3"),(4, "Style 4"),(5, "Style 5"),]

    displayStyle = forms.IntegerField(
        label="Display Style (Min 1, Max 6)",
        required=True,
        widget=forms.NumberInput(attrs={'class': 'numberField', 'min':1 , 'max': 6}),
    )
  
    title = forms.CharField(max_length=128, label="Page Title",    required=False, widget=forms.TextInput( attrs={'class': "titleStlye"}))
            
    content1 = forms.CharField(max_length=8000, label="Content 1", required=False, widget=forms.TextInput( attrs={'class': "textStyle"}))
            
    content2 = forms.CharField(max_length=8000, label="Content 2", required=False, widget=forms.TextInput( attrs={'class': "textStyle"}))
            
    content3 = forms.CharField(max_length=8000, label="Content 3", required=False, widget=forms.TextInput( attrs={'class': "textStyle"}))
            
    content4 = forms.CharField(max_length=8000, label="Content 4", required=False, widget=forms.TextInput( attrs={'class': "textStyle"}))
            
    img1 = forms.ImageField(
        label="Image 1",
        required=False,
        widget=CustomImageInput(attrs={'class': 'hideMe'})
    )
    pageNotes = forms.CharField(max_length=4096, label="Notes for the page", empty_value="",required=False, 
            widget=forms.TextInput(attrs={'class': 'pageNotes'}),)
    

    category = forms.ModelChoiceField(queryset=Category.objects.all(),  label="Category", empty_label="Select a Category", required=True,)
    clear_image = forms.BooleanField(required=False, widget=forms.HiddenInput())

    def clean(self):
        cleaned_data = super().clean()

        # If the user clicked 'Clear', set the image field to None
        if cleaned_data.get('clear_image') == True:
            print("TIME TO CLEAN!!!")
            cleaned_data['img1'] = None  # This clears the image

        return cleaned_data
    
    class Meta:
        model = Page
        fields = (
            "title",
            "displayStyle",
            "content1",
            "content2",
            "content3",
            "content4",
            "img1",
            "pageNotes",
            "category",
        )
        exclude = ("deletable",)


# User login / register stuff here
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = []
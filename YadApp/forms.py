from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Field
from .models import *
from ckeditor_uploader.fields import RichTextUploadingFormField
class UserSignup(forms.ModelForm):
    password=forms.CharField(label='گذرواژه',widget=forms.PasswordInput,required=True)
    repassword=forms.CharField(label='تکرار گذزواژه',widget=forms.PasswordInput,required=True)
    class Meta:
        helper=FormHelper()
        model=User
        fields=('fname','lname','email','photo','password')
        widgets={
            'photo':forms.FileInput(attrs={'class':'custom-file-input' ,'oninput':"pic.src=window.URL.createObjectURL(this.files[0])"})
        }
    def clean(self):
        cleaned_data=super(UserSignup,self).clean()   
        password=cleaned_data.get('password')
        re_password=cleaned_data.get('repassword')
        if password != re_password:
            forms.ValidationError('گذرواژه ها با هم برابر نیستند')
   
class UserUpdate(forms.ModelForm):
    class Meta:
        model=User
        fields=('fname','lname','email','photo')

class passwordForm(forms.Form):
    password=forms.CharField(label='گذرواژه فعلی',widget=forms.PasswordInput,required=True)
    new_password=forms.CharField(label='گذرواژه جدید',widget=forms.PasswordInput,required=True)
    re_password=forms.CharField(label='تکرار گذرواژه جدید',widget=forms.PasswordInput,required=True)

class passwordFormNew(forms.Form):
    new_password=forms.CharField(label='گذرواژه جدید',widget=forms.PasswordInput,required=True)
    re_password=forms.CharField(label='تکرار گذرواژه جدید',widget=forms.PasswordInput,required=True)

class UserSignin(forms.Form):
    email=forms.EmailField(label='رایانامه',required=True)
    password=forms.CharField(label='گذرواژه',required=True,widget=forms.PasswordInput)

class YadForm(forms.ModelForm):
    class Meta:
        model=Yadd
        fields=('content',)   
      
        

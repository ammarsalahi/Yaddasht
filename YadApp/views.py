from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.views.generic.base import View
from django.db.models import Q
from bootstrap_modal_forms.generic import BSModalCreateView
import datetime

def home(request):
    if request.session.has_key('user'):
        context={}
        users=User.objects.get(email=request.session['user'])
        try:
            yads=Yadd.objects.filter(user=users)
            context['yads']=yads
        except Yadd.DoesNotExist:
            messages.info(request,'هیچ یادداشتی وجود ندارد')    
        context['user']=users
        context['addedit']='yes'
        count=Yadd.objects.all().count()
        if count > 12:
            context[ 'topss']='ok'
        return render(request,'index.html',context)
    else:
        return redirect('signin')

def search(request):
    if request.session.has_key('user'):
        q=request.GET.get('q')
        yads=Yadd.objects.filter(Q(title__icontains=q)|Q(description__icontains=q))
        users=User.objects.get(email=request.session['user'])

        context={
            'yads':yads,
            'user':users,
            'addedit':'yes',
            'signin':request.session['signin']
        }
        return render(request,'index.html',context)
    else:
        return redirect('signin')    
    
def signin(request):
    context={}
    template_name=None
    if request.session.has_key('user'):
        return redirect('home')
    else:
        if request.method=='POST':
            form=UserSignin(request.POST)
            if form.is_valid():
                try:
                    email=form.cleaned_data['email']
                    passw=form.cleaned_data['password']
                    userme=User.objects.get(email=email,password=passw)
                    request.session['user']=userme.email
                    request.session['signin']=1
                    return redirect('home')
                except User.DoesNotExist:
                    messages.info(request=request,message='کاربر وجود ندارد')
                    return redirect('signin')
        elif request.method=='GET':
            form=UserSignin()
            context['form']=form
            context['formtitle']=' ورود به حساب کاربری'
            context['formbtn']='ورود'
            context['signin']=1
            template_name='form.html'
        return render(request,template_name,context)

class signup(View):
    template_name='form-n.html'
    def get(self,request,*args,**kwargs):
        if request.session.has_key('usernn') is not None:
            context={
                'form':UserSignup(),
                'formtitle':'ثبت نام کاربر جدید',
                'formbtn':'ثبت نام',
                'signup':'1'
            }            
            return render(request,'form-n.html',context)
        else:
            return redirect('home')  
    def post(self,request,*args,**kwargs):
        form=UserSignup(request.POST,request.FILES)
        if form.is_valid():
            request.session['user']=form.cleaned_data['email']
            form.save()
            return redirect('home')     
        else:
            messages.info(request,form.errors)  
            return redirect('signup')  

class update(View):
    template_name='form-n.html'
    def get_object(self):
        obj=None
        id=self.request.GET.get('uid')
        if id is not None:
            obj=get_object_or_404(User,id=id)
        return obj
    def get(request,self,*args,**kwargs):
        if request.session.has_key('user'):
            context={}
            obj=self.get_object()
            if obj is not None:
                context['form']=UserUpdate(instance=obj)
                context['formtitle']='ویرایش حساب کاربری'
                context['formbtn']='تکمیل'
                context['addedit']='yes'
            return render(request,self.template_name,context)
        else:
            return redirect('signin')    
    def post(request,self,*args,**kwargs):
        form=UserUpdate(request.POST,request.FILES,instance=True)
        if form.is_valid():
            form.save()   
            return redirect('home')

def logout(request):
    del request.session['user']
    return redirect('signin')



class add_yadd(View):
    template_name='add-yadd.html'
    def get(self,request,*args,**kwargs):
        if request.session.has_key('user'):
            users=User.objects.get(email=request.session['user'])
            context={
                'form':YadForm(),
                'formtitle':'افزودن یادداشت جدید',
                'formbtn':'افزودن',
                'addedit':'yes',
                'user':users,
                'add':1
            }
            return render(request,self.template_name,context)
        else:
            return redirect('signin')
    def post(self,request,*args,**kwargs):
        form=YadForm(request.POST,request.FILES)
        yad=Yadd()
        if form.is_valid():
            yad.content=form.cleaned_data['content']
            yad.date=datetime.datetime.now()
            yad.user=User.objects.get(email=request.session['user'])
            yad.save()
            print(datetime.datetime.now())
            return redirect('home')
        else:
            messages.info(request,form.errors)
            return redirect('add-yadd')   

class edit_yadd(View):
    template_name='add-yadd.html'
    def get_object(self):
        obj=None
        id=self.request.GET.get('yid')
        if id is not None:
            obj=get_object_or_404(Yadd,id=id)
        return obj

    def get(self,request,*args,**kwargs):
        context={}
        if request.session.has_key('user'):
            users=User.objects.get(email=request.session['user'])
            obj=self.get_object()
            if obj is not None:
                context['form']=YadForm(instance=obj)
                context['formtitle']='ویرایش یادداشت'
                context['formbtn']='ویرایش'
                context['addedit']='yes'
                context['user']=users
            return render(request,self.template_name,context)    
        else:
            return redirect('signin')
    def post(self,request,*args,**kwargs):
        obj=self.get_object()
        if obj is not None:
            form=YadForm(request.POST,request.FILES,instance=obj)
            if form.is_valid():
                form.save()
                return redirect('home')                                       



def delete_yadd(request):
    id=request.POST['yidd']
    yad=Yadd.objects.filter(id=id).delete()
    return redirect('home')


                      



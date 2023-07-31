from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect, get_object_or_404
from pathlib import Path
from .models import Post
from .models import UserReg
from .tasks import send_mail_task
from .tasks import send_mail_task_ce
from .tasks import send_mail_task_mk
from django.contrib import messages
from django.contrib.auth import authenticate 
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
import os
from datetime import datetime
from django.core.paginator import Paginator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.conf import settings
from io import BytesIO
from django.http import HttpResponseRedirect, Http404,FileResponse,HttpResponse
from pathlib import Path
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.db import transaction
'''
def create(request):
    for i in range(5):
        Post.objects.create(title="College Day",approved=True,date="2023-04-9",time="18:45:22",img="img/04-23/ece.jpg",cllg="mkce",venue="circuit",dept="",etype="symposium",pay="0",description="It is our College Day It is our pride and prestigious day to celebrate our college's achievements and students achievements and performances")
    return redirect('home')

'''

@login_required
def create(request):
    try:
        with transaction.atomic():
            user = request.user
            username = user.username
            if request.method == 'POST':
                if request.POST.get('title') and request.POST.get('date'):
                    
                    title= request.POST['title']
                    date= request.POST['date']
                    time= request.POST['time']
                    cllg = request.POST['cllg']
                    dept = request.POST['dept']
                    etype = request.POST['etype']
                    pay = request.POST['pay']
                    ven = request.POST['ven']
                    description = request.POST['description']
                    img = request.FILES['img']
                    reglink = request.POST['reglink']
                    post = Post.objects.create(title=title,date=date,time=time,img=img,cllg=cllg,venue=ven,dept=dept,etype=etype,pay=pay,reglink=reglink,description=description)
                
                    messages.success(request, 'post appllied successfully')
                    if user.username == 'krct@post':
                        return redirect('krct@post')
                    if user.username == 'krce@post':
                        return redirect('krce@post')
                    if user.username == 'mkce@post':
                        return redirect('mkce@post') 
                     


            return render(request,'post/createpost.html',{'user':username})

    except:
        return render(request,'post/error.html')

    

@login_required
def update(request, post_id):
    with transaction.atomic():
        user = request.user
        username = user.username

            # Get the post object using the post_id provided in the URL
        post = get_object_or_404(Post, pk=post_id)

        existing_departments = post.dept

        if request.method == 'POST':
            if request.POST.get('title') and request.POST.get('date'):
                    # Only update fields with new values
                post.title = request.POST['title']
                post.date = request.POST['date']
                post.time = request.POST['time']
                post.cllg = request.POST['cllg']
                post.etype = request.POST['etype']
                post.pay = request.POST['pay']
                post.venue = request.POST['ven']
                post.description = request.POST['description']
                post.reglink = request.POST['reglink']

                    # Check if a new image was uploaded and update it
                if 'img' in request.FILES:
                    post.img = request.FILES['img']

                departments = request.POST.getlist('dept')
                post.dept = ','.join(departments) if departments else existing_departments



                post.save()

                messages.success(request, 'Post updated successfully')
                    
                    # Assuming the user.username is in the format "username@post"
                    # Extract the username part to make the redirect decisions
                user_username = user.username.split('@')[0]

                    # Make the redirection decisions based on the username
                if user_username == 'krct':
                    return redirect('krct@post')
                elif user_username == 'krce':
                    return redirect('krce@post')
                elif user_username == 'mkce':
                    return redirect('mkce@post')
                else:
                    # Redirect to a generic view for other users, change it to the desired URL
                    return redirect('generic_view_url')
                

        return render(request, 'post/updatepost.html', {'user': username, 'post': post})

    



@login_required
def addreport(request,id):
    post = Post.objects.get(id=id)
    user = request.user
    username = user.username
    global context
    if request.method == 'POST':
        context={
            'event' : request.POST['eventname'],
            'date' : request.POST['date'],
            'time' : request.POST['time'],
            'dept' : request.POST['dept'],
            'cllg' : request.POST['cllg'],
            'venue' : request.POST['venue'], 
            'coor' : request.POST['coor'],
    
              


        }
        
        buffer = BytesIO()
        fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'krct.png')
        c = canvas.Canvas(buffer,pagesize=A4)
        c.drawImage(fn,50,700,width=300,height=100)
        

        #c.drawImage(f'{settings.MEDIA_ROOT}/pics/kr.jpg',450,780,width=50,height=50)
    
        c.drawString(60,670,"Event Name")
        c.drawString(130,670,":")
        c.drawString(150,670,context['event'])
        c.drawString(60,650,"Held on")
        c.drawString(130,650,":")
        c.drawString(150,650,context['date'])
        c.drawString(60,630,"Timing")
        c.drawString(130,630,":")
        c.drawString(150,630,context['time'])
        c.drawString(60,610,"Department")
        c.drawString(130,610,":")
        c.drawString(150,610,context['dept'])
        c.drawString(60,590,"Co-ordinator")
        c.drawString(130,590,":")
        c.drawString(150,590,context['coor'])
        c.save()

        pdf = buffer.getvalue()
        buffer.close()
        post.reportpdf.save(f"{context['event']}.pdf", File(BytesIO(pdf)))
        post.report = True
        post.save()
        return redirect('krct@post')



    return render(request,'post/report.html',{'post':post,'user':username})

def viewreport(request,id):
    post = Post.objects.get(id=id)
    filepath = os.path.join(settings.MEDIA_ROOT,post.reportpdf.name)
    print(filepath)
    return FileResponse(open(filepath, "rb"))


def reg(request,id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':        
        name= request.POST['name']
        email= request.POST['email']
        cllgname= request.POST['cllgname']
        sors =  request.POST['sors']
        eve =request.POST['eve']
        ecllg = request.POST['ecllg']
        uimg= request.FILES['uimg']
        UserReg.objects.create(name=name,email=email,cllgname=cllgname,verify=uimg,sors=sors,event=eve,fromcllg=ecllg)
        messages.success(request, 'Registered successfully')
        return redirect('home')

    return render(request,'post/contact.html',{'post':post})


def post(request):
    
    post = Post.objects.all()
    poster = Post.objects.filter(approved=True,is_archive=False)
    flag = True
    gi_sym = Post.objects.filter(etype__contains="symposium",approved=True).count()
    gi_w = Post.objects.filter(etype__contains="workshop",approved=True).count()
    gi_ww = Post.objects.filter(etype__contains="webinar",approved=True).count()
    gi_f = Post.objects.filter(etype__contains="fd",approved=True).count()
    ct_sym = Post.objects.filter(cllg__contains="krct",etype__contains="symposium",approved=True).count()
    ct_w = Post.objects.filter(cllg__contains="krct",etype__contains="workshop",approved=True).count()
    ct_ww = Post.objects.filter(cllg__contains="krct",etype__contains="webinar",approved=True).count()
    ct_f = Post.objects.filter(cllg__contains="krct",etype__contains="fd",approved=True).count()
    ce_sym = Post.objects.filter(cllg__contains="krce",etype__contains="symposium",approved=True).count()
    ce_w = Post.objects.filter(cllg__contains="krce",etype__contains="workshop",approved=True).count()
    ce_ww = Post.objects.filter(cllg__contains="krce",etype__contains="webinar",approved=True).count()
    ce_f = Post.objects.filter(cllg__contains="krce",etype__contains="fd",approved=True).count()
    mk_sym = Post.objects.filter(cllg__contains="mkce",etype__contains="symposium",approved=True).count()
    mk_w = Post.objects.filter(cllg__contains="mkce",etype__contains="workshop",approved=True).count()
    mk_ww = Post.objects.filter(cllg__contains="mkce",etype__contains="webinar",approved=True).count()
    mk_f = Post.objects.filter(cllg__contains="mkce",etype__contains="fd",approved=True).count()
    #


    if request.method == "POST":
        item = request.POST.get('search')
        if item != '':
            post = Post.objects.filter(title__contains=item) 
            context = {'post':post}
            return render(request,'post/index.html',context)
        else:
            p = Paginator(post, 12)
            page = request.GET.get('page')
            venues = p.get_page(page)
            nums = "a" * venues.paginator.num_pages
            context = {"posts":post,"post":venues,"nums":nums}
            return render(request,'post/index.html',context)
    


   
    
    context = {"posts":post,
    "post":poster[:6],
    "poster":poster[:5] if len(poster) > 0 else flag,
     "gisym":gi_sym,
    "giw":gi_w,
    "giww":gi_ww,
    "gif":gi_f,
    "ctsym":ct_sym,
    "ctw":ct_w,
    "ctww":ct_ww,
    "ctf":ct_f,
    "cesym":ce_sym,
    "cew":ce_w,
    "ceww":ce_ww,
    "cef":ce_f,
    "mksym":mk_sym,
    "mkw":mk_w,
    "mkww":mk_ww,
    "mkf":mk_f    
    }
    return render(request,'post/index.html',context)
    

def fest(request):
    
    post = Post.objects.filter(approved=True,is_archive=False)
    
    flag = True
    #


    

    '''
    p = Paginator(post, 12)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = "a" * venues.paginator.num_pages
    '''
    context = {"posts":post if len(post) > 0 else True
    #"post":venues,"nums":nums,
    
    }
    return render(request,'post/fest.html',context)
    

    
@login_required    
def krctiqac(request):
    user = request.user
    if user.username == 'krct@iqac':

        post = Post.objects.filter(cllg__contains='krct')
        '''
        p = Paginator(post, 12)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        '''
        context = {"posts":post,#"post":venues,"nums":nums
        }
        return render(request,'post/krctiqac.html',context)
    else:
        return HttpResponse('Your Not Authorized for this page')


@login_required
def krceiqac(request):
    user = request.user
    if user.username == 'krce@iqac':
        post = Post.objects.filter(cllg__contains='krce')
        if request.method == "POST":
            item = request.POST.get('search')
            if item != '':
                post = Post.objects.filter(title__contains=item) 
                context = {'post':post}
                return render(request,'post/krceiqac.html',context)
            else:
                p = Paginator(post, 12)
                page = request.GET.get('page')
                venues = p.get_page(page)
                nums = "a" * venues.paginator.num_pages
                context = {"posts":post,"post":venues,"nums":nums}
                return render(request,'post/krceiqac.html',context)
        '''
        p = Paginator(post, 12)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        '''
        context = {"posts":post,#"post":venues,"nums":nums
        }
        return render(request,'post/krceiqac.html',context)
    else:
        return HttpResponse('Your Not Authorized for this page')


@login_required
def mkceiqac(request):
    user = request.user
    if user.username == 'mkce@iqac':
        post = Post.objects.filter(cllg__contains='mkce')
        if request.method == "POST":
            item = request.POST.get('search')
            if item != '':
                post = Post.objects.filter(title__contains=item) 
                context = {'post':post}
                return render(request,'post/mkceiqac.html',context)
            else:
                p = Paginator(post, 12)
                page = request.GET.get('page')
                venues = p.get_page(page)
                nums = "a" * venues.paginator.num_pages
                context = {"posts":post,"post":venues,"nums":nums}
                return render(request,'post/mkceiqac.html',context)
        

        p = Paginator(post, 12)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        
        context = {"posts":post,"post":venues,"nums":nums}
        return render(request,'post/mkceiqac.html',context)
    else:
        return HttpResponse('Your Not Authorized for this page')

@login_required
def krce_post(request):
    user = request.user
    if user.username == 'krce@post':
        post = Post.objects.filter(cllg__contains='krce',is_archive=False)
        if request.method == "POST":
            item = request.POST.get('search')
            if item != '':
                post = Post.objects.filter(title__contains=item) 
                context = {'post':post}
                return render(request,'post/krce@post.html',context)
            else:
                p = Paginator(post, 12)
                page = request.GET.get('page')
                venues = p.get_page(page)
                nums = "a" * venues.paginator.num_pages
                context = {"posts":post,"post":venues,"nums":nums}
                return render(request,'post/krce@post.html',context)
        

        p = Paginator(post, 12)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        
        context = {"posts":post,"post":venues,"nums":nums}
        return render(request,'post/krce@post.html',context)
    else:
        return HttpResponse('Your Not Authorized for this page')

@login_required
def krct_post(request):
    user = request.user
    if user.username == 'krct@post':
        post = Post.objects.filter(cllg__contains='krct',is_archive=False)
        if request.method == "POST":
            item = request.POST.get('search')
            if item != '':
                post = Post.objects.filter(title__contains=item) 
                context = {'post':post}
                return render(request,'post/krct@post.html',context)
            else:
                p = Paginator(post, 12)
                page = request.GET.get('page')
                venues = p.get_page(page)
                nums = "a" * venues.paginator.num_pages
                context = {"posts":post,"post":venues,"nums":nums}
                return render(request,'post/krct@post.html',context)
        

        p = Paginator(post, 12)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        
        context = {"posts":post,"post":venues,"nums":nums}
        return render(request,'post/krct@post.html',context)
    else:
        return HttpResponse('Your Not Authorized for this page')

@login_required
def mkce_post(request):
    user = request.user
    if user.username == 'mkce@post':
        post = Post.objects.filter(cllg__contains='mkce',is_archive=False)
        if request.method == "POST":
            item = request.POST.get('search')
            if item != '':
                post = Post.objects.filter(title__contains=item) 
                context = {'post':post}
                return render(request,'post/mkce@post.html',context)
            else:
                p = Paginator(post, 12)
                page = request.GET.get('page')
                venues = p.get_page(page)
                nums = "a" * venues.paginator.num_pages
                context = {"posts":post,"post":venues,"nums":nums}
                return render(request,'post/mkce@post.html',context)
        

        p = Paginator(post, 12)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        
        context = {"posts":post,"post":venues,"nums":nums}
        return render(request,'post/mkce@post.html',context)
    else:
        return HttpResponse('Your Not Authorized for this page')

@login_required
def krcecoordinator(request):
    user = request.user
    if user.username == 'krce@coordinator':
        post = UserReg.objects.filter(fromcllg__contains='krce')
        if request.method == "POST":
            item = request.POST.get('search')
            if item != '':
                post = Post.objects.filter(title__contains=item) 
                context = {'post':post}
                return render(request,'post/kececoordinator.html',context)
            else:
                p = Paginator(post, 12)
                page = request.GET.get('page')
                venues = p.get_page(page)
                nums = "a" * venues.paginator.num_pages
                context = {"posts":post,"post":venues,"nums":nums}
                return render(request,'post/krcecoordinator.html',context)
        

        p = Paginator(post, 12)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        
        context = {"posts":post,"post":venues,"nums":nums}
        return render(request,'post/krcecoordinator.html',context)
    else:
        return HttpResponse('Your Not Authorized for this page')

@login_required
def krctcoordinator(request):
    user = request.user
    if user.username == 'krct@coordinator':
        post = UserReg.objects.filter(fromcllg__contains='krct')
        if request.method == "POST":
            item = request.POST.get('search')
            if item != '':
                post = Post.objects.filter(title__contains=item) 
                context = {'post':post}
                return render(request,'post/krctcoordinator.html',context)
            else:
                p = Paginator(post, 12)
                page = request.GET.get('page')
                venues = p.get_page(page)
                nums = "a" * venues.paginator.num_pages
                context = {"posts":post,"post":venues,"nums":nums}
                return render(request,'post/krctcoordinator.html',context)
        

        p = Paginator(post, 12)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        
        context = {"posts":post,"post":venues,"nums":nums}
        return render(request,'post/krcecoordinator.html',context)
    else:
        return HttpResponse('Your Not Authorized for this page')



@login_required
def mkcecoordinator(request):
    user = request.user
    if user.username == 'mkce@coordinator':
        post = UserReg.objects.filter(fromcllg__contains='mkce')
        if request.method == "POST":
            item = request.POST.get('search')
            if item != '':
                post = Post.objects.filter(title__contains=item) 
                context = {'post':post}
                return render(request,'post/mkcecoordinator.html',context)
            else:
                p = Paginator(post, 12)
                page = request.GET.get('page')
                venues = p.get_page(page)
                nums = "a" * venues.paginator.num_pages
                context = {"posts":post,"post":venues,"nums":nums}
                return render(request,'post/mkcecoordinator.html',context)
        

        p = Paginator(post, 12)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        
        context = {"posts":post,"post":venues,"nums":nums}
        return render(request,'post/mkcecoordinator.html',context)
    else:
        return HttpResponse('Your Not Authorized for this page')





def login(request):
    
    
    if request.method == 'POST': 
        userr = request.user
        username = request.POST.get('user')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
    
        if user is not None:
            auth_login(request, user)
            messages.success(request, 'logged in successfully')
        # Redirect to a success page.
            if userr.username == 'krct@iqac':
                return redirect('krctiqac') 
            if userr.username == 'krce@iqac':
                return redirect('krceiqac') 
            if userr.username == 'mkce@iqac':
                return redirect('mkceiqac') 
            if userr.username == 'krct@post':
                return redirect('krct@post') 
            if userr.username == 'krce@post':
                return redirect('krce@post')
            if userr.username == 'mkce@post':
                return redirect('mkce@post') 
            if userr.username == 'krct@coordinator':
                return redirect('krctco')
            if userr.username == 'krce@coordinator':
                return redirect('krceco')
            if userr.username == 'mkce@coordinator':
                return redirect('mkceco') 
        
        else:
            messages.error(request, 'invalid username or password')
            return redirect('login')
        
    return render(request,'post/login.html')





def admin_post(request): 
    post = Post.objects.all() 
    if request.method == "POST":
        item = request.POST.get('search')
        post = Post.objects.filter(title__contains=item) 
        context = {'post':post}
        render(request,'post/admin@post.html',context) 

    context = {'posts':post}

    return render(request,'post/admin@post.html',context) 

@login_required
def delete(request,id):
    post = Post.objects.get(id=id)
    image = post.img.name
    pdf = post.reportpdf.name
    if os.path.isfile(image):
       os.remove(image)
    if os.path.isfile(pdf):
       os.remove(pdf)
    post.delete()
    messages.success(request, 'deleted successfully')
    if request.user.username == 'krct@iqac':
        return redirect('krctiqac')
    if request.user.username == 'krce@iqac':
        return redirect('krceiqac')
    if request.user.username == 'mkce@iqac':
        return redirect('mkceiqac')

def ac(request,id):
    post = Post.objects.get(id=id)
    '''
    image = post.img.url
    if os.path.isfile(image):
       os.remove(image)
    '''
    post.delete()
    return redirect('active')


def detail(request,id):
    post = Post.objects.get(id=id)
    poster = Post.objects.filter(cllg__contains=post.cllg,etype__contains=post.etype,approved=True,is_archive=False)
    context = {'post':post,'poster':poster[:6],'clg':post.cllg}
    return render(request,'post/fdetail.html',context)

def regdetail(request,id):
    post = UserReg.objects.get(id=id)
    context = {'post':post}
    return render(request,'post/regdetail.html',context)


@login_required
def admindetail(request,id):
    post = Post.objects.get(id=id)
    context = {'post':post}
    return render(request,'post/admindetail.html',context)

@login_required
def postadmindetail(request,id):
    post = Post.objects.get(id=id)
    context = {'post':post}
    return render(request,'post/postadmindetail.html',context)



'''
def reqdetail(request,id):
    post = Post.objects.get(id=id)
    context = {'post':post}
    return render(request,'post/detail.html',context)
'''

def logout(request):
    auth_logout(request)
    return redirect('home') 

@login_required
def approve(request,id):
    post = Post.objects.get(id=id)
    post.approved = True
    post.save(update_fields=['approved'])
    if request.user.username == 'krct@iqac':
        return redirect('krctiqac')
    if request.user.username == 'krce@iqac':
        return redirect('krceiqac')
    if request.user.username == 'mkce@iqac':
        return redirect('mkceiqac')

@login_required
def close(request,id):
    mail = list()
    post = Post.objects.get(id=id)
    uemail = UserReg.objects.filter(event__contains=post.title).count()
    
    post.closed = True
    post.save(update_fields=['closed'])
    if request.user.username == 'krct@iqac':
        if uemail != 0:
            send_mail_task.delay(id)
            return redirect('krctiqac')
        else:
            return redirect('krctiqac')
    if request.user.username == 'krce@iqac':
        if uemail != 0:
            send_mail_task_ce.delay(id)
            return redirect('krceiqac')
        else:
            return redirect('krceiqac')
    if request.user.username == 'mkce@iqac':
        if uemail != 0:
            send_mail_task_mk.delay(id)
            return redirect('mkceiqac')
        else:
            return redirect('mkceiqac')

@login_required
def open(request,id):
    post = Post.objects.get(id=id)
    post.closed = False
    post.save(update_fields=['closed'])
    if request.user.username == 'krct@iqac':
        return redirect('krctiqac')
    if request.user.username == 'krce@iqac':
        return redirect('krceiqac')
    if request.user.username == 'mkce@iqac':
        return redirect('mkceiqac')



flag = False
@login_required
def undo(request,id):
    post = Post.objects.get(id=id)
    post.approved = False
    post.save(update_fields=['approved'])
    if request.user.username == 'krct@iqac':
        return redirect('krctiqac')
    if request.user.username == 'krce@iqac':
        return redirect('krceiqac')
    if request.user.username == 'mkce@iqac':
        return redirect('mkceiqac')

@login_required
def archive(request,id):
    post = Post.objects.get(id=id)
    post.is_archive = True
    post.save(update_fields=['is_archive'])
    messages.success(request, 'Added to Archives successfully')
    if request.user.username == 'krct@iqac':
        return redirect('krctiqac')
    if request.user.username == 'krce@iqac':
        return redirect('krceiqac')
    if request.user.username == 'mkce@iqac':
        return redirect('mkceiqac')


@login_required    
def krctiqac_archive(request):
    user = request.user
    if user.username == 'krct@iqac':

        post = Post.objects.filter(cllg__contains='krct',is_archive=True)
        if request.method == "POST":
            item = request.POST.get('search')
            if item != '':
                post = Post.objects.filter(title__contains=item) 
                context = {'post':post}
                return render(request,'post/archive.html',context)
            else:
                p = Paginator(post, 12)
                page = request.GET.get('page')
                venues = p.get_page(page)
                nums = "a" * venues.paginator.num_pages
                context = {"posts":post,"post":venues,"nums":nums}
                return render(request,'post/archive.html',context)
        

        p = Paginator(post, 12)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        
        context = {"posts":post,"post":venues,"nums":nums}
        return render(request,'post/archive.html',context)
    else:
        return HttpResponse('Your Not Authorized for this page')

@login_required    
def krceiqac_archive(request):
    user = request.user
    if user.username == 'krce@iqac':

        post = Post.objects.filter(cllg__contains='krce',is_archive=True)
        if request.method == "POST":
            item = request.POST.get('search')
            if item != '':
                post = Post.objects.filter(title__contains=item) 
                context = {'post':post}
                return render(request,'post/archive@krce.html',context)
            else:
                p = Paginator(post, 12)
                page = request.GET.get('page')
                venues = p.get_page(page)
                nums = "a" * venues.paginator.num_pages
                context = {"posts":post,"post":venues,"nums":nums}
                return render(request,'post/archive@krce.html',context)
        

        p = Paginator(post, 12)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        
        context = {"posts":post,"post":venues,"nums":nums}
        return render(request,'post/archive@krce.html',context)
    else:
        return HttpResponse('Your Not Authorized for this page')


@login_required    
def mkceiqac_archive(request):
    user = request.user
    if user.username == 'mkce@iqac':

        post = Post.objects.filter(cllg__contains='mkce',is_archive=True)
        if request.method == "POST":
            item = request.POST.get('search')
            if item != '':
                post = Post.objects.filter(title__contains=item) 
                context = {'post':post}
                return render(request,'post/archive@mkce.html',context)
            else:
                p = Paginator(post, 12)
                page = request.GET.get('page')
                venues = p.get_page(page)
                nums = "a" * venues.paginator.num_pages
                context = {"posts":post,"post":venues,"nums":nums}
                return render(request,'post/archive@mkce.html',context)
        

        p = Paginator(post, 12)
        page = request.GET.get('page')
        venues = p.get_page(page)
        nums = "a" * venues.paginator.num_pages
        
        context = {"posts":post,"post":venues,"nums":nums}
        return render(request,'post/archive@mkce.html',context)
    else:
        return HttpResponse('Your Not Authorized for this page')

'''

def active(request):
    post = ApprovedPost.objects.all()
    if request.method == "POST":
        if request.POST != '':
            item = request.POST.get('search')
            post = ApprovedPost.objects.filter(title__contains=item) 
            context = {'post':post}
            return render(request,'post/activeindex.html',context)
        else:
             context = {"posts":post}
             return render(request,'post/activeindex.html',context)

    context = {'posts':post}
    return render(request,'post/activeindex.html',context)
'''
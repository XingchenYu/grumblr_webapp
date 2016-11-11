from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from models import *

from forms import *
import datetime
from django.utils import timezone
from mimetypes import guess_type
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core import serializers

# Create your views here.

@transaction.atomic
def home(request):
    blog_stream=Blog.objects.order_by('-pub_date')
    context={}
    context['blogs']=blog_stream

    if request.method=='GET':
        context['form'] = signForm()
        return render(request, "grumblr/guest_home.html",context)

    form = signForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'grumblr/guest_home.html', context)
    
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        context['user']=user
        login(request, user)
        return redirect(reverse('home1'))
    else:
        return render(request, "grumblr/guest_home.html",context)

@login_required
def logout_view(request):
    logout(request)
    return redirect("grumblr/guest_home.html")

@transaction.atomic
def register_user(request):
    context = {}
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = profileForm()
        context['form2'] = editOtherForm()
        return render(request, 'grumblr/registration.html', context)
    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = profileForm(request.POST)
    form2 = editOtherForm(request.POST, request.FILES)
    context['form'] = form
    context['form2'] = form2
    # Validates the form.
    if not form.is_valid():
        return render(request, 'grumblr/registration.html', context)
    if not form2.is_valid():
        return render(request, 'grumblr/registration.html', context)
    # If we get here the form data was valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'], email=form.cleaned_data['email'],
                                        password=form.cleaned_data['password'],
                                        is_active=False)
    new_user.save()
    my_user = Myuser(user=new_user, age=form2.cleaned_data['age'],
                     bio=form2.cleaned_data['bio'], photo=form2.cleaned_data['photo'])
    my_user.save()
    # new_user = authenticate(username=form.cleaned_data['username'],
    #                         password=form.cleaned_data['password'])

    token = default_token_generator.make_token(new_user)
    email_body = """
    Welcome to Grumblr. Please click the link below to verify your email address and complete the registration of your account:

    http://%s%s
    """ % (request.get_host(), reverse('confirm', args = (new_user.username, token)))
    send_mail(subject="Verify your email address",
              message = email_body,
              from_email = "xingche1@andrew.cmu.edu",
              recipient_list = [new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'grumblr/confirm.html', context)

@transaction.atomic
def confirm(request, name, token):
    user=get_object_or_404(User, username = name)
    if (default_token_generator.check_token(user, token)):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(reverse('home1'))
    else:
        return redirect(reverse('register'))



@login_required
@transaction.atomic
def myaccount(request):
    cu_user=request.user
    my_user=get_object_or_404(Myuser, user=cu_user)
    blog_my=cu_user.blog_set.order_by('-pub_date')
    context={'blog_my':blog_my, 'my_user':my_user}
    return render(request, "grumblr/profile_my.html",context)

@login_required
@transaction.atomic
def post(request):
    context={}

    if request.method == 'GET':
        # context['form'] = request.POST
        return render(request, "grumblr/post_new.html",context)

    form = postForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        print ('middle111')
        return render(request, 'grumblr/post_new.html', context)

    new_blog=Blog(content=form.cleaned_data['blog'], pub_date=datetime.datetime.now(), user=request.user)
    new_blog.save()
    return HttpResponse("")

# @login_required
# @transaction.atomic
# def do_post(request):
#     if not 'blog' in request.POST or not request.POST['blog']:
#         print request.POST['blog']
#         raise Http404
#     else:
#         new_blog = Blog(content=request.POST['blog'],pub_date=timezone.now(), user=request.user)
#         new_blog.save()
#     return redirect(reverse('home1'))
    # return HttpResponse("")

@login_required
@transaction.atomic
def profile(request, profile_id):
    try:
        choose_user = User.objects.get(id=profile_id)
    except ObjectDoesNotExist:
        return redirect(reverse('home1'))
    # choose_user = User.objects.get(id=profile_id)
    cu_myuser = Myuser.objects.get(user=request.user)
    follow_list = cu_myuser.follow.all()
    my_user = get_object_or_404(Myuser, user=choose_user)
    blog_his=choose_user.blog_set.order_by('-pub_date')
    context = {'choose_user':choose_user, 'blog_his':blog_his, 'my_user':my_user,
               'cu_myuser': cu_myuser, 'follow_list':follow_list}
    return render(request, 'grumblr/profile.html', context)


@login_required
@transaction.atomic
def edit(request):
    cu_user=request.user
    cur_my = get_object_or_404(Myuser, user=cu_user)
    if request.method == 'GET':
        form = editForm(instance = cu_user)
        form2 = editOtherForm(instance=cur_my)
        context = {'form': form, 'form2': form2}
        return render(request, "grumblr/edit.html", context)

    form = editForm(request.POST, instance=cu_user)
    form2 = editOtherForm(request.POST, request.FILES, instance=cur_my)
    if not form.is_valid():
        context = {'form': form, 'form2': form2}
        return render(request, 'grumblr/edit.html', context)
    if not form2.is_valid():
        context = {'form': form, 'form2': form2}
        return render(request, 'grumblr/edit.html', context)

    form.save()
    form2.save()
    return redirect(reverse('account'))


@login_required
@transaction.atomic
def follow(request, profile_id):
    user = request.user
    try:
        choose_user = User.objects.get(id=profile_id)
    except ObjectDoesNotExist:
        return redirect(reverse('home1'))
    blog_his = choose_user.blog_set.order_by('-pub_date')
    cu_myuser = Myuser.objects.get(user=user)
    my_user = get_object_or_404(Myuser, user=choose_user)
    cu_myuser.follow.add(choose_user)
    cu_myuser.save()
    follow_list = cu_myuser.follow.all()
    context = {'choose_user': choose_user, 'blog_his': blog_his, 'my_user': my_user,
               'cu_myuser': cu_myuser, 'follow_list':follow_list}
    return render(request, 'grumblr/profile.html', context)


@login_required
@transaction.atomic
def unfollow(request, profile_id):
    user = request.user
    try:
        choose_user = User.objects.get(id=profile_id)
    except ObjectDoesNotExist:
        return redirect(reverse('home1'))
    blog_his = choose_user.blog_set.order_by('-pub_date')
    cu_myuser = Myuser.objects.get(user=user)
    my_user = get_object_or_404(Myuser, user=choose_user)
    cu_myuser.follow.remove(choose_user)
    cu_myuser.save()
    follow_list = cu_myuser.follow.all()
    # print cu_myuser.follow.all()
    context = {'choose_user': choose_user, 'blog_his': blog_his, 'my_user': my_user,
               'cu_myuser': cu_myuser, 'follow_list':follow_list}
    return render(request, 'grumblr/profile.html', context)


@login_required
@transaction.atomic
def followstream(request):
    user = request.user
    my_user = get_object_or_404(Myuser, user=user)
    follow_list = my_user.follow.all()
    stream = Blog.objects.filter(user__in = my_user.follow.all()).order_by('-pub_date')
    context = {'my_user': my_user, 'follow_list': follow_list, 'stream': stream}
    return render(request, 'grumblr/follow_stream.html', context)

@transaction.atomic
def photo(request, profile_id):
    user = User.objects.get(id=profile_id)
    my_user = get_object_or_404(Myuser, user = user)
    if not my_user.photo:
        raise Http404
    content_type = guess_type(my_user.photo.name)
    return HttpResponse(my_user.photo, content_type = content_type)


@login_required
@transaction.atomic
def blog_delete(request, blog_id):
    errors = []
    try:
        blog_delete = Blog.objects.get(id=blog_id, user=request.user)
        blog_delete.delete()
    except ObjectDoesNotExist:
        errors.append('The blog is not existed')
    return redirect(reverse('account'))

@login_required
@transaction.atomic
def changepassword(request):
    my_user = Myuser.objects.get(user = request.user)
    if request.method == 'GET':
        form = ChangePasswordForm()
        return render(request, 'grumblr/change_password.html', {'form': form, 'my_user': my_user})
    else:
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            username = request.user.username
            oldpassword = form.cleaned_data['oldpassword']
            user = authenticate(username=username, password=oldpassword)
            if user is not None and user.is_active:
                newpassword = form.cleaned_data['newpassword1']
                user.set_password(newpassword)
                user.save()
                login(request, user)
                return redirect(reverse('home1'))
            else:
                return render(request, 'grumblr/change_password.html', {'form': form, 'my_user': my_user, 'oldpassword_is_wrong': True})
        else:
            return render(request, 'grumblr/change_password.html', {'form': form, 'my_user': my_user})

@transaction.atomic
def forgetpassword(request):
    context = {}
    if request.method == 'GET':
        context['form'] = ForgetPasswordForm()
        return render(request, 'grumblr/forget_password.html', context)
    form = ForgetPasswordForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'grumblr/forget_password.html', context)
    cu_user = User.objects.get(username=form.cleaned_data['username'])
    token = default_token_generator.make_token(cu_user)
    email_body = """
        Please click the link below to reset your email:

        http://%s%s
        """ % (request.get_host(), reverse('reset', args=(cu_user.username, token)))
    send_mail(subject="Reset your password of Grumblr",
              message=email_body,
              from_email="xingche1@andrew.cmu.edu",
              recipient_list=[cu_user.email])

    context['email'] = cu_user.email
    message=[]
    message.append('Please check your email to reset your password!')
    context['message'] = message
    return render(request, 'grumblr/forget_password.html', context)

def reset(request, name, token):
    user = get_object_or_404(User, username=name)
    if (default_token_generator.check_token(user, token)):
        if request.method == 'GET':
            form = ResetPasswordForm()
            context = {'name': name, 'form': form, 'token':token}
            return render(request, 'grumblr/reset.html', context)
        else:
            form = ResetPasswordForm(request.POST)
            context = {'name': name, 'form': form, 'token':token}
            if form.is_valid():
                newpassword = form.cleaned_data['newpassword1']
                user.set_password(newpassword)
                user.save()
                login(request, user)
                return redirect(reverse('home1'))
            else:
                return render(request, 'grumblr/reset.html', context)
    else:
        return redirect(reverse('forgetpassword'))

@login_required
@transaction.atomic
def comment(request, blog_id):
    print blog_id
    if not 'comment' in request.POST or not request.POST['comment']:
        print blog_id
        raise Http404
    else:
        blog = Blog.objects.get(id = blog_id)
        print blog.content
        new_comment = Comment(text = request.POST['comment'], blog = blog, com_user = request.user)
        new_comment.save()
        print new_comment.text
        comments = Comment.objects.all()
        blog = Blog.objects.get(id = blog_id)
        context ={'blog': blog, 'comments': comments}
        return render(request,'grumblr/comments.json', context, content_type='application/json')

# def get_blog(request):
#     response_text = serializers.serialize("json", Blog.objects.all())
#     return HttpResponse(response_text, content_type="application/json")


# # Returns all recent additions in the database, as JSON
# def get_items(request, time="1970-01-01T00:00+00:00"):
#     max_time = Blog.get_max_time()
#     blogs = Blog.get_items(time)
#     context = {"max_time": max_time, "blogs": blogs}
#     return render(request, 'blogs.json', context, content_type='application/json')


# Returns all recent changes to the database, as JSON
def get_changes(request, time="1970-01-01T00:00+00:00"):
    max_time = Blog.get_max_time()
    blogs = Blog.get_changes(time)
    context = {"max_time": max_time, "blogs": blogs}
    return render(request, 'grumblr/blogs.json', context, content_type='application/json')
def get_posts(request):
    max_time = Blog.get_max_time()
    # print max_time
    blogs = Blog.objects.order_by('-pub_date')
    context = {"max_time": max_time, "blogs": blogs}
    print max_time
    print "akkakakakak"
    return render(request, 'grumblr/blogs.json', context, content_type='application/json')


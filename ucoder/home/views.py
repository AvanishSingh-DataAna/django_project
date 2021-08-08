from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.
def home(request):
    # fetch top 3 posts based on number of views
    context = {}
    return render(request, 'home/home.html',context)

def about(request):
    messages.success(request, 'This is About')
    return render(request, 'home/about.html')

def contact(request):
    messages.success(request, ' Welcome to Contact')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, 'Please fill the form correctly')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, ' your message has been successfully sent')

    return render(request, 'home/contact.html')
    
def search(request):
    query = request.GET['query']
    if len(query)>60:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent,allPostsAuthor)
    if allPosts.count() == 0:
        messages.warning(request, ' No search results found. please refine your query')
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)
    

def handelSignup(request):
    if request.method == 'POST':
        # get the post parameter
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        #check for errorneous input
        if len(username) > 13:
            messages.error(request, "username must be less than 10 characters")
            return redirect('home')

        if not username.isalnum():
            messages.error(request, "username should only contain letters and numbers")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Your passwords do not match")
            return redirect('home')


        #create the user

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your Ucoder account has been successfully created")
        return redirect('home')

    else:
        return HttpResponse('404 not found')

def handelLogin(request):
    if request.method == 'POST':
        # get the post parameter
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in to your Ucoder Account")
            return redirect('home')
        else:
            messages.error(request, "Invalid Username or password!!! please try again")
            return redirect('home')
            


    return HttpResponse('404 - Not found')

def handelLogout(request):

    logout(request)
    messages.success(request, "You have successfully logged Out to your Ucoder Account")
    return redirect('home')





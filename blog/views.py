from django.http import Http404
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def signupview(request):
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})

        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Authenticate and log in the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful signup
        else:
            return render(request, 'signup.html', {'error': 'Failed to authenticate'})

    return render(request, 'signup.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def loginview(request):
    if request.method == 'POST':
        username_or_email = request.POST['usernameOrEmail']
        password = request.POST['password']

        # Check if the input is an email address
        if '@' in username_or_email:
            # Authenticate with email
            user = authenticate(request, email=username_or_email, password=password)
        else:
            # Authenticate with username
            user = authenticate(request, username=username_or_email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to home page after successful login
        else:
            return render(request, 'login.html', {'error': 'Invalid username/email or password'})

    return render(request, 'login.html')


import requests
from django.shortcuts import render

@login_required
def home(request):
    # Your News API key
    api_key = '83136f4e88364bb099838906e0fab993'
    # News API endpoint for wsj.com
    api_url = f'https://newsapi.org/v2/everything?domains=wsj.com&apiKey={api_key}'


    try:
        # Fetch news from News API
        response = requests.get(api_url)
        news_data = response.json()

        # Extract articles from news data
        articles = news_data.get('articles', [])
        user_blogs = blog.objects.all().order_by('-id')

        # Pass articles to the template
        return render(request, 'index.html', {'articles': articles ,'user_blogs': user_blogs})

    except Exception as e:
        # Handle errors
        error_message = str(e)
        return render(request, 'error.html', {'error_message': error_message})


from .models import blog
def editblog(request):
    user_blogs = blog.objects.filter(user=request.user).order_by('-id')
    return render(request, 'editblog.html', {'user_blogs': user_blogs})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import blog

@login_required
def createblog(request):
    if request.method == 'POST':
        # Check if the form is for editing an existing blog
        if 'blog_id' in request.POST:
            blog_id = request.POST.get('blog_id')
            # Get the existing blog instance
            existing_blog = blog.objects.get(pk=blog_id)
            # Delete the existing blog
            existing_blog.delete()
            print('deleted')
        
        # Create a new blog instance with the submitted data
        topic = request.POST.get('topic')
        content = request.POST.get('blog_value')
        user = request.user
        new_blog = blog.objects.create(user=user, topic=topic, content=content)
        
        # Redirect to a success page or wherever you want
        return redirect('/editblog')  # Replace 'success_page' with the name of your success page URL pattern
    else:
        return render(request, 'editblog.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import blog

@login_required
def deleteblog(request, blog_id):
    # Retrieve the blog instance to be deleted
    blog_to_delete = blog.objects.get(pk=blog_id)
    # Check if the logged-in user is the owner of the blog
    if blog_to_delete.user == request.user:
        # Delete the blog
        blog_to_delete.delete()
        # Redirect to a success page or wherever you want
        return redirect('/editblog')  # Replace 'success_page' with the name of your success page URL pattern
    else:
        # If the logged-in user is not the owner of the blog, handle unauthorized access
        # You can redirect to an error page or display an error message
        # For simplicity, let's redirect to the home page
        return redirect('/')


# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import blog
from .serializers import BlogSerializer
from rest_framework.permissions import IsAdminUser
class BlogListAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        blogs = blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import blog
from .serializers import BlogSerializer

class BlogListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        blogs = blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogRetrieveUpdateDestroyAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return blog.objects.get(pk=pk)
        except blog.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        blog = self.get_object(pk)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = self.get_object(pk)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


from django.shortcuts import render, get_object_or_404
def fullBlog(request,pk):
    blogs = get_object_or_404(blog, pk=pk)

    # Render the blog content in a template
    return render(request, 'full_blog.html', {'blog': blogs})

import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Material, DownloadLog
from .forms import MaterialForm, ReviewForm, SimpleUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def home(request):
    materials = Material.objects.all().order_by('-upload_date')[:5]
    return render(request, 'library/home.html', {'materials': materials})


def material_list(request):
    category = request.GET.get('category', None)
    query = request.GET.get('q', '')
    materials = Material.objects.all()

    if query:
        materials = materials.filter(title__icontains=query) | materials.filter(description__icontains=query)
    if category:
        materials = materials.filter(category=category)

    return render(request, 'library/material_list.html', {'materials': materials, 'selected_category': category})

def material_detail(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    reviews = material.reviews.all()
    return render(request, 'library/material_detail.html', {'material': material, 'reviews': reviews})

@login_required(login_url='login')
def upload_material(request):
    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.save()
            messages.success(request, "Material uploaded successfully!")
            return redirect('material_list')
    else:
        form = MaterialForm()
    return render(request, 'library/upload_material.html', {'form': form})

@login_required(login_url='login')
def download_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    file_path = material.file.path
    if not os.path.exists(file_path):
        return HttpResponse("File not found", status=404)
    DownloadLog.objects.create(user=request.user, material=material)

    return FileResponse(open(file_path, 'rb'), as_attachment=True)

@login_required
def add_review(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.material = material
            review.save()
            return redirect('material_detail', material_id=material.id)
    else:
        form = ReviewForm()
    return render(request, 'library/add_review.html', {'form': form, 'material': material})

@login_required(login_url='login')
def user_dashboard(request):
    user_materials = Material.objects.filter(uploaded_by=request.user)
    user_downloads = DownloadLog.objects.filter(user=request.user).order_by('-download_date')
    return render(request, 'library/dashboard.html', {'user_materials': user_materials, 'user_downloads': user_downloads})

def register(request):
    if request.method == "POST":
        form = SimpleUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
    else:
        form = SimpleUserCreationForm()
    return render(request, 'library/register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'library/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

@login_required(login_url='login')
def upload_material(request):
    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploaded_by = request.user
            material.save()
            return redirect('material_list')
    else:
        form = MaterialForm()
    return render(request, 'library/upload_material.html', {'form': form})

@login_required(login_url='login')
def add_review(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.material = material
            review.save()
            return redirect('material_detail', material_id=material.id)
    else:
        form = ReviewForm()
    return render(request, 'library/add_review.html', {'form': form, 'material': material})

@login_required(login_url='login')
def user_dashboard(request):
    user_materials = Material.objects.filter(uploaded_by=request.user)
    return render(request, 'library/dashboard.html', {'user_materials': user_materials})
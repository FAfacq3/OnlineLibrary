import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Material, DownloadLog, UserProfile
from .forms import MaterialForm, ReviewForm, SimpleUserCreationForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Avg


def home(request):
    latest_materials = Material.objects.all().order_by('-upload_date')[:5]
    top_materials = Material.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:5]

    return render(request, 'library/home.html', {
        'latest_materials': latest_materials,
        'top_materials': top_materials
    })

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
    reviews = material.reviews.all().order_by('-created_at')
    form = ReviewForm()

    print("Material File URL:", material.file.url if material.file else "No file uploaded")

    return render(request, 'library/material_detail.html', {
        'material': material,
        'reviews': reviews,
        'form': form
    })

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

@login_required(login_url='login')
def delete_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if request.user == material.uploaded_by or request.user.is_superuser:
        file_path = material.file.path
        material.delete()
        if os.path.exists(file_path):
            os.remove(file_path)

        messages.success(request, "Material deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this material.")

    return redirect('material_list')

@login_required
def favourite_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    user_profile = request.user.profile

    if material in user_profile.favourites.all():
       user_profile.favourites.remove(material)
       status = "removed"
    else:
       user_profile.favourites.add(material)
       status = "added"

    return JsonResponse({"status": status})

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
            return JsonResponse({
                "success": True,
                "username": request.user.username,
                "rating": review.rating,
                "comment": review.comment,
                "created_at": review.created_at.strftime("%Y-%m-%d %H:%M")
            })
    return JsonResponse({"success": False})

@login_required(login_url='login')
def user_dashboard(request):
    user_materials = Material.objects.filter(uploaded_by=request.user)
    user_downloads = DownloadLog.objects.filter(user=request.user).order_by('-download_date')
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_favourites = user_profile.favourites.all()
    print("HFJDSKLHFJSDKLHFJSDKLHFS", user_favourites)
    return render(request, 'library/dashboard.html', {'user_materials': user_materials, 'user_downloads': user_downloads, 'user_favourites':user_favourites})

def register(request):
    if request.method == "POST":
        form = SimpleUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
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
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.error(request, "Your account has been disabled.")
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
def user_dashboard(request):
    user_materials = Material.objects.filter(uploaded_by=request.user)
    user_downloads = DownloadLog.objects.filter(user=request.user).order_by('-download_date')
    user_profile = get_object_or_404(UserProfile, user=request.user)
    user_favourites = user_profile.favourites.all()
    return render(request, 'library/dashboard.html', {'user_materials': user_materials, "user_favourites": user_favourites, 'user_downloads':user_downloads})

def txt_preview(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if not material.file.url.endswith('.txt'):
        return HttpResponse("Invalid file type", status=400)

    file_path = material.file.path

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        return HttpResponse(f"Error reading file: {e}", status=500)

    return HttpResponse(f"<pre style='white-space: pre-wrap;'>{content}</pre>", content_type="text/html")
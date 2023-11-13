from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CarbonFootprintDataForm
from .utils import calculate_carbon




def welcome(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name for your home page
    else:
        form = AuthenticationForm()
    return render(request, 'welcome.html', {'form': form})
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name for your home page
            return
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace 'home' with the URL name for your home page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def carbon_calculator(request):
    if request.method == 'POST':
        form = CarbonFootprintDataForm(request.POST)
        if form.is_valid():
            carbon_data_instance = form.save()

            # Calculate carbon after saving the form
            total_emission = calculate_carbon(carbon_data_instance)

            # Render the result page with the calculated total emission
            return render(request, 'result_page.html', {'total_emission': total_emission})
    else:
        form = CarbonFootprintDataForm()

    return render(request, 'carbon_calculator.html', {'form': form})

def challenges_page(request):
    # You can add any logic here if needed
    return render(request, 'challenges_page.html')

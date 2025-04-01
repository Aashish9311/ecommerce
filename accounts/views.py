from django.shortcuts import render

# Create your views here.


from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, OTP
from .forms import LoginForm, OTPVerificationForm, UserRegistrationForm, UserProfileForm
from .utils import send_otp_email

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Generate OTP for MFA
                otp_code = OTP.generate_otp(user)
                
                # Send OTP via email
                try:
                    send_otp_email(user, otp_code)
                    messages.success(request, f"An OTP has been sent to your email address: {user.email}")
                except Exception as e:
                    messages.error(request, "Failed to send OTP email. Please try again.")
                    return redirect('login')
                
                # Store user ID in session for OTP verification
                request.session['user_id'] = user.id
                request.session['otp_sent'] = True
                
                # Redirect to OTP verification page
                return redirect('verify_otp')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def verify_otp_view(request):
    if 'user_id' not in request.session or not request.session.get('otp_sent'):
        return redirect('login')
        
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            user_id = request.session['user_id']
            
            try:
                user = User.objects.get(id=user_id)
                otp_obj = OTP.objects.filter(user=user, is_used=False).latest('created_at')
                
                if otp_obj.verify_otp(otp_code):
                    # OTP verified, log in the user
                    login(request, user)
                    
                    # Clean up session
                    del request.session['user_id']
                    del request.session['otp_sent']
                    
                    # Redirect based on user role
                    if user.is_seller():
                        return redirect('seller_dashboard')
                    else:
                        return redirect('buyer_dashboard')
                else:
                    messages.error(request, 'Invalid or expired OTP')
            except (User.DoesNotExist, OTP.DoesNotExist):
                messages.error(request, 'Something went wrong. Please try again.')
                return redirect('login')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'accounts/verify_otp.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def enable_mfa_view(request):
    if request.user.mfa_enabled:
        messages.info(request, 'Two-factor authentication is already enabled.')
        return redirect('profile')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            otp_obj = OTP.objects.filter(user=request.user, is_used=False).latest('created_at')
            
            if otp_obj.verify_otp(otp_code):
                request.user.mfa_enabled = True
                request.user.save()
                messages.success(request, 'Two-factor authentication has been enabled successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid or expired OTP code.')
    else:
        # Generate and send OTP
        otp_code = OTP.generate_otp(request.user)
        try:
            send_otp_email(request.user, otp_code)
            messages.success(request, f"An OTP has been sent to your email address: {request.user.email}")
        except Exception as e:
            messages.error(request, "Failed to send OTP email. Please try again.")
            return redirect('profile')
        
        form = OTPVerificationForm()
    
    return render(request, 'accounts/enable_mfa.html', {'form': form})

@login_required
def disable_mfa_view(request):
    if not request.user.mfa_enabled:
        messages.info(request, 'Two-factor authentication is already disabled.')
        return redirect('profile')
    
    if request.method == 'POST':
        request.user.mfa_enabled = False
        request.user.save()
        messages.success(request, 'Two-factor authentication has been disabled successfully.')
    
    return redirect('profile')
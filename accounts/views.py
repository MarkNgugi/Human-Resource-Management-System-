from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('dashboard')
#         else:
#             return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
#     return render(request, 'accounts/login.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
import pyotp

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['is_verified'] = False  # Mark session as not verified
            return redirect('verify_otp')  # Redirect to OTP verification
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

@login_required
def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        user = request.user
        totp = pyotp.TOTP(user.otp_secret)

        if totp.verify(otp):
            request.session['is_verified'] = True  # Mark session as verified
            messages.success(request, "OTP verified successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return render(request, 'accounts/verify_otp.html')

    return render(request, 'accounts/verify_otp.html')


def logout_view(request):
    logout(request)
    return redirect('login')
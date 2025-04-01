# # from django.db import models

# # Create your models here.



# from django.contrib.auth.models import AbstractUser
# from django.db import models
# import pyotp
# from datetime import datetime, timedelta
# from django.utils import timezone


# class User(AbstractUser):
#     BUYER = 'buyer'
#     SELLER = 'seller'
    
#     ROLE_CHOICES = [
#         (BUYER, 'Buyer'),
#         (SELLER, 'Seller'),
#     ]
    
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BUYER)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     is_phone_verified = models.BooleanField(default=False)
    
#     # MFA related fields
#     mfa_enabled = models.BooleanField(default=False)
#     mfa_secret = models.CharField(max_length=100, blank=True, null=True)
    
#     def is_buyer(self):
#         return self.role == self.BUYER
        
#     def is_seller(self):
#         return self.role == self.SELLER

# class OTP(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     otp_secret = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_used = models.BooleanField(default=False)
    
#     @classmethod
#     def generate_otp(cls, user):
#         # Generate a time-based OTP
#         secret = pyotp.random_base32()
#         totp = pyotp.TOTP(secret)
#         otp_code = totp.now()
        
#         # Save the OTP
#         otp_obj = cls.objects.create(
#             user=user,
#             otp_secret=secret
#         )
        
#         return otp_code
    
#     # def verify_otp(self, otp_code):
#     #     # Check if OTP is expired (10 minutes validity)
#     #     if datetime.now() > self.created_at + timedelta(minutes=10):
#     #         return False
            
#     #     # Check if OTP is already used
#     #     if self.is_used:
#     #         return False
            
#     #     # Verify the OTP
#     #     totp = pyotp.TOTP(self.otp_secret)
#     #     is_valid = totp.verify(otp_code)
        
#     #     if is_valid:
#     #         self.is_used = True
#     #         self.save()
            
#     #     return is_valid
#     class OTP(models.Model):
#         user = models.ForeignKey(User, on_delete=models.CASCADE)
#         otp = models.CharField(max_length=6)
#         created_at = models.DateTimeField(auto_now_add=True)

#         def __str__(self):
#             return f"{self.user.username} - {self.otp}"

#         def verify_otp(self, otp):
#             if timezone.now() > self.created_at + timedelta(minutes=10):
#                 return False
#             if self.otp == otp:
#                 return True
#             return False










# from django.db import models
# from django.contrib.auth.models import AbstractUser
# import pyotp
# from datetime import timedelta
# from django.utils import timezone


# class User(AbstractUser):
#     BUYER = 'buyer'
#     SELLER = 'seller'
    
#     ROLE_CHOICES = [
#         (BUYER, 'Buyer'),
#         (SELLER, 'Seller'),
#     ]
    
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BUYER)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     is_phone_verified = models.BooleanField(default=False)
    
#     # MFA related fields
#     mfa_enabled = models.BooleanField(default=False)
#     mfa_secret = models.CharField(max_length=100, blank=True, null=True)
    
#     def is_buyer(self):
#         return self.role == self.BUYER
        
#     def is_seller(self):
#         return self.role == self.SELLER

# class OTP(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     otp_secret = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_used = models.BooleanField(default=False)
    
#     @classmethod
#     def generate_otp(cls, user):
#         # Generate a time-based OTP
#         secret = pyotp.random_base32()
#         totp = pyotp.TOTP(secret)
#         otp_code = totp.now()
        
#         # Save the OTP
#         otp_obj = cls.objects.create(
#             user=user,
#             otp_secret=secret
#         )
        
#         return otp_code
    
#     def verify_otp(self, otp_code):
#         # Check if OTP is expired (10 minutes validity)
#         if timezone.now() > self.created_at + timedelta(minutes=10):
#             return False
            
#         # Check if OTP is already used
#         if self.is_used:
#             return False
            
#         # Verify the OTP
#         totp = pyotp.TOTP(self.otp_secret)
#         is_valid = totp.verify(otp_code)
        
#         if is_valid:
#             self.is_used = True
#             self.save()
            
#         return is_valid











from django.db import models
from django.contrib.auth.models import AbstractUser
import pyotp
from datetime import timedelta
from django.utils import timezone


class User(AbstractUser):
    BUYER = 'buyer'
    SELLER = 'seller'
    
    ROLE_CHOICES = [
        (BUYER, 'Buyer'),
        (SELLER, 'Seller'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=BUYER)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    
    # MFA related fields
    mfa_enabled = models.BooleanField(default=False)
    mfa_secret = models.CharField(max_length=100, blank=True, null=True)
    
    def is_buyer(self):
        return self.role == self.BUYER
        
    def is_seller(self):
        return self.role == self.SELLER

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    @classmethod
    def generate_otp(cls, user):
        # Generate a time-based OTP
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret)
        otp_code = totp.now()
        
        # Save the OTP
        otp_obj = cls.objects.create(
            user=user,
            otp_secret=secret
        )
        
        return otp_code
    
    def verify_otp(self, otp_code):
        # Check if OTP is expired (10 minutes validity)
        if timezone.now() > self.created_at + timedelta(minutes=10):
            return False
            
        # Check if OTP is already used
        if self.is_used:
            return False
            
        # Verify the OTP with a window to account for time drift
        totp = pyotp.TOTP(self.otp_secret)
        # Allow for a window of 1 interval before and after (30 seconds each way)
        is_valid = totp.verify(otp_code, valid_window=1)
        
        if is_valid:
            self.is_used = True
            self.save()
            
        return is_valid


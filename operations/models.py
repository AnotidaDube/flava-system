from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# 1. THE REP PROFILE
class RepProfile(models.Model):
    # This links the profile to the standard Django User login
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rep_profile')
    phone_number = models.CharField(max_length=20, help_text="Include country code, e.g., +26377...")
    has_whatsapp = models.BooleanField(default=True)
    security_deposit_balance = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending Review'),
        ('Approved', 'Hired - Account Created'),
        ('Rejected', 'Rejected')
    ]
    
    full_name = models.CharField(max_length=150)
    id_number = models.CharField(max_length=50, help_text="National ID Number")
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    age = models.IntegerField()
    marital_status = models.CharField(max_length=50, choices=[('Single', 'Single'), ('Married', 'Married'), ('Other', 'Other')])
    
    agreed_to_terms = models.BooleanField(default=False)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Application: {self.full_name} ({self.status})"

# 2. THE MORNING DISPATCH
class DailyDisbursement(models.Model):
    STATUS_CHOICES = [
        ('Active', 'In Field'),
        ('Settled', 'Settled'),
    ]
    rep = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    # New Field Logistics
    cart_number = models.CharField(max_length=20)
    current_area = models.CharField(max_length=100, help_text="Where are they today? e.g., Lundi Park")
    ice_packs = models.IntegerField()
    
    # Inventory Math
    carryover_units = models.IntegerField(default=0, help_text="Units brought back yesterday")
    new_units = models.IntegerField(help_text="Fresh units taken today")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_disbursements')

    @property
    def total_units_taken(self):
        """Automatically calculates the total inventory they are responsible for today"""
        return self.carryover_units + self.new_units

    def __str__(self):
        return f"{self.rep.username} | {self.current_area} | {self.date}"

# 3. THE EVENING SETTLEMENT (With the $100 Deposit Logic!)
class DailySettlement(models.Model):
    disbursement = models.OneToOneField(DailyDisbursement, on_delete=models.CASCADE)
    units_returned_unsold = models.IntegerField()
    units_damaged_melted = models.IntegerField()
    cash_remitted = models.DecimalField(max_digits=10, decimal_places=2)
    settled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='settlements_processed')
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # 1. Check if this is a brand new settlement being created
        is_new_settlement = self.pk is None 
        
        # 2. Save the settlement to the database first
        super().save(*args, **kwargs)
        
        # 3. If it's new, run your genius Security Deposit logic
        if is_new_settlement:
            profile = self.disbursement.rep.rep_profile
            
            # Auto-increment by $1.00 until it hits the $100 cap using strict Decimals
            if profile.security_deposit_balance < Decimal('100.00'):
                profile.security_deposit_balance += Decimal('1.00')
                profile.save()
            
            # Auto-update the morning sheet to 'Settled' so they can't be settled twice
            self.disbursement.status = 'Settled'
            self.disbursement.save()

    @property
    def expected_company_revenue(self):
        # The rep is billed for everything they didn't return cold and intact.
        # (Total taken - strictly unsold cold units) * $0.37 wholesale rate
        billable_units = self.disbursement.total_units_taken - self.units_returned_unsold
        return float(billable_units) * 0.37

    @property
    def discrepancy(self):
        # What they handed in vs What the math says they owe
        return float(self.cash_remitted) - self.expected_company_revenue

    def __str__(self):
        return f"Settlement for {self.disbursement.rep.username} on {self.disbursement.date}"
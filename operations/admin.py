import random
from django.contrib import admin, messages
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import DailyDisbursement, DailySettlement, RepProfile, JobApplication


# 1. Streamlined Rep Registration
class RepProfileInline(admin.StackedInline):
    model = RepProfile
    can_delete = False
    verbose_name_plural = 'Rep Configuration'

admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (RepProfileInline, )

# 2. Updated Disbursement Admin
@admin.register(DailyDisbursement)
class DailyDisbursementAdmin(admin.ModelAdmin):
    list_display = ('rep', 'date', 'cart_number', 'total_units_taken', 'status', 'issued_by')
    list_filter = ('status', 'date', 'rep', 'current_area')
    search_fields = ('rep__username', 'issued_by__username', 'cart_number', 'current_area')
    date_hierarchy = 'date'

# 3. Updated Settlement Admin
@admin.register(DailySettlement)
class DailySettlementAdmin(admin.ModelAdmin):
    list_display = (
        'get_rep_name', 'get_date', 'units_returned_unsold', 
        'units_damaged_melted', 'cash_remitted', 'expected_company_revenue', 'discrepancy'
    )
    list_filter = ('timestamp', 'settled_by')

    def get_rep_name(self, obj):
        return obj.disbursement.rep.username
    get_rep_name.short_description = 'Rep'
    get_rep_name.admin_order_field = 'disbursement__rep__username'

    def get_date(self, obj):
        return obj.disbursement.date
    get_date.short_description = 'Date'
    get_date.admin_order_field = 'disbursement__date'

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'application_date', 'status')
    list_filter = ('status', 'application_date')
    search_fields = ('full_name', 'id_number', 'phone_number')
    
    # Register the custom action
    actions = ['approve_and_generate_account']

    @admin.action(description="Hire Applicant: Generate Login & Rep Profile")
    def approve_and_generate_account(self, request, queryset):
        success_count = 0
        
        for app in queryset:
            # Prevent double-hiring
            if app.status == 'Approved':
                self.message_user(request, f"{app.full_name} is already hired!", level=messages.WARNING)
                continue

            try:
                # 1. Generate a clean username
                base_name = app.full_name.split()[0].lower().replace(r"[^a-zA-Z]", "")
                username = f"{base_name}{random.randint(10, 99)}"
                
                while User.objects.filter(username=username).exists():
                    username = f"{base_name}{random.randint(100, 999)}"

                # 2. PREDICTABLE PASSWORD: "Flava-" + the last 4 digits of their phone number!
                temp_password = f"Flava-{app.phone_number[-4:]}"

                # 3. Create User (Safely handling the optional email)
                new_user = User.objects.create_user(
                    username=username,
                    password=temp_password,
                    first_name=app.full_name.split()[0] 
                )
                
                if app.email:
                    new_user.email = app.email
                    new_user.save()

                # 4. Create Profile
                RepProfile.objects.create(
                    user=new_user,
                    phone_number=app.phone_number,
                    has_whatsapp=True 
                )

                # 5. Lock Application
                app.status = 'Approved'
                app.save()

                # 6. Show Popup AND Print to your Terminal!
                msg = f"✅ HIRED {app.full_name}! | Username: {username} | Password: {temp_password}"
                self.message_user(request, msg, level=messages.SUCCESS)
                
                # THIS PRINTS TO YOUR VS CODE TERMINAL SO YOU NEVER LOSE IT
                print("\n========================================================")
                print(msg)
                print("========================================================\n")
                
                success_count += 1
                
            except Exception as e:
                error_msg = f"Error processing {app.full_name}: {str(e)}"
                self.message_user(request, error_msg, level=messages.ERROR)
                print(f"CRITICAL ERROR: {error_msg}") # Prints error to terminal if it fails

        if success_count > 0:
            self.message_user(request, f"Successfully processed {success_count} new hires.", level=messages.SUCCESS)
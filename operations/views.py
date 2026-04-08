from rest_framework import viewsets
from .models import DailyDisbursement, DailySettlement, JobApplication, RepProfile
from .serializers import DailyDisbursementSerializer, DailySettlementSerializer
from django.http import JsonResponse
import json
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

# ViewSets for the API (Keep these as they are)
class DailyDisbursementViewSet(viewsets.ModelViewSet):
    queryset = DailyDisbursement.objects.all().order_by('-date')
    serializer_class = DailyDisbursementSerializer

class DailySettlementViewSet(viewsets.ModelViewSet):
    queryset = DailySettlement.objects.all().order_by('-timestamp')
    serializer_class = DailySettlementSerializer

# API to send live reps to the Vue Homepage
def active_radar_api(request):
    active_dispatches = DailyDisbursement.objects.filter(status='Active')
    radar_data = []
    for dispatch in active_dispatches:
        try:
            profile = dispatch.rep.rep_profile
            radar_data.append({
                "id": dispatch.id,
                "name": dispatch.rep.username,
                "area": dispatch.current_area,
                "phone": profile.phone_number,
                "hasWhatsapp": profile.has_whatsapp,
                "cartNumber": dispatch.cart_number,
                "avatar": f"https://ui-avatars.com/api/?name={dispatch.rep.username}&background=FF477E&color=fff&bold=true"
            })
        except Exception:
            continue
            
    return JsonResponse(radar_data, safe=False)

# API to handle User Login
@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful", "username": user.username})
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=400)

# API to fetch the logged-in rep's personal data
def api_my_dashboard(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized access"}, status=401)
    
    try:
        # SAFE FIX: Query the database directly instead of using Django's reverse relations
        profile = RepProfile.objects.get(user=request.user)
        active_shift = DailyDisbursement.objects.filter(rep=request.user, status='Active').last()
        
        data = {
            "name": request.user.username,
            "securityDepositBalance": float(profile.security_deposit_balance),
            "today": {
                "status": active_shift.status if active_shift else "No Active Shift",
                "unitsTaken": active_shift.total_units_taken if active_shift else 0,
                "wholesaleRate": 0.37,
            }
        }
        return JsonResponse(data)
    except Exception as e:
        # Prints the exact error to your terminal if it fails again
        print(f"DASHBOARD ERROR: {str(e)}") 
        return JsonResponse({"error": str(e)}, status=400)
    
# API to handle the "Join the Team" application form
@csrf_exempt
def api_submit_application(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Save the application
            application = JobApplication.objects.create(
                full_name=data.get('fullName'),
                id_number=data.get('idNumber'),
                phone_number=data.get('phone'),
                email=data.get('email', ''), 
                age=data.get('age'),
                marital_status=data.get('maritalStatus'),
                agreed_to_terms=data.get('agreedToTerms')
            )
            
            # Send the email if they provided one
            user_email = data.get('email')
            if user_email:
                office_address = "Mkoba road via Bristol next to Delta"
                subject = "Next Steps: Flava Ice Creams Application"
                message = f"Hi {application.full_name},\n\nThank you for applying to Flava Ice Creams!\n\nPlease bring your physical ID to our main office at {office_address} for verification."
                
                send_mail(
                    subject,
                    message,
                    'your_company_email@gmail.com', 
                    [user_email],
                    fail_silently=True
                )

            return JsonResponse({"message": "Application received successfully!"}, status=201)
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
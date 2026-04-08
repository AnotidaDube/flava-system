from rest_framework import serializers
from .models import DailyDisbursement, DailySettlement

class DailyDisbursementSerializer(serializers.ModelSerializer):
    # We can add a read-only field to show the rep's username instead of just their ID
    rep_name = serializers.ReadOnlyField(source='rep.username')
    issued_by_name = serializers.ReadOnlyField(source='issued_by.username')

    class Meta:
        model = DailyDisbursement
        fields = [
            'id', 'rep', 'rep_name', 'date', 'units_taken', 
            'status', 'issued_by', 'issued_by_name'
        ]

class DailySettlementSerializer(serializers.ModelSerializer):
    # Explicitly pull in our calculated properties as read-only fields
    units_sold = serializers.ReadOnlyField()
    expected_company_revenue = serializers.ReadOnlyField()
    discrepancy = serializers.ReadOnlyField()
    settled_by_name = serializers.ReadOnlyField(source='settled_by.username')

    class Meta:
        model = DailySettlement
        fields = [
            'id', 'disbursement', 'units_returned_unsold', 'units_damaged_melted',
            'cash_remitted', 'settled_by', 'settled_by_name', 'timestamp',
            'units_sold', 'expected_company_revenue', 'discrepancy'
        ]
from rest_framework import serializers
from .models import DailyLog

class DailyLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = DailyLog
        fields = ['id', 'user', 'user_name', 'date', 'yesterday', 'today', 'blockers', 'comments']
        read_only_fields = ['id', 'date']
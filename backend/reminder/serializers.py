from rest_framework import serializers

class AiAssistantSerializer(serializers.Serializer):
    assignment_name = serializers.CharField()
    due_date = serializers.DateField()
    
    
    
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AiAssistantSerializer
# Create your views here.
class AiAssistantApiView(APIView):
    def post(self,request):
        serializer = AiAssistantSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({"error":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        assignment_name = data.get('assignment_name')
        due_date = data.get('due_date')
        response = []
        students = [
            {
                "name": "Rahul",
                "email": "rahul@example.com",
                "submitted": False
            },
            {
                "name": "Anu",
                "email": "anu@example.com",
                "submitted": True
            },
            {
                "name": "Arjun",
                "email": "arjun@example.com",
                "submitted": False
            }
        ]
        for student in students:
            if student['submitted'] == False:
                response.append({"name":student['name'],"email":student['email']})
                   
        return Response({
            "assignment_name":assignment_name,
            "due_date":due_date,
            "pending_students":response
        },status=status.HTTP_200_OK)
    

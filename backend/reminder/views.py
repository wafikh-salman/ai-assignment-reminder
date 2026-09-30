from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AiAssistantSerializer
from .services import process_pending_students
from datetime import date
# Create your views here.
class AiAssistantApiView(APIView):
    def post(self,request):
        serializer = AiAssistantSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({"error":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        assignment_name = data.get('assignment_name')
        due_date = data.get('due_date')
        
        if due_date < date.today():
            return Response({
                "error":"Due date is already passed"
            })
    
    
        response = []
        students = [
            {
                "name": "Rahul",
                "email": "wafikhsalman07@gmail.com",
                "submitted": False
            },
            {
                "name": "Anu",
                "email": "wafikhsalman07@gmai.com",
                "submitted": True
            },
            {
                "name": "Arjun",
                "email": "wafikhsalman07@gmail.com",
                "submitted": False
            }
        ]
        for student in students:
            if student['submitted'] == False:
                response.append({"name":student['name'],"email":student['email']})
        results = process_pending_students(
        response,
        assignment_name,
        due_date
    )          
        return Response({
    "assignment_name": assignment_name,
    "due_date": due_date,
    "results": results
},status=status.HTTP_200_OK)
    

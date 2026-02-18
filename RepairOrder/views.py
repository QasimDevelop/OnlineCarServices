from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateJobCardSerializer , JobCardListSerializer
from .models import JobCard, Vehicle

class CreateJobCardView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateJobCardSerializer(data=request.data)
        if serializer.is_valid():
            jobcard = serializer.save()
            return Response({"message": "Job Card created successfully", "jobcard_id": jobcard.JobCardID}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AllJobCardsView(APIView):
    def get(self, request, *args, **kwargs):
        jobcards = JobCard.objects.all()
        serializer = JobCardListSerializer(jobcards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

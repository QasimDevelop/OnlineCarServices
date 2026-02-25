from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CreateJobCardSerializer , JobCardListSerializer  , JobConcernSerializer, TechnicianSerializer, CreateTaskTechnicianSerializer
from .models import JobCard, Vehicle , JobConcern 

from accounts.models import Appointment , Employee , UserRole , Roles , User

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

class JobCardAssignDataView(APIView):
    #permission_classes = [IsAuthenticated] 

    def get(self, request, jobcard_id):
        try:
            job_card = JobCard.objects.get(pk=jobcard_id)
        except JobCard.DoesNotExist:
            return Response({'error': 'JobCard not found'}, status=404)

        job_concerns = JobConcern.objects.filter(JobCardID=job_card)
        # Assuming JobCard has a ServiceStation or BranchName field to filter technicians
        technicians = Employee.objects.filter(User__userrole__Role__RoleID=1,
                                              IsActive = True).distinct()

        return Response({
            'job_card': JobCardListSerializer(job_card).data,
            'job_concerns': JobConcernSerializer(job_concerns, many=True).data,
            'technicians': TechnicianSerializer(technicians, many=True).data,
        })
class JobCardAssignTechnicianView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateTaskTechnicianSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            tasktechnician = serializer.save()
            return Response(
                {
                    "message": "Task assigned successfully",
                    "JobCardID": tasktechnician.JobCardID.JobCardID
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
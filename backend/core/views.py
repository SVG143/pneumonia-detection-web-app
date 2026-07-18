from rest_framework import generics,permissions,status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User,Analysis,Review
from .serializers import UserSerializer,RegisterSerializer,AnalysisSerializer,ReviewSerializer
from .ml import predict,ModelUnavailable

class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all(); serializer_class=RegisterSerializer; permission_classes=[permissions.AllowAny]

@api_view(['GET'])
def me(request): return Response(UserSerializer(request.user).data)

class AnalysisListCreate(generics.ListCreateAPIView):
    serializer_class=AnalysisSerializer
    def get_queryset(self):
        return Analysis.objects.all().select_related('patient').order_by('-created_at') if self.request.user.role in ['doctor','admin'] else Analysis.objects.filter(patient=self.request.user).order_by('-created_at')
    def perform_create(self,serializer):
        analysis=serializer.save(patient=self.request.user)
        try:
            label,confidence,version=predict(analysis.image.path)
            analysis.predicted_class=label; analysis.confidence=confidence; analysis.model_version=version; analysis.status='complete'
        except ModelUnavailable:
            analysis.status='failed'
        analysis.save()

@api_view(['POST'])
def review_analysis(request,pk):
    if request.user.role not in ['doctor','admin'] or not request.user.is_approved: return Response({'detail':'Approved doctor access required'},status=403)
    analysis=generics.get_object_or_404(Analysis,pk=pk)
    serializer=ReviewSerializer(data=request.data); serializer.is_valid(raise_exception=True)
    review,_=Review.objects.update_or_create(analysis=analysis,defaults={'doctor':request.user,'notes':serializer.validated_data['notes']})
    return Response(ReviewSerializer(review).data)

@api_view(['GET','PATCH'])
def users(request):
    if request.user.role!='admin': return Response({'detail':'Admin access required'},status=403)
    if request.method=='PATCH':
        user=generics.get_object_or_404(User,pk=request.data.get('id')); user.is_approved=bool(request.data.get('is_approved')); user.save()
    return Response(UserSerializer(User.objects.exclude(pk=request.user.pk),many=True).data)

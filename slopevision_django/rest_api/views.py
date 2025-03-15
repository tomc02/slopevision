from datetime import datetime, timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from .models import Place, Webcam, WebcamHistory
from .serializers import PlaceSerializer, WebcamSerializer, WebcamHistorySerializer, UserSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)  # Authenticate user
    if user is None:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

    # Log the user into Django's session
    login(request, user)
    token, created = Token.objects.get_or_create(user=user)

    return Response({'token': token.key, 'user': UserSerializer(user).data})


@api_view(['POST'])
def registration_view(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def user_view(request):
    print(request.user)
    return Response(UserSerializer(request.user).data)
   


@extend_schema_view(
    list=extend_schema(
        description="Retrieve all places.",
        responses={200: PlaceSerializer(many=True)}
    ),
    retrieve=extend_schema(
        description="Retrieve a specific place by its ID.",
        responses={200: PlaceSerializer}
    ),
)
class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    @extend_schema(
        description="Retrieve all webcams associated with a specific place.",
        responses={200: WebcamSerializer(many=True)}
    )
    @action(detail=True, methods=['get'], url_path='webcams')
    def get_webcams(self, request, pk=None):
        """
        Custom action to get webcams associated with a specific place.
        """
        place = self.get_object()  # Get the place by its `pk`
        webcams = place.webcams.all()  # Get all webcams for that place
        return Response(WebcamSerializer(webcams, many=True).data)


@extend_schema_view(
    list=extend_schema(
        description="Retrieve all webcams.",
        responses={200: WebcamSerializer(many=True)}
    ),
    retrieve=extend_schema(
        description="Retrieve a specific webcam by its ID.",
        responses={200: WebcamSerializer}
    ),
)
class WebcamViewSet(viewsets.ModelViewSet):
    queryset = Webcam.objects.all()
    serializer_class = WebcamSerializer

    @extend_schema(
        description="Retrieve the history of a specific webcam.",
        responses={
            200: OpenApiResponse(
                description="A list of webcam history snapshots with timestamps.",
                response=WebcamHistorySerializer(many=True)
            ),
            400: OpenApiResponse(description="Bad request if the date format is invalid."),
        }
    )
    @action(detail=True, methods=['get'], url_path='history')
    def get_history(self, request, pk=None):
        """
        Custom action to get the history of a specific webcam.
        """
        webcam = self.get_object()

        # if ?date=2021-10-01 is provided, filter by that date
        date = request.query_params.get('date')
        # if ?times=true is provided, return only available times for that date
        times = request.query_params.get('times')
        if date:
            start_date = datetime.strptime(date, "%Y-%m-%d")
            end_date = start_date + timedelta(days=1)
            history = WebcamHistory.objects.filter(
                webcam=webcam,
                timestamp__gte=start_date,
                timestamp__lt=end_date
            ).order_by('-timestamp')
            if times:
                available_times = history.values_list('timestamp', flat=True)
                response_data = {
                    str(time.time())[:5]: time for time in available_times}
            else:
                response_data = WebcamHistorySerializer(
                    history, many=True).data
            return Response(response_data)
        else:
            # If no date is provided, return all history
            history = WebcamHistory.objects.filter(
                webcam=webcam).order_by('-timestamp')

        return Response(WebcamHistorySerializer(history, many=True).data)


@extend_schema_view(
    list=extend_schema(
        description="Retrieve all webcam history records.",
        responses={200: WebcamHistorySerializer(many=True)}
    ),
    retrieve=extend_schema(
        description="Retrieve a specific webcam history by its ID.",
        responses={200: WebcamHistorySerializer}
    ),
)
class WebcamHistoryViewSet(viewsets.ModelViewSet):
    queryset = WebcamHistory.objects.all()
    serializer_class = WebcamHistorySerializer

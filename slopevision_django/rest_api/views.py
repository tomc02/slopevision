from datetime import datetime, timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from .models import CustomUser, Place, Webcam, WebcamHistory
from .serializers import PlaceSerializer, WebcamSerializer, WebcamHistorySerializer
from dj_rest_auth.views import UserDetailsView
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from .management.commands import fetch_video_urls, fetch_hzs_images, save_history
import threading

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
                response_data = {str(time.time())[:5]: time for time in available_times}
            else:
                response_data = WebcamHistorySerializer(history, many=True).data
            return Response(response_data)
        else:
            # If no date is provided, return all history
            history = WebcamHistory.objects.filter(webcam=webcam).order_by('-timestamp')

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

@extend_schema_view(
    list=extend_schema(
        description="Retrieve the details of the authenticated user.",
        responses={200: CustomUserSerializer}
    )
)
class CustomUserDetailsView(UserDetailsView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access
    serializer_class = CustomUserSerializer  # Use your custom serializer

@extend_schema(
    description="Retrieve a CSRF token for the current session.",
    responses={200: OpenApiResponse(description="CSRF token for the session.")}
)
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrfToken': token})


class AddFavoritePlaceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, place_id):
        user = request.user
        try:
            place = Place.objects.get(pk=place_id)
            user.favorite_places.add(place)
            return Response({'status': 'Place added to favorites'}, status=status.HTTP_200_OK)
        except Place.DoesNotExist:
            return Response({'error': 'Place not found'}, status=status.HTTP_404_NOT_FOUND)


class RemoveFavoritePlaceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, place_id):
        user = request.user
        try:
            place = Place.objects.get(pk=place_id)
            user.favorite_places.remove(place)
            return Response({'status': 'Place removed from favorites'}, status=status.HTTP_200_OK)
        except Place.DoesNotExist:
            return Response({'error': 'Place not found'}, status=status.HTTP_404_NOT_FOUND)
        
class FetchWebcamDataView(APIView):
    def post(self, request):
        # Execute the task synchronously
        fetch_video_urls.Command().handle()
        # fetch_hzs_images.Command().handle()

        return Response({'status': 'Webcam data fetching completed'}, status=status.HTTP_200_OK)


class SaveHistoryView(APIView):
    def post(self, request):
        # Execute the task synchronously
        save_history.Command().handle()

        return Response({'status': 'History saving completed'}, status=status.HTTP_200_OK)

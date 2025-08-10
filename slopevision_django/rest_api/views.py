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
from django.http import HttpResponseForbidden, JsonResponse
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from .management.commands import fetch_video_urls, fetch_hzs_images, save_history
from django.db.models import Prefetch
import requests
import urllib.parse
import mimetypes
from django.http import HttpResponse, HttpResponseBadRequest

ALLOWED_PROXY_DOMAINS = ['meteo.hzs.sk'] 

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
    serializer_class = PlaceSerializer
    queryset = Place.objects.all().prefetch_related(
        Prefetch('webcams', queryset=Webcam.objects.select_related('latest_history').order_by('id').filter(is_active=True))
    )

    @extend_schema(
        description="Retrieve all webcams associated with a specific place.",
        responses={200: WebcamSerializer(many=True)}
    )
    @action(detail=True, methods=['get'], url_path='webcams')
    def get_webcams(self, request, pk=None):
        place = self.get_object()
        webcams = place.webcams.all()
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
    queryset = Webcam.objects.all().filter(is_active=True)
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
        try:
            webcam_id = int(pk)
        except (TypeError, ValueError):
            return Response({"detail": "Invalid webcam ID."}, status=400)

        date_str = request.query_params.get('date')
        times_only = request.query_params.get('times') is not None

        filters = {'webcam_id': webcam_id}
        if date_str:
            try:
                start = datetime.strptime(date_str, "%Y-%m-%d")
                end = start + timedelta(days=1)
                filters['timestamp__gte'] = start
                filters['timestamp__lt'] = end
            except ValueError:
                return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        queryset = WebcamHistory.objects.filter(**filters).order_by('-timestamp')

        if times_only:
            timestamps = queryset.values_list('timestamp', flat=True)
            response_data = {ts.strftime('%H:%M'): ts for ts in timestamps}
            return Response(response_data)

        # Optimize by deferring potentially heavy fields if not needed
        queryset = queryset.select_related('webcam').only('id', 'timestamp', 'image', 'video', 'webcam_id')

        serializer = WebcamHistorySerializer(queryset, many=True)
        return Response(serializer.data)


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

def proxy_image(request):
    url = request.GET.get("url")
    if not url:
        return HttpResponseBadRequest("Missing 'url' parameter.")

    # Check if the URL is allowed
    if not any(domain in url for domain in ALLOWED_PROXY_DOMAINS):
        return HttpResponseForbidden("URL is not allowed.")

    try:
        # Decode URL if it's URL-encoded
        url = urllib.parse.unquote(url)

        # Fetch image while ignoring SSL certificate errors
        resp = requests.get(url, verify=False, stream=True, timeout=10)
        resp.raise_for_status()

        # Guess content type from headers or file extension
        content_type = resp.headers.get("Content-Type")
        if not content_type:
            content_type, _ = mimetypes.guess_type(url)
            if not content_type:
                content_type = "application/octet-stream"

        # Return image data
        return HttpResponse(resp.content, content_type=content_type)

    except Exception as e:
        return HttpResponseBadRequest(f"Error fetching image: {e}")

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
        fetch_hzs_images.Command().handle()

        return Response({'status': 'Webcam data fetching completed'}, status=status.HTTP_200_OK)


class SaveHistoryView(APIView):
    def post(self, request):
        # Execute the task synchronously
        save_history.Command().handle()

        return Response({'status': 'History saving completed'}, status=status.HTTP_200_OK)

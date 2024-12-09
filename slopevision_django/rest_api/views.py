from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from .models import Place, Webcam, WebcamHistory
from .serializers import PlaceSerializer, WebcamSerializer, WebcamHistorySerializer


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
        if date:
            # Filter by the provided date and order by timestamp
            history = WebcamHistory.objects.filter(webcam=webcam, timestamp__date=date).order_by('-timestamp')
            # Return only available times for that date
            return Response({str(h.timestamp.time())[:5]: h.timestamp for h in history})
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

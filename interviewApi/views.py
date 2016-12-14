from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, EvaluationSerializer
from .exception import InterviewAPIException
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from timed_auth_token.authentication import TimedAuthTokenAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Evaluation
from .libs import get_all_evaluation


'''class LoginUser(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )
    authentication_classes = (BasicAuthentication,)

    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        credentials = libs.utils.login_user(request, email, password)

        if credentials is not None:
            return Response(credentials, status=status.HTTP_200_OK)
        raise InterviewAPIException(code=status.HTTP_403_FORBIDDEN, detail='Authentication failed') '''


class ListCreateEvaluation(generics.GenericAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TimedAuthTokenAuthentication,)

    def post(self, request):
        data = request.data
        synced_records = []

        for record in data:
            id = record['remote_id']
            serializer = self.get_serializer(data=record)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # cache successfully saved record to be sent in response
            synced_records.append(id)

        return Response(synced_records, status=status.HTTP_201_CREATED)

    def get(self, request):
        permission_classes= (IsAuthenticated, )
        authentication_classes = (TimedAuthTokenAuthentication,)
        serializer_class = EvaluationSerializer

        serializer = self.get_serializer(self.get_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        return get_all_evaluation()


class RetrieveEvaluation(generics.GenericAPIView):
    serializer_class = EvaluationSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TimedAuthTokenAuthentication,)

    def get_item(self, id):
        try:
            return Evaluation.objects.get(pk=id)
        except Evaluation.DoesNotExist as e:
            return Response({"detail": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        evaluation = self.get_item(id)
        serializer = self.get_serializer(evaluation)

        return Response(serializer.data, status=status.HTTP_200_OK)







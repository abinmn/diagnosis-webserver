from rest_framework.authtoken.models import Token
from api.serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from api.models import Endpoint_Check
import time
from api.compute_results import *


class UserCreate(APIView):
    """ 
    Creates the user. 
    """

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # check if conditions in serialize.UserSerializer is valid
            user = serializer.save()
            print(user)
            # Check if user was created
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    """
    Create or update user heigth
    """

    def post(self, request, format='json'):
        serializer = ProfileSerializer(data=request.data, context={
                                       "request": self.request})
        print(request.data)
        if serializer.is_valid():
            profile = serializer.save(user=self.request.user)

            if profile:
                json = {"status": True}
                print(json)
                return Response(json, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserData(generics.ListAPIView):
#     serializer_class = DataSerializer

#     def get_queryset(self):
#         user = self.request.user
#         try:
#             data = user.data_set.order_by('-created_at')
#         except:
#             return {"status":False}

#         return data


class UserData(generics.ListAPIView):
    serializer_class = DataSerializer

    def get_queryset(self):
        user = self.request.user
        pk = user.pk #object id

        #Inform arduino - write permission
        endpoint = Endpoint_Check.objects.get(pk=1)
        endpoint.status = True
        endpoint.user = pk
        endpoint.save()

        #Loop exit - when arduino write the data to database
        while (Endpoint_Check.objects.get(pk=1).status):
            continue
        try:
            #get the list of records
            queryset = user.data_set.order_by('-created_at')
        except:
            return {"status": False}

        return queryset


class SerialData(APIView):

    def post(self, request):
        endpoint = Endpoint_Check.objects.get(pk=1)
        #endpoint.status = True -> can write to database
        if not endpoint.status:
            print("Not allowed  ")
            return Response("Not Allowed", status=status.HTTP_403_FORBIDDEN)

        #Serial Data from Arduino
        data = self.request.data

        pk = endpoint.user
        user = User.objects.get(pk=pk)
        height = user.profile_set.all()[0].height
        results = get_result(height, data)

        #To save result to database blue-column name and white-value
        d = Data(user=user, bpm=results['bpm'], cardiac_output=results['cardiac_output'], stroke_volume=results['stroke'], estimated_delta=results['delta'],
                 stiffness_index=results['stiffness_index'],  augmented_index=results['augmented_index'], pulse_wave_velocity=results['pulse_wave_velocity'], plot='graph/'+results['filename']
                 )
        d.save()
        endpoint.status = False
        endpoint.save()
        print("data saved")
        return Response("Hello Arduino", status=status.HTTP_200_OK)

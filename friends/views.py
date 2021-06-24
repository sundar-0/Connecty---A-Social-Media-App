from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets,generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from . models import FriendRequest
from . serializers import FriendRequestSerializer
from rest_framework import permissions
from rest_framework.decorators import action
from user_profile.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer
from django.http import Http404, request
from rest_framework import status
from rest_framework.parsers import JSONParser

# Create your views here.


class FriendViewSet(viewsets.ViewSet):
    """
    Friends
    """
    parser_classes = [JSONParser]
    permission_classes=[permissions.IsAuthenticated,IsOwnerOrReadOnly]
    def get_queryset(self):
        user=self.request.user.pk
        q1=FriendRequest.objects.filter(request_from=user,status='Accepted')
        q2=FriendRequest.objects.filter(request_to=user,status='Accepted')
        result=[]
        if q1.exists and not q2.exists:
            for i in range(len(q1.values())):
                result.append(q1.values()[i]['request_to_id'])
        elif not q1.exists and q2.exists:
            for i in range(len(q2.values())):
                result.append(q2.values()[i]['request_from_id'])
        elif q1.exists and q2.exists:
            for i in range(len(q1.values())):
                result.append(q1.values()[i]['request_to_id'])
            for i in range(len(q2.values())):
                result.append(q2.values()[i]['request_from_id'])
        else:
            pass  
        friends=User.objects.filter(id__in=result).values()
        return friends

    def get_object(self,pk):
        user=self.request.user.pk
        try:
            friend=FriendRequest.objects.filter(request_from=user,request_to=pk)
            if self.request.method=='GET': 
                if friend.exists(): 
                    friend_id=friend.values()[0]['request_to_id']
                    return User.objects.get(pk=friend_id)
            elif self.request.method=='PUT' or self.request.method=='DELETE':
                return friend
            
        except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        friends=self.get_queryset()
        serializer = UserSerializer(friends, many=True)
        return Response(serializer.data)

    def create(self, request):

        request.data['_mutable']=True
        request.data['request_from']=self.request.user.pk
        request.data['_mutable']=False
        already_friend=FriendRequest.objects.filter(request_from=request.data['request_from'],request_to=request.data['request_to'],status='Accepted').exists()
        already_sent=FriendRequest.objects.filter(request_from=request.data['request_from'],request_to=request.data['request_to'],status='pending').exists()

        if already_friend:

            return Response({"message":"You are already friend.."})
        elif already_sent:

            return Response({"message":"You have already sent friend request to this person.."})
        else:

            serializer = FriendRequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        

    def retrieve(self, request, pk=None):
        friend= self.get_object(pk)
        serializer = UserSerializer(friend)
        return Response(serializer.data)
        

    def update(self, request, pk=None):
        friend=self.get_object(pk)
        serializer=FriendRequestSerializer(friend,data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        friend=self.get_object(pk)
        friend.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



    @action(detail=False,methods=['GET'])
    def find_friends(self,request):
        user=self.request.user.pk
        q1=FriendRequest.objects.filter(request_from=user,status='Accepted')
        q2=FriendRequest.objects.filter(request_to=user,status='Accepted')
        result=[user]
        if q1.exists and not q2.exists:
            for i in range(len(q1.values())):
                result.append(q1.values()[i]['request_to_id'])
        elif not q1.exists and q2.exists:
            for i in range(len(q2.values())):
                result.append(q2.values()[i]['request_from_id'])
        elif q1.exists and q2.exists:
            for i in range(len(q1.values())):
                result.append(q1.values()[i]['request_to_id'])
            for i in range(len(q2.values())):
                result.append(q2.values()[i]['request_from_id'])
        else:
            pass     
        find_friends=User.objects.exclude(id__in=result)
        serializer = UserSerializer(find_friends, many=True)
        return Response(serializer.data)


    @action(detail=False,methods=['GET'])
    def incoming_requests(self,request):
        incoming_requests= FriendRequest.objects.filter(request_to=self.request.user,status='pending')
        if incoming_requests.exists():
            request_from_users=[]
            for i in range(len(incoming_requests.values())):
                request_from_users.append(incoming_requests.values()[i]['request_from_id'])
            pending=User.objects.filter(id__in=request_from_users).values()
            serializer = UserSerializer(pending, many=True)
            return Response(serializer.data)
        else:
            return Response({"message":"You have no any incoming requests"})


    @action(detail=True,methods=['PUT'],name='Accept Friend Request')
    def friendrequests(self,request,pk):
        print(pk)
        incoming_request=FriendRequest.objects.filter(request_to=self.request.user,request_from=pk,status='pending').get()
        print(incoming_request)
        serializer=FriendRequestSerializer(incoming_request,data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data)    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @friendrequests.mapping.delete
    def delete_request(self,request,pk):
        print(pk)
        try:
            incoming_request= FriendRequest.objects.filter(request_to=self.request.user,request_from=pk,status='pending')
            print(incoming_request)
            incoming_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



    @action(detail=False,methods=['GET'])
    def sent_requests(self,request):
        sent_requests= FriendRequest.objects.filter(request_from=self.request.user,status='pending')
        print(sent_requests)
        if sent_requests.exists():
            request_to_users=[]
            for i in range(len(sent_requests.values())):
                request_to_users.append(sent_requests.values()[i]['request_to_id'])
            pending=User.objects.filter(id__in=request_to_users).values()
            serializer = UserSerializer(pending, many=True)
            return Response(serializer.data)
        else:
            return Response({"message":"No sent Requests Found!!!"})

    @action(detail=True,methods=['DELETE'])
    def undo_request(self,request,pk):
        try:
            sent_request= FriendRequest.objects.filter(request_from=self.request.user,request_to=pk,status='pending')
            sent_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



        
        












      
        
    







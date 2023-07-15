# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Group 
from .serializers import UserSerializer, GroupSerializer, MessageSerializer, GroupMessageSerializer
from .schema import schema

# get users and create users
class UserAPIView(APIView):

    def get(self, request):        
        username = User.objects.all()
        serializer = UserSerializer(username, many=True)        
        return Response(serializer.data)

    def post(self, request):        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

# get groups and create groups
class GroupAPIView(APIView):

    def get(self, request):        
        groupname = Group.objects.all()
        serializer = GroupSerializer(groupname, many=True)        
        return Response(serializer.data)

    def post(self, request):        
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    



# # one to one message
# class UserSendMessageAPIView(APIView):
#     def post(self, request):
#         serializer = MessageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


# # group message
# class UserSendGroupMessageAPIView(APIView):
#     def post(self, request):
#         serializer = GroupMessageSerializer(data=request.data)
#         if serializer.is_valid():
#             group = serializer.validated_data['group']            
#             sender = serializer.validated_data['sender']            
#             group = Group.objects.get(name = group)            
#             if sender in group.members.all():
#                 serializer.save()
#                 return Response(serializer.data, status=201)
#             else:
#                 return Response({'error': 'Only group members can send messages to the group.'}, status=403)
#         return Response(serializer.errors, status=400)



# one to one message
class SendMessageAPIView(APIView):
    def post(self, request):
        sender_name = request.data.get('sender')
        recipient_name = request.data.get('recipient')
        content = request.data.get('content')
        
        query = '''
            mutation {
                createMessage(senderName: "%s", recipientName: "%s", content: "%s") {
                    success
                    message {
                        id
                        sender {
                            id
                            username
                        }
                        recipient {
                            id
                            username
                        }
                        content
                    }
                }
            }
        ''' % (sender_name, recipient_name, content)

        result = schema.execute(query)
        if result.errors:
            return Response({'errors': [str(error) for error in result.errors]}, status=400)
        
        return Response(result.data['createMessage'])


# group message
class SendGroupMessageAPIView(APIView):
    def post(self, request):        
        sender_name = request.data.get('sender')        
        group_name = request.data.get('group')
        content = request.data.get('content')
        
        query = '''
            mutation {
                createGroupmessage(senderName: "%s", groupName: "%s", content: "%s") {
                    success
                    message {
                        id
                        sender {
                            id
                            username
                        }
                        group {
                            id
                            name
                        }
                        content
                    }
                }
            }
        ''' % (sender_name, group_name, content)

        sender = User.objects.get(username = sender_name)
        group = Group.objects.get(name = group_name)
        member = group.members.all()        
        if sender in group.members.all():
            result = schema.execute(query)
            if result.errors:
                return Response({'errors': [str(error) for error in result.errors]}, status=400)
            return Response(result.data['createGroupmessage'])
        else:
            return Response({'error': 'Only group members can send messages to the group.'}, status=403)
        
        
        
# user received message
class UserReceivedMessagesAPIView(APIView):
    def get(self, request, username):
        query = '''
            query {
                userRecievedmessages(username: "%s") {                    
                    sender {                        
                        username
                    }                    
                    content
                }
            }
        ''' % username
        
        result = schema.execute(query)        
        if result.errors:            
            return Response({'errors': [str(error) for error in result.errors]}, status=400)
        
        return Response(result.data['userRecievedmessages'])
    

# user received group message
class UserReceivedGroupMessagesAPIView(APIView):
    def get(self, request, username):
        query = '''
            query {
                userRecievedgroupmessages(username: "%s") {                    
                    group {                        
                        name
                    }
                    sender {                        
                        username
                    }                    
                    content
                }
            }
        ''' % username
        
        result = schema.execute(query)
        # print(result)
        if result.errors:
            return Response({'errors': [str(error) for error in result.errors]}, status=400)
        
        return Response(result.data['userRecievedgroupmessages'])

















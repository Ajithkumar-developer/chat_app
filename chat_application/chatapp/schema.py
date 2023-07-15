
import graphene
from graphene_django import DjangoObjectType
from .models import User, Group, Message,GroupMessage

# types

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'

class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        fields = '__all__'

class MessageType(DjangoObjectType):
    class Meta:
        model = Message
        fields = '__all__'

class GroupMessageType(DjangoObjectType):
    class Meta:
        model = GroupMessage
        fields = '__all__'


# Query
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_groups = graphene.List(GroupType)
    all_messages = graphene.List(MessageType)
    all_groupMessages = graphene.List(GroupMessageType)
    user_recievedMessages = graphene.List(MessageType, username = graphene.String(required=True))
    user_recievedGroupMessages = graphene.List(GroupMessageType, username = graphene.String(required=True))    
    

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_all_groups(self, info):        
        return Group.objects.all()

    def resolve_all_messages(self, info):
        return Message.objects.all()
    
    def resolve_all_groupMessages(self, info):
        return GroupMessage.objects.all()
    
    # recieved message
    def resolve_user_recievedMessages(self, info, username):
        recipient = User.objects.get(username= username)        
        messages = Message.objects.filter(recipient=recipient)     

        return messages

    # recieved group message
    def resolve_user_recievedGroupMessages(self, info, username):
        recipient = User.objects.get(username=username)        
        group_messages = []
        groups = Group.objects.filter(members=recipient)
        for group in groups:            
            group_messages.extend(GroupMessage.objects.filter(group=group))                        

        return group_messages


# message mutation
class CreateMessageMutation(graphene.Mutation):
    message = graphene.Field(MessageType)
    success = graphene.Boolean()

    class Arguments:
        sender_name = graphene.String(required=True)
        recipient_name = graphene.String(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, sender_name, recipient_name, content):
        sender = User.objects.get(username=sender_name)
        recipient = User.objects.get(username=recipient_name)
        message = Message(sender=sender, recipient=recipient, content=content)
        message.save()
        return CreateMessageMutation(success=True, message=message)


# group message mutation
class CreateGroupMessageMutation(graphene.Mutation):
    message = graphene.Field(GroupMessageType)
    success = graphene.Boolean()

    class Arguments:
        sender_name = graphene.String(required=True)
        group_name = graphene.String(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, sender_name, group_name, content):
        sender = User.objects.get(username=sender_name)
        group = Group.objects.get(name=group_name)                
        message = GroupMessage(sender=sender, group=group, content=content)
        message.save()
        return CreateGroupMessageMutation(success=True, message=message)
        
        
        
# mutation
class Mutation(graphene.ObjectType):
    create_message = CreateMessageMutation.Field()
    create_groupmessage = CreateGroupMessageMutation.Field()



    
schema = graphene.Schema(query=Query, mutation=Mutation)

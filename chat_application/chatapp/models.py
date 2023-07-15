from django.db import models

# user model
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.username

# group model
class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(User, related_name='groups')
    
    def __str__(self):
        return self.name 

# message model
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"From: {self.sender} To: {self.recipient} Message: {self.content}"

# group message model
class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Group: {self.group} Sender: {self.sender} Message: {self.content}"

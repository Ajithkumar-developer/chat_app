from django.contrib import admin
from .models import User, Group, Message, GroupMessage

class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
        fields = '__all__'

class GroupAdmin(admin.ModelAdmin):
    class Meta:
        model = Group
        fields = '__all__'

class MessageAdmin(admin.ModelAdmin):
    class Meta:
        model = Message
        fields = '__all__'

class GroupMessageAdmin(admin.ModelAdmin):
    class Meta:
        model = GroupMessage
        fields = '__all__'

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(GroupMessage, GroupMessageAdmin)
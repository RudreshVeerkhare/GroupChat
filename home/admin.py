from django.contrib import admin
from .models import Group, Messages, Profile, GroupProfile

# To register group on admin page
admin.site.register(Group)

# To register Messages on admin page
admin.site.register(Messages)

# To register profile model
admin.site.register(Profile)

# To register group_profile model
admin.site.register(GroupProfile)

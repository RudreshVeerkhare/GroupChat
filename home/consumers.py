from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Messages, Group


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        self.count = 0
        return super().__init__(*args, **kwargs)

    def fetch_old_messages(self, data):
        grp_name = data["grp_name"]
        messages = Group.last_10_messages(grp_name, times=self.count)
        if messages:
            self.count += 1
        else:
            self.count -= 1
            messages = Group.last_10_messages(grp_name, times=self.count)

        content = {"command": "messages", "messages": self.messages_to_json(messages)}
        self.send_message(content)

    def fetch_messages(self, data):
        self.count = 0
        grp_name = data["grp_name"]
        messages = Group.last_10_messages(grp_name, self.count)
        content = {"command": "messages", "messages": self.messages_to_json(messages)}
        self.send_message(content)

    def fetch_groups(self, data):
        user_name = data["username"]
        user = User.objects.get(username=user_name)
        groups = user.all_groups.all()
        content = {
            "command" : "groups",
            "groups" : self.groups_to_json(groups),
        }
        self.send_message(content)
    
    def groups_to_json(self, groups):
        results = []
        for group in groups:
            last_msg = group.messages.last()
            results.append({
                "group_name" : group.group_name,
                "profile_pic" : group.group_profile.image.url,
                "last_msg" : f"{last_msg.parent_user.username + ' : ' + last_msg.message_text if last_msg else ''}",
            })
        return results

    def new_message(self, data):
        author = data["from"]
        grp_name = data["grp_name"]
        parent_user = User.objects.get(username=author)
        parent_group = Group.objects.get(group_name=grp_name)
        message = Messages.objects.create(
            parent_group=parent_group,
            parent_user=parent_user,
            message_text=data["message"],
        )
        content = {"command": "new_message", "message": self.message_to_json(message)}
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            "author": message.parent_user.username,
            "author_profile_img": message.parent_user.profile.image.url,
            "content": message.message_text,
            "timestamp": str(message.date_posted),
        }

    commands = {
        "fetch_old_messages": fetch_old_messages,
        "fetch_messages": fetch_messages,
        "new_message": new_message,
        "fetch_groups" : fetch_groups,
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data["command"]](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps(message))

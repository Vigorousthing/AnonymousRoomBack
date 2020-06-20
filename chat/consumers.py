from channels.generic.websocket import AsyncWebsocketConsumer
import json


total_num_per_group = {}
like_num_per_group = {}


def response_json(json_request, group_name):
    message = json_request['message']
    opinion = json_request['opinion']
    tot_num = total_num_per_group[group_name]
    if json_request['type'] == "chat_message":
        return {
            'type': 'chat_message',
            'message': message,
            'opinion': opinion,
            'id': tot_num
        }
    elif json_request['type'] == "live_like":
        if json_request['id'] in like_num_per_group[group_name]:
            like_num_per_group[group_name][json_request['id']][0] += 1
        else:
            like_num_per_group[group_name][json_request['id']] = [1,
                                                                  message,
                                                                  opinion,
                                                                  json_request['id']]

        return {
            'type': 'live_like',
            'like_list': sorted([like_num_per_group[group_name][key]
                          for key in like_num_per_group[group_name]],
                                reverse=True)
        }


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        if self.room_group_name not in total_num_per_group:
            total_num_per_group[self.room_group_name] = 0
        if self.room_group_name not in like_num_per_group:
            like_num_per_group[self.room_group_name] = {}

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        total_num_per_group[self.room_group_name] += 1
        text_data_json = json.loads(text_data)
        await self.channel_layer.group_send(
            self.room_group_name,
            response_json(text_data_json, self.room_group_name)
        )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def live_like(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))



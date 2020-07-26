from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.http import AsyncHttpConsumer

from django.core.serializers.json import DjangoJSONEncoder
import datetime
import channels_redis
import json
import django.db
import socket


total_num_of_message_per_group = {}
total_num_of_post_per_group = {}

total_num_of_group_members = {}
like_num_per_group = {}

poll_state_per_group = {}


def response_json(json_request, group_name):
    tot_num = total_num_of_message_per_group[group_name]
    if json_request['type'] == "text":
        # message = json_request['message']
        content = json_request['content']
        opinion = json_request['opinion']
        send_time = json_request['post_time']
        return {
            'type': 'chat_message',
            'content': content,
            'opinion': opinion,
            'time': send_time,
            'id': tot_num
        }
    elif json_request['type'] == "live_like":
        message = json_request['message']
        opinion = json_request['opinion']
        send_time = json_request['time']
        if json_request['id'] in like_num_per_group[group_name]:
            like_num_per_group[group_name][json_request['id']][0] += \
                json_request['likeness']
        else:
            like_num_per_group[group_name][json_request['id']] = [json_request['likeness'],
                                                                  message,
                                                                  opinion,
                                                                  send_time,
                                                                  json_request['id']]

        return {
            'type': 'live_like',
            # like num / message / opinion / send_time / id
            'like_list': sorted([like_num_per_group[group_name][key]
                          for key in like_num_per_group[group_name]],
                                reverse=True)
        }
    elif json_request['type'] == "poll_post":
        p_id = total_num_of_message_per_group[group_name]
        total_num_of_message_per_group[group_name] += 1

        now = datetime.datetime.now()
        t = str(now)

        poll_state_per_group[group_name][p_id] = {
            'post': {
                'id': p_id,
                'title': json_request['title'],
                'poll_items': json_request['poll_items'],
                'start_time': t,
                'end': False,
            },
            'vote_state': [0 for i in range(
                len(json_request['poll_items']))],
        }

        return {
            'type': 'poll_view',
            'poll_info': [poll_state_per_group[group_name][each] for each
                              in poll_state_per_group[group_name]]
        }

    elif json_request['type'] == 'poll_vote':

        p_id = json_request['id']
        idx = json_request['vote_idx']

        # check whether vote is end or not
        if poll_state_per_group[group_name][p_id]['post']['end'] is True:
            return {
                'type': 'poll_view',
                'poll_info': [poll_state_per_group[group_name][each] for each
                              in poll_state_per_group[group_name]]
            }
        # if vote isn't over yet, check end time is passed
        else:
            e_time = datetime.datetime.strptime(
                poll_state_per_group[group_name][p_id]['post'][
                    'start_time'].split(".")[0],
                '%Y-%m-%d %H:%M:%S') + datetime.timedelta(minutes=1)
            now = datetime.datetime.now()
            # if end time is passed, make end flag True and return view
            if e_time < now:
                poll_state_per_group[group_name][p_id]["post"]['end'] = True
            # else, apply vote and return view
            else:
                poll_state_per_group[group_name][p_id]["vote_state"][idx] += 1
            return {
                'type': 'poll_view',
                'poll_info': [poll_state_per_group[group_name][each] for each
                              in poll_state_per_group[group_name]]
            }
    else:
        content = json_request['content']
        return {
            'type': 'multimedia',
            'like_list': content
        }


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        if self.room_group_name not in total_num_of_message_per_group:
            total_num_of_message_per_group[self.room_group_name] = 0
        if self.room_group_name not in like_num_per_group:
            like_num_per_group[self.room_group_name] = {}
        if self.room_group_name not in poll_state_per_group:
            poll_state_per_group[self.room_group_name] = {}

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        # send welcome packet
        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type': 'welcome',
            'like_list': sorted([like_num_per_group[self.room_group_name][key]
                          for key in like_num_per_group[self.room_group_name]],
                                reverse=True),
            'poll_info': [poll_state_per_group[self.room_group_name][each] for
                          each in poll_state_per_group[self.room_group_name]]
            }
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        total_num_of_message_per_group[self.room_group_name] += 1

        if text_data is None:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'multimedia',
                    'content': bytes_data
                }
            )
        else:
            text_data_json = json.loads(text_data)
            await self.channel_layer.group_send(
                self.room_group_name,
                response_json(text_data_json, self.room_group_name)
            )

    # Receive message from room group
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def live_like(self, event):
        await self.send(text_data=json.dumps(event))

    async def welcome(self, event):
        await self.send(text_data=json.dumps(event))

    async def poll_view(self, event):
        await self.send(text_data=json.dumps(event))

    async def multimedia(self, event):
        # await self.send(text_data=json.dumps(event))
        await self.send(bytes_data=event['content'])

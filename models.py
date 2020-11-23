from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
import os
from twilio.rest import Client
from secret import akk,tok
db = SQLAlchemy()



class Queue:

    def __init__(self):
        self._queue = []
        self._mode = 'LIFO'
        self._account_sid = akk
        self._auth_token = tok

    def enqueue(self, item):
        self._queue.append(item)
        client = Client(self._account_sid, self._auth_token)
        message = client.messages \
                .create(
                    body=f"{item['name']} was added to the queue, there are {len(self._queue) -1} users before him ",
                    from_='+12059286871',
                    to='+56999199479'
                )
        print(self._queue)
        print(message.sid)
       

    def dequeue(self):
        if self._mode == 'FIFO':
            lastuser = self._queue.pop(0)
            client = Client(self._account_sid, self._auth_token)
            message = client.messages \
                    .create(
                        body=f"{lastuser['name']} your turn has arrived, you where deleted from the list",
                        from_='+12059286871',
                        to='+56999199479'
                    )
            return lastuser['name']
            print(message.sid)

        if self._mode == 'LIFO':
            lastuser = self._queue.pop()
            client = Client(self._account_sid, self._auth_token)
            message = client.messages \
                    .create(
                        body=f"{lastuser['name']} your turn has arrived, you where deleted from the list",
                        from_='+12059286871',
                        to='+56999199479'
                    )
            print(message.sid)
            return lastuser['name']

    def get_queue(self):
        users = []
        for user in self._queue:
            users.append(user['name'])
        client = Client(self._account_sid, self._auth_token)
        message = client.messages \
                .create(
                    body=f"Users in the queue: {users}",
                    from_='+12059286871',
                    to='+56999199479'
                )
        print(message.sid)

    def size(self):
        return len(self._queue)

import os
# import the necessary libraries
from twilio.rest import Client

# set up the Twilio client
account_sid = 'ACa318f712416a8a5837f21c452a7fdf93'

auth_token = 'e9c0b8a725626833be03d628cdbab0aa'
client = Client(account_sid, auth_token)

# send the message
message = client.messages.create(
    body='Check out this image!',
    from_='whatsapp:+15076195949',
    
    to='whatsapp:+917980136952'
)

print(message.sid)

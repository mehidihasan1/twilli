from twilio.rest import Client

def create_client(sid, token):
    return Client(sid, token)

def search_numbers(client, country='US', type='mobile', contains=None):
    available_numbers = client.available_phone_numbers(country)
    number_type = getattr(available_numbers, type)
    return number_type.list(contains=contains, limit=5)

def buy_number(client, number):
    return client.incoming_phone_numbers.create(phone_number=number)

def release_number(client, sid):
    client.incoming_phone_numbers(sid).delete()

def list_numbers(client):
    return client.incoming_phone_numbers.list(limit=10)

def get_sms_messages(client, to_number):
    return client.messages.list(to=to_number, limit=5)
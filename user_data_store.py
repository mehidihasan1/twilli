user_twilio_data = {}

def set_user_twilio(user_id, sid, token):
    user_twilio_data[user_id] = {"sid": sid, "token": token}

def get_user_twilio(user_id):
    return user_twilio_data.get(user_id)
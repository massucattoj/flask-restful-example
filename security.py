import hmac

from models.user import UserModel


# A function to authenticate our user
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and hmac.compare_digest(user.password, password):
        return user

def identity(payload):
    # payload is the content of the JWT content
    user_id = payload['identity'] # extract user id from the payload
    return UserModel.find_by_id(user_id)

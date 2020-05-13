

class PrivateRoom():
    
    def __init__(self, user, conversation):
        self._user_1 = user
        self._user_1_public_key = ''
        self._user_2 = conversation
        self._user_2_public_key = ''
        self._websockets = []

    def get_name(self):
        return f'{self.user_1}:{self.user_2}'

    @property
    def user_1(self):
        return self._user_1

    @property
    def user_2(self):
        return self._user_2

    @property
    def user_1_public_key(self):
        return self._user_1_public_key

    @user_1_public_key.setter
    def user_1_public_key(self, value):
        self._user_1_public_key = value

    @property
    def user_2_public_key(self):
        return self._user_2_public_key

    @user_2_public_key.setter
    def user_2_public_key(self, value):
        self._user_2_public_key = value

    def get_ws_list(self):
        return self._websockets

    def append_ws(self, ws):
        self._websockets.append(ws)
        print(self._websockets)

    def remove_ws(self, ws):
        self._websockets.remove(ws)
        print(self._websockets)
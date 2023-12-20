class OTPSecret:
    def __init__(self):
        self.secrets = {}  # Dictionnaire pour stocker les secrets

    def store(self, username, secret):
        self.secrets[username] = secret

    def get(self, username):
        return self.secrets.get(username)

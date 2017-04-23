from mongoengine import *
from passlib.hash import sha256_crypt

class Assassin(DynamicDocument):
    name = StringField(required=True)
    email = EmailField()

    killed_time = DateTimeField()

    targets = DictField()
    kills = DictField()





class AdminUser(Document):
    username = StringField(unique=True, required=True)
    hashed_password = StringField(required=True)
    phone_number = IntField()


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def set_password(self, password):
        self.hashed_password = sha256_crypt.encrypt(password)


    @staticmethod
    def validate_login(password_hash, password):
        return sha256_crypt.verify(password, password_hash)

    def __unicode__(self):
        return self.username

    meta = {
        'indexes': [
            {'fields': ['username'], 'unique': True}
        ]
    }
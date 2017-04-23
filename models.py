from mongoengine import *
from passlib.hash import sha256_crypt
import datetime


class Mission(EmbeddedDocument):
    time = DateTimeField(default=datetime.datetime.utcnow())
    target = ReferenceField('Assassin', required=False)

    def __unicode__(self):
        return unicode(self.target)

class Assassin(DynamicDocument):
    name = StringField(required=True, unique=True)
    email = EmailField(unique=True)

    killed_time = DateTimeField()

    targets = EmbeddedDocumentListField(Mission)
    kills = EmbeddedDocumentListField(Mission)

    random_order = IntField()

    def __unicode__(self):
        return self.name

    meta = {
        'indexes': [
            {'fields': ['name'], 'unique': True}
        ]
    }






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
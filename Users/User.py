from howru_helpers.MongoHelper import MongoHelper
from log.logger import logger
from howru_models.keyboards import flag


class User(object):
    def __init__(self, name, identifier, username, picture, gender, role, language, collection_name, load_from_db):
        self.db = MongoHelper(db='users', collection=collection_name)
        self._identifier = str(identifier) if identifier else None
        self.role = role if role else None
        if load_from_db:
            self.load_from_db()
        else:
            self._name = str(name) if name else None
            self._picture = str(picture) if picture else None
            self._gender = str(gender) if gender else None
            self._language = str(language) if language else None
            self._username = str(username) if username else None

    def to_dict(self):
        return {
            '_id': self._identifier,
            'name': self._name,
            'picture': self._picture,
            'gender': self._gender,
            'language': self._language,
            'username': self._username
        }

    def to_db(self):
        logger.debug("Inserting user %d role %d into database...", self.identifier, self.role)
        record = self.to_dict()
        return self.db.insert_document(record)

    def exists(self):
        return self.db.count_documents({'_id': self.identifier})

    def load_from_db(self):
        try:
            doc = self.db.get_document_by_id(self.identifier)
            self.from_dict(doc)
        except:
            logger.exception(f'Unable to retrieve user {self.identifier} from DB.')
            raise Exception

    def from_dict(self, doc):
        self._name = doc['name']
        self._picture = doc['picture']
        self._gender = doc['gender']
        self._language = doc['language']
        self._username = doc['username']

    def update_field(self, field, value):
        self.db.update_document(self.identifier, {'$set': {field: value}})

    def delete_from_db(self):
        return self.db.delete_document_by_id(self.identifier)

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        raise Exception("Identifier can not be changed")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)
        self.update_field('name', self._name)

    @property
    def picture(self):
        return self._picture

    @picture.setter
    def picture(self, value):
        self._picture = str(value)
        self.update_field('picture', self._picture)

    @property
    def gender(self):
        if self._gender == "M":
            processed_value = "Male" if self.language == "EN" else "Masculino"
        elif self._gender == "F":
            processed_value = "Female" if self.language == "EN" else "Femenino"
        else:
            processed_value = "Other" if self.language == "EN" else "Otro"
        return processed_value

    @gender.setter
    def gender(self, value):
        if value in ("Male", "Masculino"):
            processed_value = "M"
        elif value in ("Female", "Femenino"):
            processed_value = "F"
        else:
            processed_value = "O"
        self._gender = processed_value
        self.update_field('gender', self._gender)

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        raise Exception("Username can not be changed")


    @property
    def language(self):
        if not self._language:
            doc = self.db.get_document_by_id(self.identifier)
            self._language = doc['language']
        return self._language

    # Language must be normalized
    @language.setter
    def language(self, value):
        self._language = 'ES' if value == flag('es') else 'EN'
        self.update_field('language', self._language)

# -*- coding: utf-8 -*-
"""
    tests.factories
    ~~~~~~~~~~~~~~~

    Overholt test factories module
"""

from datetime import datetime

from factory import Factory, Sequence, LazyAttribute
from flask.ext.security.utils import encrypt_password

from overholt.core import db
from overholt.models import *


class TestFactory(Factory):
    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        entity = target_class(**kwargs)
        db.session.add(entity)
        db.session.commit()
        return entity

class RoleFactory(TestFactory):
    class Meta:
        model = Role

    name = 'admin'
    description = 'Administrator'


class UserFactory(TestFactory):
    class Meta:
        model = User

    email = Sequence(lambda n: 'user{0}@overholt.com'.format(n))
    password = LazyAttribute(lambda a: encrypt_password('password'))
    last_login_at = datetime.utcnow()
    current_login_at = datetime.utcnow()
    last_login_ip = '127.0.0.1'
    current_login_ip = '127.0.0.1'
    login_count = 1
    roles = []
    active = True


class StoreFactory(TestFactory):
    class Meta:
        model = Store

    name = Sequence(lambda n: 'Store Number {0}'.format(n))
    address = '123 Overholt Alley'
    city = 'Overholt'
    state = 'New York'
    zip_code = '12345'


class ProductFactory(TestFactory):
    class Meta:
        model = Product

    name = Sequence(lambda n: 'Product Number {0}'.format(n))


class CategoryFactory(TestFactory):
    class Meta:
        model = Category

    name = Sequence(lambda n: 'Category {0}'.format(n))

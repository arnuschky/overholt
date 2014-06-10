# -*- coding: utf-8 -*-
"""
    tests
    ~~~~~

    tests package
"""

from flask_fillin import FormWrapper
from flask.testing import FlaskClient
from unittest import TestCase

from overholt.core import db

from .factories import UserFactory, RoleFactory
from .utils import FlaskTestCaseMixin


class OverholtTestCase(TestCase):
    pass


class OverholtAppTestCase(FlaskTestCaseMixin, OverholtTestCase):

    def _create_app(self):
        raise NotImplementedError

    def _create_fixtures(self):
        role = RoleFactory()
        self.user = UserFactory(roles=[role])

    def setUp(self):
        super(OverholtAppTestCase, self).setUp()
        self.app = self._create_app()
        self.client = FlaskClient(self.app, response_wrapper=FormWrapper)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self._create_fixtures()

    def tearDown(self):
        super(OverholtAppTestCase, self).tearDown()
        db.drop_all()
        self.app_context.pop()

    def _login(self, email=None, password=None):
        r = self.get('/login')
        self.csrf_token = r.form.fields['csrf_token']
        email = email or self.user.email
        password = password or 'password'
        return self.post('/login', data={'email': email, 'password': password},
                         follow_redirects=False)

from django.db import transaction
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import localtime


class UnitOfWork:

    def __init__(self):
        engine = create_engine("batch1")
        self.session_factory = sessionmaker(bind=engine)

    def __enter__(self):
        self.session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

from django.contrib.auth.models import User
from django.db.models import QuerySet


class IPAddressQuerySet(QuerySet):
    def related_with_user(self, user: User):
        return self.filter(user=user)

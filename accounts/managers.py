from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager
    """

    def create(self, email, password, **fields):
        """
        Create and save a user
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **fields):
        """
        Create and save a normal user
        """
        if not email:
            raise ValueError(_("The email must be set"))

        if fields.get("is_superuser") is True:
            raise ValueError(
                _("Normal user cannot be a superuser")
            )

        return self.create(email, password, **fields)

    def create_superuser(self, email, password, **fields):
        """
        Create and save a superuser
        """

        fields.setdefault("is_superuser", True)

        if fields.get("is_superuser") is not True:
            raise ValueError(_("Super user must have super user set to true"))

        return self.create(email, password, **fields)

    def get_by_id(self, _id=None):
        """
        Get User id
        """
        if not _id:
            raise ValueError(_("An ID is required"))

        return self.get(pk=_id)

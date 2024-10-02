from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):

    def _create_user(self, password, phone_number=None, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not phone_number and not extra_fields["email"]:
            raise ValueError("The given phone_number must be set")
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        if phone_number:
            user = self.model(phone_number=phone_number, **extra_fields)
        else:
            user = self.model(**extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number=None, email=None, password=None, **extra_fields):
        if not phone_number and not email:
            raise ValueError("Eaither the phone number or email should given")
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        if email:
            extra_fields["email"] = email
        return self._create_user(
            phone_number=phone_number, password=password, **extra_fields
        )

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)

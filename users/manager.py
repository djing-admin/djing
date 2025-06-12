from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations: bool = True

    def create_user(
        self, first_name, last_name, username, email, password, super_user=False
    ):
        email = self.normalize_email(email)

        user = self.model(
            first_name=first_name, last_name=last_name, username=username, email=email
        )

        user.set_password(password)

        user.is_superuser = super_user

        user.is_staff = super_user

        user.save()

        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        if not first_name:
            raise ValueError("first_name is required")

        if not last_name:
            raise ValueError("last_name is required")

        if not username:
            raise ValueError("username is required")

        if not email:
            raise ValueError("email is required")

        if not password:
            raise ValueError("password is required")

        return self.create_user(first_name, last_name, username, email, password, True)

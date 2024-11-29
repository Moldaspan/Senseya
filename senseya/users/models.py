import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser, BaseUserManager
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")
        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, password, **extra_fields)


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    jwt_key = models.UUIDField(default=uuid.uuid4)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="baseuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="baseuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


class User(AbstractUser):
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=False)

    username = None

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="user_set_custom",
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="user_set_custom",
        blank=True,
        help_text="Specific permissions for this user.",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from datetime import datetime
from django.utils.http import base36_to_int, int_to_base36
from django.utils.crypto import constant_time_compare, salted_hmac
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured


def get_code_model():
    """
    Return the User model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.AUTH_CODE_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed"
            % settings.AUTH_USER_MODEL
        )

class CustomUserTokenGenerator(PasswordResetTokenGenerator):
    """
      Custom token generator:
          - user pk in token
          - expires after 15 minutes
          - longer hash (40 instead of 20)
      """

    KEY_SALT = "django.contrib.auth.tokens.PasswordResetTokenGenerator"
    SECRET = settings.SECRET_KEY
    EXPIRY_TIME = 60 * 15

    def make_token(self, user) -> str:
        return self._make_token_with_timestamp(user, int(datetime.now().timestamp()))

    def check_token(self, user, token: str):
        user_model = get_code_model()
        if not token:
            return None
        try:
            token = str(token)
            user_pk, ts_b36, token_hash = token.rsplit("-", 2)
            ts = base36_to_int(ts_b36)
            user = user_model._default_manager.get(pk=user_pk)
        except (ValueError, TypeError, user_model.DoesNotExist):
            return None

        if (datetime.now().timestamp() - ts) > self.EXPIRY_TIME:
            return None  # pragma: no cover

        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            return None

        return user

    def _make_hash_value(self, user, timestamp):
        """
        Hash the user's primary key, email (if available), and some user state
        that's sure to change after a password reset to produce a token that is
        invalidated when it's used:
        1. The password field will change upon a password reset (even if the
           same password is chosen, due to password salting).
        2. The last_login field will usually be updated very shortly after
           a password reset.
        Failing those things, settings.PASSWORD_RESET_TIMEOUT eventually
        invalidates the token.

        Running this data through salted_hmac() prevents password cracking
        attempts using the reset token, provided the secret isn't compromised.
        """
        # Truncate microseconds so that tokens are consistent even if the
        # database doesn't support microseconds.
        login_timestamp = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        return f"{user.pk}{user.user}{login_timestamp}{timestamp}{user.user_id_messenger}{user.user_activation_key}"

    def _make_token_with_timestamp(self, user, timestamp: int, **kwargs) -> str:
        ts_b36 = int_to_base36(timestamp)
        token_hash = salted_hmac(
            self.KEY_SALT,
            self._make_hash_value(user, timestamp),
            secret=self.SECRET,
        ).hexdigest()
        return f"{user.pk}-{ts_b36}-{token_hash}"

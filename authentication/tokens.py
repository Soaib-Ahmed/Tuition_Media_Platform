from django.contrib.auth.tokens import PasswordResetTokenGenerator

class EmailConfirmationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        if hasattr(user, 'email_confirmed'):
            return (
                str(user.pk) + str(timestamp) +
                str(user.email_confirmed)
            )
        return super()._make_hash_value(user, timestamp)

email_confirmation_token = EmailConfirmationTokenGenerator()
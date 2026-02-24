from django.db.models.signals   import post_save
from django.dispatch            import receiver
from django.core.mail           import EmailMessage
from django.template.loader     import render_to_string
from .models                    import Invitation

@receiver(post_save, sender=Invitation)
def send_invitation_email(sender, instance, created, **kwargs):
    if created:
        # print(f"Sending invitation email to {instance.owner_email}")
        invite_link = instance.invite_url()
        html = render_to_string('porchpanel/emails/porch-user-invitation.html', {
            'invite_link': invite_link,
        })
        email = EmailMessage(
            subject="Welcome to 2026 Tower Porchfest – Important Dates & Host Information",
            body=html,
            from_email="Tower Porchfest <info@towerporchfest.org>",
            to=[instance.owner_email],
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)
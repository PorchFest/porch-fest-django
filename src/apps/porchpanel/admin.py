from django.contrib     import admin
from .models            import Invitation
from django.utils.html  import format_html

@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ("owner_email", "accepted", "expires_at", "invite_link")
    readonly_fields = ("invite_link",)

    def invite_link(self, obj):
        return format_html(
            '<button type="button" onclick="navigator.clipboard.writeText(\'{}\')">Copy Invite Link</button>',
            obj.invite_url()
        )

    invite_link.short_description = "Invite Link"
from rest_framework.permissions import BasePermission

from circles.models import Membership

class isActiveCircleMember(BasePermission):
    """permite el acceso solo a miembros"""

    def has_permission(self, request, view):

        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True



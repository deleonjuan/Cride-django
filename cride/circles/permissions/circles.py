from rest_framework.permissions import BasePermission

from circles.models import Membership


class isCircleAdmin(BasePermission):
    """
    da permiso de manipular el circulo solo si es el admin
    """
    def has_object_permission(self, request, view, obj):
        """ verifica que el usuario tenga mebresia en el circulo """
        try:
            Membership.objects.get(
                user=request.user,
                circle=obj,
                is_admin=True,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True

from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from circles.models import Circle, Membership, Invitation
from circles.serializers import MembershipModelSerializer, AddMemberSerializer

from circles.permissions.memberships import isActiveCircleMember, IsSelfMember

class MembershipViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet):

    serializer_class = MembershipModelSerializer

    def dispatch(self, request, *args, **kwards):
        slug_name = kwards['slug_name']
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super(MembershipViewSet, self).dispatch(request, *args, **kwards)

    def get_permissions(self):
        permissions = [IsAuthenticated]
        if self.action != 'create':
            permissions.append(isActiveCircleMember)
        if self.action == 'invitations':
            permissions.append(IsSelfMember)
        return [ p() for p in permissions ]

    def get_queryset(self):
        """ return circle members"""
        return Membership.objects.filter(
            circle=self.circle,
            is_active=True
        )

    def get_object(self):
        return get_object_or_404(
            Membership,
            user__username=self.kwargs['pk'],
            circle=self.circle,
            is_active=True
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    @action(detail=True, methods=['get'])
    def invitations(self, request, *args, **kwargs):

        member = self.get_object()

        invited_members = Membership.objects.filter(
            circle=self.circle,
            invited_by=request.user,
            is_active=True
        )

        unused_invitations = Invitation.objects.filter(
            circle=self.circle,
            issued_by=request.user,
            is_used=False
        ).values_list('code')

        diff = member.remaining_invitations - len(unused_invitations)

        invitations = [x[0] for x in unused_invitations]
        for i in range(0, diff):
            invitations.append(
                Invitation.objects.create(issued_by=request.user, circle=self.circle).code
            )

        data = {
            'used_invitations': MembershipModelSerializer(invited_members, many=True).data,
            'invitations': invitations
        }

        return Response(data)

    def get_serializer_context(self):
        context = super(RideViewSet, self).get_serializer_context()
        context['circle'] = self.circle
        return context

    def create(self, request, *args, **kwargs):

        serializer = AddMemberSerializer(
            data=request.data,
            context={'circle': self.circle, 'request': request}
        )

        serializer.is_valid(raise_exception=True)
        member = serializer.save()

        data = self.get_serializer(member).data
        return Response(data, status=status.HTTP_201_CREATED)





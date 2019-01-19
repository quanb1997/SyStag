from rest_framework import permissions

# Tristan: we can probably remove this later. Although we could have permissions classes for
# any class based view

# Tristan: following rest_framework tutorial
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user


# used to check whether user can edit group or not
class IsGroupAdmin(permissions.BasePermission):
    pass
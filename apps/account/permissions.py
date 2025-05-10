from rest_framework import permissions

class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: return True
        if not request.user and not request.user.is_authenticated: return False
        if not request.user.is_verified: return False
        return True
    

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission:
    - Read for all users
    - Write only for owner
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
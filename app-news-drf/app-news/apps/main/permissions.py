from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permisson that allows only user to edit object
    """
    
    def has_object_permission(self, request, view, obj):
        # Read mode for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
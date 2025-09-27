from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permissions allows editing comments only for authors
    """
    
    def has_object_permission(self, request, view, obj):
        # allow reading for all
        if request.method in permissions.SAFE_METHODS:
            return True
        # allow editing only for author
        return obj.author == request.user
        
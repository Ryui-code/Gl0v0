from rest_framework.permissions import BasePermission, SAFE_METHODS

class StatusBasedPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        role = getattr(user, 'status', None)
        try:
            model_name = view.get_queryset().model.__name__
        except Exception:
            return True

        if role == 'Seller':
            if model_name == 'Store':
                return True
            if model_name == 'StoreRating':
                return request.method in SAFE_METHODS
            return False

        if role == 'Client':
            if model_name == 'Store':
                return request.method in SAFE_METHODS
            if model_name in ['Cart', 'Order', 'CourierRating', 'StoreRating']:
                return True
            return False

        if role == 'Courier':
            if model_name in ['Order', 'CourierRating']:
                return request.method in SAFE_METHODS
            return False
        return False
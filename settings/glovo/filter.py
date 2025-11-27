from django_filters import FilterSet
from .models import Store

class StoreFilterSet(FilterSet):
    class Meta:
        model = Store
        fields = {
            'store_name': ['exact'],
            'category': ['exact'],
        }
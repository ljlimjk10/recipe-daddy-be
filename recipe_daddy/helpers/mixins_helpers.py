from rest_framework.generics import get_object_or_404


class MultipleFieldLookupMixin:

    def get_object(self):
        queryset = self.get_queryset() 
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs.get(field):
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
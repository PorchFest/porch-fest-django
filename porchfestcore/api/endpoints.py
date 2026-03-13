from rest_framework.generics    import ListAPIView
from rest_framework.views       import APIView
from rest_framework.response    import Response
from django.http                import JsonResponse
from .serializers               import PorchMapSerializer
from .filters                   import PorchMapFilter
from porchfestcore.models       import Porch, Performance
from django.db.models import Prefetch


class PorchMap(ListAPIView):
    filterset_class     = PorchMapFilter
    serializer_class    = PorchMapSerializer
    def get_queryset(self):
        qs              = Porch.objects.filter(approved=True)
        filterset       = PorchMapFilter(self.request.GET, queryset=qs)
        performance_qs  = Performance.objects.none()
        if filterset.form.is_valid():
            active_filters = {
                k: v for k, v in filterset.form.cleaned_data.items()
                if v not in (None, "", [])
            }
            qs = filterset.qs
            if active_filters:
                print(active_filters)
                performance_filters = {}
                if "genre" in active_filters:
                    performance_filters["performer__genre__iexact"] = active_filters["genre"]
                if "after" in active_filters:
                    performance_filters["start_time__gte"]          = active_filters["after"]
                if "search" in active_filters:
                    performance_filters["performer__name__icontains"] = active_filters["search"]
                performance_qs = Performance.objects.filter(**performance_filters)
        qs = qs.prefetch_related(
            Prefetch("performances", queryset=performance_qs)
        )
        return qs.distinct()
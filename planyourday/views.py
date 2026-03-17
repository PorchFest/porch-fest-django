from django.shortcuts import render
from django.views.generic import ListView
from porchfestcore.models   import Performance
from planyourday.api.filters           import PerformanceFilter

def index(request):
    performances = Performance.objects.filter(porch__approved=True).distinct()
    return render(request, 'planyourday/index.html', {'performances': performances})

class PerformancesListView(ListView):
    template_name = 'planyourday/performances.html'
    context_object_name = 'performances'

    def get_queryset(self):
        qs = Performance.objects.filter(porch__approved=True).distinct()
        self.filterset = PerformanceFilter(self.request.GET, queryset=qs)

        if self.filterset.is_valid():
            return self.filterset.qs
        
        return qs
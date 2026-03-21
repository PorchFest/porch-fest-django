from django.shortcuts import render
from django.views.generic import ListView
from porchfestcore.models   import Performance, Performer
from planyourday.api.filters           import PerformanceFilter

def index(request):
    performances = Performance.objects.filter(porch__approved=True).distinct()
    genres = Performer.Genre.choices
    performance_count = len(performances)
    return render(request, 'planyourday/index.html', {'performances': performances, 'genres': genres, 'performance_count':performance_count})

class PerformancesListView(ListView):
    template_name = 'planyourday/performances.html'
    context_object_name = 'performances'

    def get_queryset(self):
        qs = Performance.objects.filter(porch__approved=True).distinct()
        self.filterset = PerformanceFilter(self.request.GET, queryset=qs)

        if self.filterset.is_valid():
            return self.filterset.qs
        
        return qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        qs = self.object_list

        context['performance_count'] = len(qs)
        context['filterset'] = self.filterset

        return context
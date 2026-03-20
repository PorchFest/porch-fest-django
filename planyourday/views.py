from django.shortcuts           import render, get_object_or_404
from django.views.generic       import ListView
from porchfestcore.models       import Performance
from planyourday.api.filters    import PerformanceFilter
from planyourday.models         import Itinerary
# remove from production:
from django.views.decorators.csrf import csrf_exempt

def index(request):
    performances = Performance.objects.filter(porch__approved=True).distinct()
    return render(request, 'planyourday/index.html', {'performances': performances})

# Notes for rebuilt performances view with add to itinerary logic
# performances.html is performance-list.html and looks like this now:
# {% for performance in performances %}
#     {% include "planyourday/performance-detail.html" %}
# {% endfor %}

# Add performance handles the itinerary logic and returns the performance html with the updated checkmark (or it should :)). This is the POST url for it:
# /plan-your-day/add-performance/740897a5-0765-4056-8336-fda6842ffdb2 (itinerary id)
# With a body/form data {performance_id: 94747a76-72d5-4ac9-8f50-99a0e624f1bb}

class PerformancesListView(ListView):
    template_name = 'planyourday/performance-list.html'
    context_object_name = 'performances'

    def get_queryset(self):
        qs = Performance.objects.filter(porch__approved=True).distinct()
        self.filterset = PerformanceFilter(self.request.GET, queryset=qs)

        if self.filterset.is_valid():
            return self.filterset.qs
        
        return qs

@csrf_exempt
def add_performance(request, itinerary_id):
    itinerary = get_object_or_404(Itinerary, id=itinerary_id)
    performance_id = request.POST.get('performance_id')
    performance = get_object_or_404(Performance, id=performance_id)

    if not itinerary.performances.filter(id=performance.id).exists():
        itinerary.performances.add(performance)

    context = {
        "performance": performance,
        "itinerary": itinerary,
    }

    return render(request, "planyourday/performance-detail.html", context)
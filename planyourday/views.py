from django.shortcuts           import render, get_object_or_404
from django.views.generic       import ListView
from porchfestcore.models       import Performance
from planyourday.api.filters    import PerformanceFilter
from planyourday.models         import Itinerary

def plan_your_day(request):
    performances    = Performance.objects.filter(porch__approved=True).distinct()
    itinerary       = get_or_create_itinerary(request)
    return render(request, 'planyourday/index.html', {'performances': performances, 'itinerary': itinerary.ordered_performances()})

# Notes for rebuilt performances view with add to itinerary logic
# performances.html is performance-list.html and looks like this now:
# {% for performance in performances %}
#     {% include "planyourday/performance-detail.html" %}
# {% endfor %}

# Add performance handles the itinerary logic and returns the performance html with the updated checkmark (or it should :)). This is the POST url for it:
# /plan-your-day/add-performance
# With a body/form data {performance_id: 94747a76-72d5-4ac9-8f50-99a0e624f1bb}

# I added some more stuff so that we can eventually update the itinerary when a performance gets added (or removed :P) I'm commiting the html files so that the idea makes sense
# Actually I think I pretty much got it there? heckin...

# More updates I added a remove performance path. Now the only thing I think we need to api is creating an itinerary if we don't have one. Something like check to see if localstorage exists, if not create itinerary which will return the itinerary id for future requests. Example how it works from plan your day right now:
# UPDATE AGAAIN: I used sessions in the view to keep track of the itinerary per session. Everything should just work off of performance_id now :O

# I also included the itinerary in the default page load too so it should be ready to wire up I think? I'm sure we're missing stuff and the filtering is of course not ready but should be good otherwise

# Here is the htmx example:

# <div
#     style="width: 100px;height: 100px;background-color: blue;color: white;"
#     hx-post="http://localhost:8300/plan-your-day/add-performance"
#     hx-trigger="click"
#     hx-vals='{"performance_id": "83460f22-298a-47d0-8d94-1503060aa7bf"}'
#     hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'
# >
#     click here
# </div>
# <div id="itinerary_sidebar"></div>

class PerformancesListView(ListView):
    template_name       = 'planyourday/performance-list.html'
    context_object_name = 'performances'
    def get_queryset(self):
        qs              = Performance.objects.filter(porch__approved=True).distinct()
        self.filterset  = PerformanceFilter(self.request.GET, queryset=qs)
        if self.filterset.is_valid():
            return self.filterset.qs
        return qs

def add_performance(request):
    itinerary       = get_or_create_itinerary(request)
    performance_id  = request.POST.get('performance_id')
    performance     = get_object_or_404(Performance, id=performance_id)
    if not itinerary.performances.filter(id=performance.id).exists():
        itinerary.performances.add(performance)
    context = {
        "performance": performance,
        "itinerary": itinerary.ordered_performances(),
    }
    return render(request, "planyourday/performance-detail-update.html", context)

def remove_performance(request):
    itinerary       = get_or_create_itinerary(request)
    performance_id  = request.POST.get('performance_id')
    performance     = get_object_or_404(Performance, id=performance_id)
    itinerary.performances.remove(performance)
    context = {
        "performance": performance,
        "itinerary": itinerary.ordered_performances(),
    }
    return render(request, "planyourday/itinerary-list-update.html", context)

def get_or_create_itinerary(request):
    itinerary_id    = request.session.get("itinerary_id")
    if itinerary_id:
        try:
            return Itinerary.objects.get(id=itinerary_id)
        except Itinerary.DoesNotExist:
            pass
    itinerary       = Itinerary.objects.create()
    request.session["itinerary_id"] = str(itinerary.id)
    return itinerary
from django.shortcuts           import render, get_object_or_404
from django.views.generic       import ListView
from porchfestcore.models       import Performance
from planyourday.api.filters    import PerformanceFilter
from planyourday.models         import Itinerary

def plan_your_day(request):
    performances    = with_show_time(get_filtered_performances(request))
    itinerary       = get_or_create_itinerary(request)
    return render(request, 'planyourday/index.html', {'performances': performances, 'itinerary': itinerary.ordered_performances()})

class PerformancesListView(ListView):
    template_name       = 'planyourday/performance-list.html'
    context_object_name = 'performances'
    def get_queryset(self):
        return get_filtered_performances(self.request)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['performances'] = with_show_time(context['performances'])
        return context

def get_filtered_performances(request):
    qs              = Performance.objects.filter(porch__approved=True).distinct()
    filterset  = PerformanceFilter(request.GET, queryset=qs)
    if filterset.is_valid():
        return filterset.qs.order_by('start_time')
    return qs

def with_show_time(performances_qs):
    performances = list(performances_qs)
    previous_hour = None
    for p in performances:
        if p.start_time is None:
            continue
        current_hour = p.start_time.hour
        if previous_hour is None or current_hour != previous_hour:
            p.show_time = True
        else:
            p.show_time = False
        previous_hour = current_hour
    return performances

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
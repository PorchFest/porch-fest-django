from django.shortcuts 		import render
from django.views.generic 	import TemplateView
from django.http			import JsonResponse
from django.conf 		    import settings
from .models                import Genre
# from planyourday.views      import get_or_create_itinerary

def map_page(request):
    genres = Genre.objects.order_by('name').filter(performer__isnull=False).distinct()
    context = {
        'genres': genres,
        'MAPBOX_PUBLIC_KEY': settings.MAPBOX_PUBLIC_KEY
    }
    if request.session.get('itinerary_id'):
        context['itinerary'] = get_or_create_itinerary(request).ordered_performances()

    return render(request, 'porchfestcore/map.html', context)

def bland_map(request):
    return render(request, 'porchfestcore/bland-map.html', {'MAPBOX_PUBLIC_KEY': settings.MAPBOX_PUBLIC_KEY})

def coming_soon(request):
    return render(request, 'porchfestcore/coming-soon.html')






# from django.shortcuts           import render, get_object_or_404
# from django.views.generic       import ListView
# from porchfestcore.models       import Performance, Genre
# from planyourday.api.filters    import PerformanceFilter
# from planyourday.models         import Itinerary

# def plan_your_day(request, itinerary_id=None):
#     performances = (
#         Performance.objects
#         .select_related('porch', 'performer')
#         .prefetch_related('performer__genres')
#     )
#     performances        = with_show_time(performances)
#     genres              = Genre.objects.order_by('name').filter(performer__isnull=False).distinct()
#     itinerary           = None
#     if itinerary_id:
#         itinerary       = get_object_or_404(Itinerary, id=itinerary_id)
#     elif request.session.get('itinerary_id'):
#         itinerary       = get_or_create_itinerary(request)

#     if itinerary:
#         context = {
#             'performances': performances,
#             'itinerary':    itinerary.ordered_performances(),
#             'itinerary_id': itinerary.id,
#             'genres':       genres,
#             "itinerary_test": set(item.id for item in itinerary.ordered_performances()),
#         }
#         if itinerary_id:
#             context["shared"] = True
#     else:
#         context = {
#             'performances': performances,
#             'genres':       genres,
#         }
#     return render(request, 'planyourday/index.html', context)

# class PerformancesListView(ListView):
#     template_name       = 'planyourday/performance-list.html'
#     context_object_name = 'performances'

#     def get_queryset(self):
#         return (
#             get_filtered_performances(self.request)
#             .select_related('porch', 'performer')
#             .prefetch_related('performer__genres')
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         itinerary = None
#         itinerary_id = self.kwargs.get("itinerary_id")

#         if itinerary_id:
#             itinerary = get_object_or_404(Itinerary, id=itinerary_id)
#             context["shared"] = True
#         elif self.request.session.get("itinerary_id"):
#             itinerary = get_or_create_itinerary(self.request)

#         if itinerary:
#             context["itinerary_test"] = {
#                 item.id for item in itinerary.ordered_performances()
#             }
#             context["itinerary_id"] = itinerary.id

#         context['performances'] = with_show_time(context['performances'])
#         return context

# # Helper Function
# def get_filtered_performances(request):
#     qs = Performance.objects.filter(porch__approved=True)
#     filterset = PerformanceFilter(request.GET, queryset=qs)
#     if filterset.is_valid():
#         return filterset.qs.order_by('start_time').distinct()
#     return qs.distinct()

# # Helper Function
# def with_show_time(performances_qs):
#     performances = list(performances_qs)
#     previous_hour = None
#     for p in performances:
#         if p.start_time is None:
#             continue
#         current_hour = p.start_time.hour
#         if previous_hour is None or current_hour != previous_hour:
#             p.show_time = True
#         else:
#             p.show_time = False
#         previous_hour = current_hour
#     return performances

# def add_performance(request, itinerary_id=None):
#     if itinerary_id:
#         itinerary   = get_object_or_404(Itinerary, id=itinerary_id)
#     else:
#         itinerary   = get_or_create_itinerary(request)
#     performance_id  = request.POST.get('performance_id')
#     performance     = get_object_or_404(Performance, id=performance_id)
#     if not itinerary.performances.filter(id=performance.id).exists():
#         itinerary.performances.add(performance)
#     context = {
#         "performance":  performance,
#         "itinerary":    itinerary.ordered_performances(),
#         "itinerary_id": itinerary.id,
#         "itinerary_test": set(item.id for item in itinerary.ordered_performances()),
#     }
#     return render(request, "planyourday/performance-detail-update.html", context)

# def remove_performance(request, itinerary_id=None):
#     if itinerary_id:
#         itinerary   = get_object_or_404(Itinerary, id=itinerary_id)
#     else:
#         itinerary   = get_or_create_itinerary(request)
#     performance_id  = request.POST.get('performance_id')
#     performance     = get_object_or_404(Performance, id=performance_id)
#     itinerary.performances.remove(performance)
#     context = {
#         "performance":  performance,
#         "itinerary":    itinerary.ordered_performances(),
#         "itinerary_id": itinerary.id,
#     }
#     return render(request, "planyourday/itinerary-list-update.html", context)

# def get_or_create_itinerary(request, id=None):
#     itinerary_id = request.session.get("itinerary_id")
#     if itinerary_id:
#         try:
#             request.session.modified = True
#             return Itinerary.objects.get(id=itinerary_id)
#         except Itinerary.DoesNotExist:
#             pass
#     itinerary = Itinerary.objects.create()
#     request.session["itinerary_id"] = str(itinerary.id)
#     return itinerary
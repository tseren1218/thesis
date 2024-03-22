from datetime import timezone
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, "core/index.html")

def get_locations(request):
    return render(request, 'core/locations.html', {'locations': Location.nodes.all()})

# class LocationListView(generic.ListView):
#     model = Location
#     paginate_by = 10

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["now"] = timezone.now()
#         return context
    
def new_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ажмилттай үүсгэлээ!')
            return redirect('core:index')  # Redirect to a success page or another URL
        else:
            print("error form")
    else:
        form = LocationForm()
    return render(request, 'core/new_location.html', {'form': form})
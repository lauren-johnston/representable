from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.decorators import verified_email_required
from django.forms import formset_factory
from .forms import CommunityForm, IssueForm
from .models import CommunityEntry, Issue
from django.views.generic.edit import FormView
from django.core.serializers import serialize
from shapely.geometry import Polygon, mapping
import geojson, os, json,re
from django.http import JsonResponse


#******************************************************************************#

# must be imported after other models
from django.contrib.gis.geos import Point

#******************************************************************************#

'''
Documentation: https://docs.djangoproject.com/en/2.1/topics/class-based-views/
'''
class Index(TemplateView):
    template_name = "main/index.html"

    # Add extra context variables.
    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs) # get the default context data
        context['mapbox_key'] = os.environ.get('DISTR_MAPBOX_KEY')
        return context

#******************************************************************************#

class MainView(TemplateView):
    template_name = "main/main_test.html"

    # Add extra context variables.
    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs) # get the default context data
        context['mapbox_key'] = os.environ.get('DISTR_MAPBOX_KEY')
        return context

#******************************************************************************#

class Timeline(TemplateView):
    template_name = "main/timeline.html"

#******************************************************************************#

class AboutUs(TemplateView):
    template_name = "main/about.html"

#******************************************************************************#

class Map(TemplateView):
    template_name = "main/map.html"
    # serialize('geojson', Entry.objects.all(), geometry_field='polygon', fields=('entry_polygon',))

    def get_context_data(self, **kwargs):
        # GEOJSONSerializer = serializers.get_serializer("geojson")
        # geojson_serializer = GEOJSONSerializer()
        # geojson_serializer.serialize(Entry.objects.only('entry_polygon'))
        # data = geojson_serializer.getvalue()
        # data = serialize("geojson", CommunityEntry.objects.all(
        # ), geometry_field="Polygon", fields=("entry_polygon", "Polygon",))
        # print("printing data")
        # print(data)
        # struct = json.loads(data)
        # data = Entry.objects.only('entry_polygon')

        # s = "".join(data)
        # something = geojson.loads(s)

        # print(geojson.loads(Entry.objects.all()))
        # print(data[0])
        # print(geojson.Polygon(data[0]))
        # data = json.dumps(struct)

        # the dict of issues + input of descriptions
        issues = dict()
        for obj in Issue.objects.all():
            cat = obj.category
            cat = re.sub('_', ' ', cat).title()
            if cat == 'Economic':
                cat = 'Economic Affairs'
            if cat == 'Health':
                cat = 'Health and Health Insurance'
            if cat == 'Internet':
                cat = 'Internet Regulation'
            if cat == 'Women':
                cat = 'Women\'s Issues'
            if cat == 'Lgbt':
                cat = 'LGBT Issues'
            if cat == 'Security':
                cat = 'National Security'
            if cat == 'Welfare':
                cat = 'Social Welfare'
            if cat in issues:
                issues[cat].append(obj.description)
            else:
                issues[cat] = [obj.description]



        a = []
        for obj in CommunityEntry.objects.all():
            # print(obj.entry_polygon.geojson)
            a.append(obj.entry_polygon.geojson)

        final = []
        for obj in a:
            s = "".join(obj)

            # add all the coordinates in the array
            # at this point all the elements of the array are coordinates of the polygons
            struct = geojson.loads(s)
            # print("printing the struct")
            # print(struct)
            final.append(struct.coordinates)

        context = ({
            # 'entries':  serialize('geojson', Entry.objects.all(), geometry_field='polygon', fields=('entry_polygon')),
            # 'entries': data,
            'issues': issues,
            'entries': final,
            'mapbox_key': os.environ.get('DISTR_MAPBOX_KEY'),
        })
        return context

#******************************************************************************#

class Thanks(TemplateView):
    template_name = "main/thanks.html"

#******************************************************************************#

class EntryView(LoginRequiredMixin, View):
    '''
    EntryView displays the form and map selection screen.
    '''
    template_name = 'main/entry.html'
    form_class = CommunityForm
    initial = {'key': 'value'}
    success_url = '/thanks/'
    data = {
        'form-TOTAL_FORMS': '1',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': ''
    }
    # Create the formset, specifying the form and formset we want to use.
    IssueFormSet =  formset_factory(IssueForm, extra=1)

    # https://www.agiliq.com/blog/2019/01/django-formview/
    def get_initial(self):
        initial = self.initial
        if self.request.user.is_authenticated:
            initial.update({'user': self.request.user})
        return initial

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.get_initial())
        issue_formset = self.IssueFormSet(self.data)
        context = {
            'form': form,
            'issue_formset': issue_formset,
            'mapbox_key': os.environ.get('DISTR_MAPBOX_KEY')
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        issue_formset = self.IssueFormSet(request.POST)
        if form.is_valid() and issue_formset.is_valid():
            entryForm = form.save(commit=False)
            entryForm.save()
            for issue_form in issue_formset:
                category = issue_form.cleaned_data.get('category')
                description = issue_form.cleaned_data.get('description')
                # Ignore form row if it's completely empty.
                if category and description:
                    issue = issue_form.save(commit=False)
                    # Set issueFormset form Foreign Key (entry) to the recently
                    # created entryForm.
                    issue.entry = entryForm
                    issue.save()
            return HttpResponseRedirect(self.success_url)
        context = {
            'form': form,
            'issue_formset': issue_formset,
            'mapbox_key': os.environ.get('DISTR_MAPBOX_KEY')
        }
        print(issue_formset)
        return render(request, self.template_name, context)

#******************************************************************************#

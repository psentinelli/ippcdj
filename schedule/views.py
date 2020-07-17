
import json
import pytz
import datetime
#from urllib import quote
from six.moves.urllib.parse import quote
from django.contrib.messages import info, error
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User,Group
from schedule.conf.settings import GET_EVENTS_FUNC, OCCURRENCE_CANCEL_REDIRECT
from schedule.forms import EventForm, OccurrenceForm, EventFileFormSet, EventUrlFormSet,EventParticipantsFormSet
from schedule.models import Calendar, Occurrence, Event,EventParticipants
from schedule.periods import weekday_names
from schedule.utils import check_event_permissions, coerce_date_dict
from ippc.forms import IssueKeywordsRelateForm
from ippc.models import IssueKeywordsRelate,CountryPage,IppcUserProfile, UserMembershipHistory
from ippc.views import  CPMS, split,send_notificationevent_message,send_notification_register_event_message
from django.template.response import TemplateResponse
from django.core import mail
from django.core.mail import send_mail

def calendar(request, calendar_slug, template='schedule/calendar.html'):
    """
    This view returns a calendar.  This view should be used if you are
    interested in the meta data of a calendar, not if you want to display a
    calendar.  It is suggested that you use calendar_by_periods if you would
    like to display a   calendar.

    Context Variables:

    ``calendar``
        The Calendar object designated by the ``calendar_slug``.
    """
    calendar = get_object_or_404(Calendar, slug=calendar_slug)
    return render_to_response(template, {
        "calendar": calendar,
    }, context_instance=RequestContext(request))

def calendar_by_year(request, calendar_slug, year=None, template_name="schedule/calendar_by_year.html"):
    """
    """
    model = Event
    calendar = get_object_or_404(Calendar, slug=calendar_slug)
    try:
        date = coerce_date_dict(request.GET)
    except ValueError:
        raise Http404
    print(date)
    if date:
        try:
            date = datetime.datetime(**date)
            print(date)
        except ValueError:
            raise Http404
    else:
        date = timezone.now()
      
    user = request.user   
    can_add= 0 
    if user.groups.filter(name='IPPC Secretariat'):
        can_add=1
   
    calendar = get_object_or_404(Calendar, slug=calendar_slug)
    
    event_list= calendar.event_set.filter(start__year=date.year,country=-1).order_by('start')
    event_list2=[]
    months_list = []
    for m in range(1,13):
        months_list.append((m, datetime.date(2014, m, 1).strftime('%B')))
        monthevents=[]
     
        for e in event_list:
            
            if e.start.month == m:
                monthevents.append(e)
                 
        event_list2.append((m,monthevents))
        
    period_objects = dict([(period.__name__.lower(), period(event_list, date)) for period in year])
  #  return render_to_response(template_name, {
  #      'periods': period_objects,
  #      'calendar': calendar,
  #      'weekday_names': weekday_names,
  #      'event_list': event_list,
  #      'months_list': months_list,
  #      'event_list2': event_list2,
  #      'current_year': date.year,
  #      'can_add': can_add,
  #      'here': quote(request.get_full_path()),
  #  }, context_instance=RequestContext(request), )
    return TemplateResponse(request,template_name,  { 'periods': period_objects,
        'calendar': calendar,
        'weekday_names': weekday_names,
        'event_list': event_list,
        'months_list': months_list,
        'event_list2': event_list2,
        'current_year': date.year,
        'can_add': can_add,
        'here': quote(request.get_full_path()),})        


def calendar_by_cn(request, country,template_name="schedule/calendar_cn.html"):
    """
    """
    model = Event
    calendar = get_object_or_404(Calendar, slug='calendar')
    try:
        date = coerce_date_dict(request.GET)
    except ValueError:
        raise Http404

    if date:
        try:
            date = datetime.datetime(**date)
        except ValueError:
            raise Http404
    else:
        date = timezone.now()
        

    calendar = get_object_or_404(Calendar, slug='calendar')
    country = get_object_or_404(CountryPage, name=country)
    event_list= calendar.event_set.filter(country__country_slug=country)
    user = request.user 
    userprofile = get_object_or_404(IppcUserProfile, user_id=user.id)
    

    #return render_to_response(template_name, {
    #    'calendar': calendar,
    #    'weekday_names': weekday_names,
    #    'event_list': event_list,
    #    'here': quote(request.get_full_path()),
    #    'country' : country
    #    
    #}, context_instance=RequestContext(request), )
    return TemplateResponse(request, template_name, {  'userprofile':userprofile, 'calendar': calendar,        'weekday_names': weekday_names,        'event_list': event_list,        'here': quote(request.get_full_path()),        'country' : country},)        


def calendar_by_periods(request, calendar_slug, periods=None, template_name="schedule/calendar_by_period.html"):
    """
    This view is for getting a calendar, but also getting periods with that
    calendar.  Which periods you get, is designated with the list periods. You
    can designate which date you the periods to be initialized to by passing
    a date in request.GET. See the template tag ``query_string_for_date``

    Context Variables

    ``date``
        This was the date that was generated from the query string.

    ``periods``
        this is a dictionary that returns the periods from the list you passed
        in.  If you passed in Month and Day, then your dictionary would look
        like this

        {
            'month': <schedule.periods.Month object>
            'day':   <schedule.periods.Day object>
        }

        So in the template to access the Day period in the context you simply
        use ``periods.day``.

    ``calendar``
        This is the Calendar that is designated by the ``calendar_slug``.

    ``weekday_names``
        This is for convenience. It returns the local names of weekedays for
        internationalization.

    """
    user = request.user   
    can_add= 0 
    if user.groups.filter(name='IPPC Secretariat'):
        can_add=1
    calendar = get_object_or_404(Calendar, slug=calendar_slug)
    try:
        date = coerce_date_dict(request.GET)
    except ValueError:
        raise Http404

    if date:
        try:
            date = datetime.datetime(**date)
        except ValueError:
            raise Http404
    else:
        date = timezone.now()
    event_list = GET_EVENTS_FUNC(request, calendar)

    period_objects = dict([(period.__name__.lower(), period(event_list, date)) for period in periods])
    print(period_objects)
    return render_to_response(template_name, {
        'date': date,
        'periods': period_objects,
        'calendar': calendar,
        'weekday_names': weekday_names,
        'event_list': event_list,
        'can_add':can_add,
        'here': quote(request.get_full_path()),
    }, context_instance=RequestContext(request), )


def event(request, event_id, template_name="schedule/event.html"):
    """
    This view is for showing an event. It is important to remember that an
    event is not an occurrence.  Events define a set of reccurring occurrences.
    If you would like to display an occurrence (a single instance of a
    recurring event) use occurrence.

    Context Variables:

    event
        This is the event designated by the event_id

    back_url
        this is the url that referred to this view.
    """
    user = request.user
    is_contryeditor=0
    is_secretariat=0
    is_contryeevent=0
    is_registered=0
  
    event = get_object_or_404(Event, id=event_id)
    if event.country.id!=-1 :
        is_contryeevent=1
    if user.groups.filter(name='Country editor')  and (user.get_profile().country==event.country):
        is_contryeditor=1
    if user.groups.filter(name='IPPC Secretariat'):
        is_secretariat=1
    
    array_participants=[]    
    eventParticipants=EventParticipants.objects.filter(event_id=event_id)
    for u in eventParticipants:
        array_participants.append(u.user)
    if user in array_participants:
        is_registered=1
    else:
        is_registered=0
    
    event = get_object_or_404(Event, id=event_id)
    return render(request, template_name, {
        "event": event,
        "back_url": None,
        "is_contryeditor": is_contryeditor,
        "is_secretariat": is_secretariat,
        "is_contryeevent":is_contryeevent,
        "country":event.country,
        "is_registered":is_registered,
    })


def occurrence(request, event_id, template_name="schedule/occurrence.html", *args, **kwargs):
    """
    This view is used to display an occurrence.

    Context Variables:

    ``event``
        the event that produces the occurrence

    ``occurrence``
        the occurrence to be displayed

    ``back_url``
        the url from which this request was refered
    """
    event, occurrence = get_occurrence(event_id, *args, **kwargs)
    back_url = request.META.get('HTTP_REFERER', None)
    return render_to_response(template_name, {
        'event': event,
        'occurrence': occurrence,
        'back_url': back_url,
    }, context_instance=RequestContext(request))


@check_event_permissions
def edit_occurrence(request, event_id, template_name="schedule/edit_occurrence.html", *args, **kwargs):
    event, occurrence = get_occurrence(event_id, *args, **kwargs)
    next = kwargs.get('next', None)
    form = OccurrenceForm(data=request.POST or None, instance=occurrence)
    if form.is_valid():
        occurrence = form.save(commit=False)
        occurrence.event = event
        occurrence.save()
        next = next or get_next_url(request, occurrence.get_absolute_url())
        return HttpResponseRedirect(next)
    next = next or get_next_url(request, occurrence.get_absolute_url())
    return render_to_response(template_name, {
        'form': form,
        'occurrence': occurrence,
        'next': next,
    }, context_instance=RequestContext(request))


@check_event_permissions
def cancel_occurrence(request, event_id, template_name='schedule/cancel_occurrence.html', *args, **kwargs):
    """
    This view is used to cancel an occurrence. If it is called with a POST it
    will cancel the view. If it is called with a GET it will ask for
    conformation to cancel.
    """
    event, occurrence = get_occurrence(event_id, *args, **kwargs)
    next = kwargs.get('next', None) or get_next_url(request, event.get_absolute_url())
    if request.method != "POST":
        return render_to_response(template_name, {
            "occurrence": occurrence,
            "next": next,
        }, context_instance=RequestContext(request))
    occurrence.cancel()
    return HttpResponseRedirect(next)


def get_occurrence(event_id, occurrence_id=None, year=None, month=None, day=None, hour=None, minute=None, second=None):
    """
    Because occurrences don't have to be persisted, there must be two ways to
    retrieve them. both need an event, but if its persisted the occurrence can
    be retrieved with an id. If it is not persisted it takes a date to
    retrieve it.  This function returns an event and occurrence regardless of
    which method is used.
    """
    if(occurrence_id):
        occurrence = get_object_or_404(Occurrence, id=occurrence_id)
        event = occurrence.event
    elif(all((year, month, day, hour, minute, second))):
        event = get_object_or_404(Event, id=event_id)
        occurrence = event.get_occurrence(
            datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)))
        if occurrence is None:
            raise Http404
    else:
        raise Http404
    return event, occurrence

          
    
@check_event_permissions
def create_or_edit_event(request, country, calendar_slug, event_id=None, next=None, template_name='schedule/create_event.html', form_class=EventForm):
    """
    This function, if it receives a GET request or if given an invalid form in a
    POST request it will generate the following response

    Template:
        schedule/create_event.html

    Context Variables:

    form:
        an instance of EventForm

    calendar:
        a Calendar with id=calendar_id

    if this function gets a GET request with ``year``, ``month``, ``day``,
    ``hour``, ``minute``, and ``second`` it will auto fill the form, with
    the date specifed in the GET being the start and 30 minutes from that
    being the end.

    If this form receives an event_id it will edit the event with that id, if it
    recieves a calendar_id and it is creating a new event it will add that event
    to the calendar with the id calendar_id

    If it is given a valid form in a POST request it will redirect with one of
    three options, in this order

    # Try to find a 'next' GET variable
    # If the key word argument redirect is set
    # Lastly redirect to the event detail of the recently create event
    """
    user = request.user
    
    if country=='event':
        print()
    else:
        country = get_object_or_404(CountryPage, name=country)
    
    
    date = coerce_date_dict(request.GET)
    initial_data = None
    if date:
        try:
            start = datetime.datetime(**date)
            initial_data = {
                "start": start,
                "end": start + datetime.timedelta(minutes=30)
            }
        except TypeError:
            raise Http404
        except ValueError:
            raise Http404

    instance = None
    issues = None
    
    is_contryeevent=0
    is_secretariat=0
    is_contryeditor=0
    is_contryeditor_1=0
    can_add_edit=0
      
    if user.groups.filter(name='IPPC Secretariat'):
        is_secretariat=1
    if user.groups.filter(name='Country editor'):
        is_contryeditor=1
    if user.groups.filter(name='Country Contact Points'):
        is_contryeditor=1
    issueform =IssueKeywordsRelateForm(request.POST)
    calendar = get_object_or_404(Calendar, slug=calendar_slug)
    userprofile = get_object_or_404(IppcUserProfile, user_id=user.id)
  
    
    if event_id is not None:
        instance = get_object_or_404(Event, id=event_id)
        
      
        if user.groups.filter(name='Country editor') and (instance.country==userprofile.country):
            is_contryeditor_1=1
            can_add_edit=1  
        if instance.country.id!=-1 :
            is_contryeevent=1
        if (is_secretariat==1 and is_contryeevent==0):
            can_add_edit=1       
        if instance.issuename.count()>0:
            issues = get_object_or_404(IssueKeywordsRelate, pk=instance.issuename.all()[0].id)
            issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
        else:
            issueform =IssueKeywordsRelateForm(request.POST)
 
    else:
        instance = Event()
        if is_contryeditor==1:
            can_add_edit=1
        if (is_secretariat==1):
            can_add_edit=1  
    form = form_class(data=request.POST or None, instance=instance, initial=initial_data)
  
        
    if request.method == "POST":
       f_form = EventFileFormSet(request.POST, request.FILES,instance=instance)
       u_form = EventUrlFormSet(request.POST, instance=instance)
       p_form = EventParticipantsFormSet(request.POST, instance=instance)
       #issueform =IssueKeywordsRelateForm(request.POST,instance=issues)
    else:
       # issueform =IssueKeywordsRelateForm(instance=issues)
       f_form = EventFileFormSet(instance=instance)
       u_form = EventUrlFormSet(instance=instance)
       p_form = EventParticipantsFormSet(instance=instance)
  
    if form.is_valid() and f_form.is_valid() and u_form.is_valid() and  p_form.is_valid():
        event = form.save(commit=False)
        event.start=event.start + datetime.timedelta(hours=12)

        if user.groups.filter(name='Country editor'):
            event.country=user.get_profile().country
        event.creator = request.user
        event.calendar = calendar
        event.save()
        form.save_m2m()
      
      
       
        issue_instance = issueform.save(commit=False)
        issue_instance.content_object = event
        issue_instance.save()
        issueform.save_m2m()
        
        f_form.instance = event
        f_form.save()
        u_form.instance = event
        u_form.save()
        p_form.instance = event
        p_form.save()
        
        if event_id is not None: 
            print('edit')
        else:
           print('new')#sendemail
           send_notificationevent_message(event.id)
     
        next = next or reverse('event', args=[event.id])
        #next = get_next_url(request, next)
        return HttpResponseRedirect(next)

    #next = get_next_url(request, next)
 
    #return render_to_response(template_name, {
    #    "form": form,
    #    "issueform": issueform,
    #    "f_form": f_form,
    #    "u_form": u_form,
    #    "p_form": p_form,
    #    "calendar": calendar,
    #    "is_contryeditor":is_contryeditor,
    #    "is_contryeditor_1":is_contryeditor_1,        
    #    "is_secretariat":is_secretariat,
    #    "can_add_edit":can_add_edit,
    #    "event_id":event_id,
    #    "next": next
    #}, context_instance=RequestContext(request))
    return TemplateResponse(request, template_name, { "userprofile":userprofile, "form": form,
        "issueform": issueform,
        "f_form": f_form,
        "u_form": u_form,
        "p_form": p_form,
        "calendar": calendar,
        "is_contryeditor":is_contryeditor,
        "is_contryeditor_1":is_contryeditor_1,        
        "is_secretariat":is_secretariat,
        "can_add_edit":can_add_edit,
        "event_id":event_id,
        "next": next},)        


@login_required
def register_to_event(request, id=None):
    """ register to event  """
    user = request.user
   
    author = user
    array_participants=[]
    if id:
        event = get_object_or_404(Event, id=id)
        eventParticipants=EventParticipants.objects.filter(event_id=id)
        for u in eventParticipants:
           array_participants.append(u.user)
        
        if user in array_participants:
            print("Already registered")
        else:
            print("registered") 
            instance = EventParticipants()
            instance.user=user
            instance.registered=1
            instance.registered_date=timezone.now() 
            instance.event=event
            instance.save()
            send_notification_register_event_message(1,event.id,user)
     
            info(request, ("Successfully Registered to Event."))
            
      
        next=None
        next = next or reverse('event', args=[event.id])
        next = get_next_url(request, next)
        return HttpResponseRedirect(next)

        
    

@login_required
def unregister_to_event(request, id=None):
    """ un-register to event  """
    user = request.user
    array_participants=[]
    if id:
        eventParticipants=get_object_or_404(EventParticipants, user_id=user.id, event_id=id)
        eventParticipants.delete()
        info(request, ("Successfully Un-Registered to Event."))
        send_notification_register_event_message(0,id,user)
      
        print('un-registered')
            
        next=None
        next = next or reverse('event', args=[id])
        next = get_next_url(request, next)
        return HttpResponseRedirect(next)

@check_event_permissions
def resend_invite(request, id=None):
    """ resend_invite to event  """
    send_notificationevent_message(id)

    info(request, ("Successfully re-sent invite to Event."))


    next=None
    next = next or reverse('event', args=[id])
    next = get_next_url(request, next)
    return HttpResponseRedirect(next)



class DeleteEventView(DeleteView):
    template_name = 'schedule/delete_event.html'
    pk_url_kwarg = 'event_id'
    model = Event

    def get_context_data(self, **kwargs):
        ctx = super(DeleteEventView, self).get_context_data(**kwargs)
        ctx['next'] = self.get_success_url()
        return ctx

    def get_success_url(self):
        """
        After the event is deleted there are three options for redirect, tried in
        this order:

        # Try to find a 'next' GET variable
        # If the key word argument redirect is set
        # Lastly redirect to the event detail of the recently create event
        """
        next = self.kwargs.get('next') or reverse('day_calendar', args=[self.object.calendar.slug])
        next = get_next_url(self.request, next)
        return next

    ## Override dispatch to apply the permission decorator
    @method_decorator(login_required)
    @method_decorator(check_event_permissions)
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteEventView, self).dispatch(request, *args, **kwargs)


def check_next_url(next):
    """
    Checks to make sure the next url is not redirecting to another page.
    Basically it is a minimal security check.
    """
    if not next or '://' in next:
        return None
    return next


def get_next_url(request, default):
    next = default
    if OCCURRENCE_CANCEL_REDIRECT:
        next = OCCURRENCE_CANCEL_REDIRECT
    if 'next' in request.REQUEST and check_next_url(request.REQUEST['next']) is not None:
        next = request.REQUEST['next']
    return next


def api_occurrences(request):
    utc=pytz.UTC
    start = utc.localize(datetime.datetime.utcfromtimestamp(float(request.GET.get('start'))))
    end = utc.localize(datetime.datetime.utcfromtimestamp(float(request.GET.get('end'))))
    calendar = get_object_or_404(Calendar, slug=request.GET.get('calendar_slug'))
    response_data =[]
    for event in calendar.events.filter(start__gte=start, end__lte=end):
        occurrences = event.get_occurrences(start, end)
        for occurrence in occurrences:
            response_data.append({
                "id": occurrence.id,
                "title": occurrence.title,
                "start": occurrence.start.isoformat(),
                "end": occurrence.end.isoformat(),
            })
    return HttpResponse(json.dumps(response_data), content_type="application/json")

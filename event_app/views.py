from django.http import HttpResponse
from django.shortcuts import render
from course_app.models import Course
from course_app.models import Stage
from .models import Language,Location,Mode,Authors,Collaborators,Topics,Producers,Sponsors
from django.shortcuts import redirect,get_object_or_404
from .models import Event
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView



# Create your views here.
def create_event(request):
    if request.method=='POST':
        keys=list(request.POST.keys())
        print(keys)
        key_list=keys[1:23]
        new_list={}
        for new in key_list:
            new_list[new]=request.POST[new]
            if 'event_mode' in new_list:
                print("hghjfhgfghf")
            else:
                print("not found")
        new_list["event_medium_of_communication"]=get_object_or_404(Language, id=int(new_list["event_medium_of_communication"]))
        new_list["event_location"]=get_object_or_404(Location, id=int(new_list["event_location"]))
        new_list["event_mode"]=get_object_or_404(Mode, id=int(new_list["event_mode"]))
        Event.objects.create(**new_list)
        event=Event.objects.get(id=Event.objects.last().id)
        authors=request.POST.getlist("event_authors")
        collaborators=request.POST.getlist("event_collab")
        producers=request.POST.getlist("event_producers")
        sponsors=request.POST.getlist("event_sponsors")
        topics=request.POST.getlist("event_topic")

        print(authors,"authors")
        for author in authors:
            authorid=Authors.objects.filter(id=author)
            event.event_authors.add(*authorid)
            print(event.event_authors)
        for collab in collaborators:
            collabid=Collaborators.objects.filter(id=collab)
            event.event_collab.add(*collabid)
        for producer in producers:
            producerid=Producers.objects.filter(id=producer)
            event.event_producers.add(*producerid)
        for sponsor in sponsors:
            sponsorid=Sponsors.objects.filter(id=sponsor)
            event.event_sponsors.add(*sponsorid)
        for topic in topics:
            topicid=Topics.objects.filter(id=topic)
            event.event_topic.add(*topicid)
        new_list={}
    communication=Language.objects.all()
    locations=Location.objects.all()
    modes=Mode.objects.all()
    authors=Authors.objects.all()
    collaborators=Collaborators.objects.all()
    topics=Topics.objects.all()
    producers=Producers.objects.all()
    sponsors=Sponsors.objects.all()
    key={}
    key['communication']=communication
    key['locations']=locations
    key["locations"]=locations
    key['modes']=modes
    key['authors']=authors
    key["collaborators"]=collaborators
    key["topics"]=topics
    key["producers"]=producers
    key["sponsors"]=sponsors
    return render(request,'event.html', key)

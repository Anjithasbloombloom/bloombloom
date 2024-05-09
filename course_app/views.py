# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic, View
from .models import  Course
from .forms import CourseForm
from django.shortcuts import render, redirect
from .models import Course_temp
from .models import Videos  

# Create your views here.
def index(request):
    return render(request,'course.html')

from django.shortcuts import redirect,get_object_or_404
from .forms import CourseForm
from .models import Authors, Language, Location, Collaborators, Mode, Sponsors, Topics, Producers, Course

def create_course(request):
    if request.method == 'POST':
        keys = list(request.POST.keys())
        keys_part = keys[1:22]
        newdict={}
        for key in keys_part:
            newdict[key]=request.POST[key]
        newdict["course_medium_of_communication"]=get_object_or_404(Language, id=int(newdict["course_medium_of_communication"]))
        newdict["course_location"]=get_object_or_404(Location, id=int(newdict["course_location"]))
        newdict["course_mode"]=get_object_or_404(Mode, id=int(newdict["course_mode"]))
        Course.objects.create(**newdict)
        course = Course.objects.get(id=Course.objects.last().id)
        authors = request.POST.getlist('course_authors')
        collaborators=request.POST.getlist('course_collab')
        sponsors=request.POST.getlist('course_sponsors')
        producers=request.POST.getlist('course_producers')
        topics=request.POST.getlist('course_topic')


        for author in authors:
            authorid = Authors.objects.filter(id=author)
            course.course_authors.add(*authorid)
        for collab in collaborators:
            collabid=Collaborators.objects.filter(id=collab)
            course.course_collab.add(*collabid)
        for sponsor in sponsors:
            sponsorid=Sponsors.objects.filter(id=sponsor)
            course.course_sponsors.add(*sponsorid)
        for producer in producers:
            producerid=Producers.objects.filter(id=producer)
            course.course_producers.add(*producerid)
        for topic in topics:
            topicid=Topics.objects.filter(id=topic)
            course.course_topic.add(*topicid)
        newdict={}
    else:
       pass
    languages=Language.objects.all()
    locations=Location.objects.all()
    authors=Authors.objects.all()
    collaborators=Collaborators.objects.all()
    modes=Mode.objects.all()
    topics=Topics.objects.all()
    sponsors=Sponsors.objects.all()
    producers=Producers.objects.all()
    data={}
    data['languages']=languages
    data['locations']=locations
    data['authors']=authors
    data['collaborators']=collaborators
    data['modes']=modes
    data['topics']=topics
    data['producers']=producers
    data['sponsors']=sponsors
    return render(request, 'selected.html', data)


class select_featured(View):
    def get(self,request,id):
         b= Course.objects.get(id=id)
         author_objects=b.course_authors.filter(courses=b.id)
         setattr(b, 'author_objects', author_objects)
         sponser_objects=b.course_sponsors.filter(courses=b.id)
         setattr(b, 'sponser_objects', sponser_objects)
         return render(request,'selected_featured.html',{'b':b})
    def post(self,request,id):
        b = Course.objects.get(id=id)
        b.course_name = request.POST.get('course_name')
        b.course_description=request.POST.get('course_description')
        b.course_date=request.POST.get('course_date')
        b.course_price=request.POST.get('course_price')
        b.course_learning_credits=request.POST.get('course_learning_credits')
        b.course_rating=request.POST.get('course_rating')
        course_mode_id = request.POST.get('course_mode')
        course_mode_instance = Mode.objects.get(id=course_mode_id)
        print("course_mode_instance:", course_mode_instance)
        # b.course_mode = course_mode_instance.id
        b.course_mode_id = course_mode_instance.id
        course_location_id = request.POST.get('course_location')
        print("course_location_id",course_location_id)
        course_location_instance = Location.objects.get(id=course_location_id)
        b.course_location_id = course_location_instance.id
        b.save()
        return redirect('/page/')

def page(request):
    key =Course.objects.all()
    print("trai",key)
    return render(request, 'id.html', {'key': key})

def delete(request,id):
    b=Course.objects.get(id=id)
    b.delete()

from django.http import HttpResponseNotAllowed
class AddNewCourse(View):
    def post(self, request, id):
      if Course_temp.objects.filter(course_id=id).exists():
       return HttpResponseNotAllowed(['POST'])
      else:
        course_id=Course.objects.get(id=id)
        course_name = request.POST.get('course_name')
        course_description = request.POST.get('course_description')
        course_date = request.POST.get('course_date')
        course_mode_id = request.POST.get('course_mode')
        course_mode_instance = Mode.objects.get(id=course_mode_id)
        course_price=request.POST.get('course_price')
        course_learning_credits=request.POST.get('course_learning_credits')
        course_location_id = request.POST.get('course_location')
        course_location_instance = Location.objects.get(id=course_location_id)
        course_rating=request.POST.get('course_rating')
        authors_ids = request.POST.getlist('course_authors')
        authors = Authors.objects.filter(id__in=authors_ids)
        Sponsors_ids = request.POST.getlist('course_sponsors')
        sponsors = Sponsors.objects.filter(id__in=Sponsors_ids)

        course_temp = Course_temp.objects.create(
            course_name=course_name,
            course_description=course_description,
            course_date=course_date,
            course_mode_id=course_mode_id,
            course_price=course_price,
            course_id=course_id,
            course_learning_credits=course_learning_credits,
            course_location_id=course_location_id,
            course_rating=course_rating, 
        )
        course_temp.course_authors.set(authors)
        course_temp.course_sponsors.set(sponsors)
        return redirect('/page/')

def detail(request):
    tag =Sponsors.objects.all()
    last_course = Course_temp.objects.last()
    print(last_course)
    if last_course:
        last_course_authors = last_course.course_authors.all()  # Get the authors associated with the last course
        return render(request, 'detail.html', {'last_course_authors': last_course_authors})
    return render(request,'detail.html',{'tag': tag})

def latest_lauches(request):
    popOnDemand=Course.objects.all().order_by('-course_num_interested').values()
    latest=Course.objects.all().order_by('-course_date').values()
    return render(request,'detail.html',{'latest':latest, 'popOnDemand':popOnDemand})

 
def indexes(request):
    vidioes=Videos.objects.all()
    return render(request,"indexes.html",{"vidioes":vidioes})    








from lib2to3.pgen2 import driver
from translate import Translator
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group

from silmarin.forms import Access
from silmarin.models import Being, Silmarillion, Person, Status


def quests(request):
    user = request.user
    if user.is_authenticated:
        par = Person.objects.get(user=user)
        context = {
            'name': par.user,
            'specie': user.first_name,
            'position': par.position,
            'status': par.status,
        }
        if user.groups.filter(name="Гильдмастер").exists():
            print(context)
            # be = Being.objects.get(id_being_id=user.id)
            beings = Being.objects.all()
            print(beings)
            tryGet = [0 for i in range(len(beings))]
            return render(request, "quests.html", {"beings": beings, "tryGet": tryGet, "par": context})
        else:
            print("bbbbb")

            creature = []
            beings = Being.objects.all()
            tryGet = [0 for i in range(len(beings))]
            specie = Being.objects.filter(name=user.first_name).values_list('specie', flat=True).first()
            print(specie)
            for i in range(len(beings)):
                if beings[i].specie == specie:
                    creature.append(beings[i])
            print(creature)
            return render(request, "quests.html", {"beings": creature, "tryGet": tryGet, "par": context})
    else:
        return render(request, 'NoEnter.html')

def time(request):
    user = request.user
    print(user)
    if user.is_authenticated:
        groups = Silmarillion.objects.all()
        return render(request, "time.html", {"groups": groups})

def view(request):
   print("dddd")
   user = request.user
   if user.is_authenticated:
       par = Person.objects.get(user = user)
       context = {
           'name': par.user,
           'specie': user.first_name,
           'position': par.position,
           'status': par.status,
       }
       if user.groups.filter(name="Гильдмастер").exists():
          #be = Being.objects.get(id_being_id=user.id)
          beings = Being.objects.all()
          tryGet = [0 for i in range(len(beings))]
          return render(request, "silmarinfo.html", {"beings": beings, "tryGet": tryGet, "par": context})
       else:
           creature=[]
           beings = Being.objects.all()
           tryGet = [0 for i in range(len(beings))]
           specie = Being.objects.filter(name=user.first_name).values_list('specie', flat=True).first()
           for i in range(len(beings)):
              if beings[i].specie == specie:
                  creature.append(beings[i])
           return render(request, "silmarinfo.html", {"beings": creature, "tryGet": tryGet, "par": par})
   else:
      return render(request, 'NoEnter.html')


def show_index(request):
    if request.method == "GET":
        cur_user = request.user
        if cur_user.is_authenticated:
            return redirect('/info')
        else:
            return render(request, 'login.html')
    else:
        username = request.POST.get('logename_l')
        if (request.POST.get("logename_l") == ""):
            username = request.POST.get("logemail")
            password = request.POST.get("logpass")
            if (request.POST.get("logemail") != None and request.POST.get("logpass") != None):
              username = request.POST.get("logemail")
              password = request.POST.get("logpass")
              user = authenticate(username=username, password=password)
              try:
                login(request, user)
                return redirect("/info")
              except:
                 print("Ты не пройдешь")
                 return redirect("/")
            else:
              return render(request, 'NoEnter.html')
        else:
            username = request.POST.get('logename_l')
            first_name = request.POST.get("state")
            email = request.POST.get("logemail_l")
            password = request.POST.get("logpass_s")
            if (request.POST.get("logemail_l") != None and request.POST.get("logpass_s") != None):
               user = User.objects.create_user(email=email, username=username, first_name=first_name, password=password)
               specie = Being.objects.filter(name=user.first_name).values_list('specie', flat=True).first()
               status = Status.objects.get(id=Being.objects.get(name=user.first_name).status_id)
               login(request, user)
               Person.objects.create(user=user, specie=specie, status=status,  position="Игрок")
               return redirect("/info")
            else:
               print("Ты не пройдешь")
               return redirect("/")


def show_map(request):
    if request.user.is_authenticated:
       return render(request, "Map.html")
    else:
        return render(request, 'NoEnter.html')

def acc(request):
    if request.user.is_authenticated:
       return render(request, "mypage.html")
    else:
        return render(request, 'NoEnter.html')



def secure(request, being_form_id):

    if request.user.is_authenticated:
       beings = Being.objects.all()
       if request.method == "GET":
          access = Access()
          return render(request, "templateForm.html", {"form": access})
       else:

          pas = "Tadam"
          form = Access(request.POST)
          if form.is_valid():
             result = form.cleaned_data.get("Password")
             if (result==pas):
               translator = Translator(from_lang="russian", to_lang="English")
               im = str(Being.objects.get(id=being_form_id).name)
               eng = translator.translate(im)
               return redirect("https://tolkiengateway.net/wiki/Category:Images_of_"+eng)
             else:
               tryGet = [0 for i in range(len(beings))]
               tryGet[being_form_id] = 1
               return render(request, "silmarinfo.html", {"beings": beings, "tryGet":tryGet})
    else:
       return render(request, 'NoEnter.html')
# Create your views here.

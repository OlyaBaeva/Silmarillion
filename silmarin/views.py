import io
from lib2to3.pgen2 import driver

from PIL import Image
from django.conf import settings
from django.contrib import messages
from django.core.files.images import ImageFile
from django.http import JsonResponse
from translate import Translator
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from silmarin.forms import Access
from silmarin.models import Being, Silmarillion, Person, Status, Quests, ActingCharacters


def quests(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "GET":
           par = Person.objects.get(user=user)
           context = {
              'name': par.user,
              'specie': user.first_name,
              'position': par.position,
              'status': par.status,
           }
           if user.groups.filter(name="Гильдмастер").exists():
              beings = Being.objects.all()
              tryGet = [0 for i in range(len(beings))]
              quests = Quests.objects.all()
              p = ActingCharacters.objects.all()
              pr = []
              for i in range(len(quests)):
                  person_ids = ActingCharacters.objects.filter(quest=quests[i]).values_list('people', flat=True)
                  people_id = Person.objects.filter(id__in=person_ids).values_list('user', flat=True)
                  people = User.objects.filter(id__in=people_id).values_list('username', flat=True)
                  pr.append([quests[i].name, list(people)])
              flag = True
              return render(request, "quests.html",
                          {"beings": beings, "tryGet": tryGet, "par": context, "quests": quests, "flag": flag, "people": pr})
           else:
              flag = False
              creature = []
              beings = Being.objects.all()
              tryGet = [0 for i in range(len(beings))]
              specie = Being.objects.filter(name=user.first_name).values_list('specie', flat=True).first()

              quests = Quests.objects.all()
              questforuser=[]
              for i in range(len(quests)):
                 if par.status in quests[i].statuses.all():
                    questforuser.append(quests[i])
              for i in range(len(beings)):
                if beings[i].specie == specie:
                    creature.append(beings[i])
              return render(request, "quests.html", {"beings": creature, "tryGet": tryGet, "par": context, "quests": questforuser, "flag": flag})
        else:
            if (request.POST.get('password')):
                new_password = request.POST.get('password')
                print(new_password)
                user.set_password(new_password)
                user.save()
                return redirect('/')
            elif(request.POST.get('list')):
                list_id = request.POST.getlist('list')

                for i in list_id:
                    user_instance = User.objects.get(username=i)
                    email = user_instance.email
                    #send_mail('Участие в квесте', 'Вы отправили заявку на участие в квесте', settings.EMAIL_HOST_USER, [email])
                    print(email)
                    return redirect('/')
            else:
               quest_id = request.POST.get('quest_id')
               person = Person.objects.get(user=request.user)
               if ActingCharacters.objects.filter(people=person):
                   messages.error(request, 'Вы уже отправляли заявку на участие в этом квесте')
                   return redirect('/')
               else:
                  try:
                     ActingCharacters.objects.create(id=ActingCharacters.objects.last().id+1, quest=Quests.objects.get(id=quest_id), people=Person.objects.get(user=request.user))
                     messages.success(request, 'Вы отправили заявку на участие в квесте')
                     print("Yes")
                     return redirect('/')
                  except:
                     messages.error(request, 'Что-то пошло не так, попробуйте еще раз')
                     return redirect('/')
    else:
      return render(request, 'NoEnter.html')



def time(request):
    user = request.user
    print(user)
    if user.is_authenticated:
        groups = Silmarillion.objects.all()
        return render(request, "time.html", {"groups": groups})

def forget(request):
   if request.method == "GET":
     return render(request, "password.html")
   else:
       email = request.POST.get("logemail_l")
       try:
         user = User.objects.get(email__exact=email)
       except:
         messages.error(request, 'Нет пользователя с таким email')
         return redirect('/password/')
       send_mail('Смена пароля', 'Ваш временный пароль: 123456a', settings.EMAIL_HOST_USER, [email])
       user.set_password("123456a")
       user.save()
       return redirect('/')


'''    
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
          return render(request, "quests.html", {"beings": beings, "tryGet": tryGet, "par": context})
       else:
           creature=[]
           beings = Being.objects.all()
           tryGet = [0 for i in range(len(beings))]
           specie = Being.objects.filter(name=user.first_name).values_list('specie', flat=True).first()
           for i in range(len(beings)):
              if beings[i].specie == specie:
                  creature.append(beings[i])
           return render(request, "quests.html", {"beings": creature, "tryGet": tryGet, "par": par})
   else:
      return render(request, 'NoEnter.html')
'''

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
               user_group = Group.objects.get(name='Игрок')
               user_group.user_set.add(user)
               Person.objects.create(user=user, specie=specie, status=status,  position="Игрок")
               return redirect("/info")
            else:
               print("Ты не пройдешь")
               return redirect("/")


def show_map(request):
    if request.user.is_authenticated:
        return render(request, 'Map.html')
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
               if eng.split()[0]=="Torin":
                   eng="Thorin"
               if im == "Древень":
                   eng="Treebeard"
               return redirect("https://tolkiengateway.net/wiki/Category:Images_of_"+eng)
             else:
               tryGet = [0 for i in range(len(beings))]
               tryGet[being_form_id] = 1
               return render(request, "silmarinfo.html", {"beings": beings, "tryGet":tryGet})
    else:
       return render(request, 'NoEnter.html')
# Create your views here.

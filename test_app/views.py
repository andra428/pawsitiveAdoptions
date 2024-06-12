from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
import os
from django.core.paginator import Paginator
from django.core.mail import BadHeaderError, send_mail
from django.conf import settings
from test_app.helpers import experienceScore, housingEnvScore, saveCustomUserAnimalScore, findCompatibleAnimals, saveMessages,\
                            updateMessages, whichSenderReceiver, getMessages, animalGotAdopted, scrapePetfinderArticles, \
                            extractContentFromArticle, getLatestMessage, getCorespondent, getOwner

def home(request):
    from .models import Animal
    pets = Animal.objects.all().order_by('name')
    paginator = Paginator(pets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})

def search_pets(request):
    return render(request, 'search.html')

@csrf_exempt
def findPets(request):
    from .models import Animal
    mesaj=""
    if request.method == 'POST':
        animal = request.POST.get('animal_search')
        race = request.POST.get('breed')
        size = request.POST.get('size')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        type_age = request.POST.get('type_age')
        details = request.POST.getlist('details')
        
        pets=Animal.objects.all()

        if animal:
            pets = pets.filter(Q(animal__iexact=animal))
            
        if race:
            race=race.capitalize()
            pets = pets.filter(race__icontains=race)
            
        if size:
            pets=pets.filter(Q(size__iexact=size))
        if gender:
            pets = pets.filter(Q(gender__iexact=gender))
        
        if type_age:
            pets = pets.filter(type_age__contains=type_age)
            if age:
                pets=pets.filter(age__icontains=age)
            if age=="":
               
                if type_age=="Weeks":
                    age_threshold = 4
                    pets = pets.filter(Q(age__lte=age_threshold))
                if type_age=="Months":
                    age_threshold = 12
                    pets = pets.filter(Q(age__lt=age_threshold))
                if type_age=="Years":
                    age_threshold = 1
                    pets = pets.filter(Q(age__gte=age_threshold))
        for i in details:
            pets=pets.filter(description__icontains=i)
        if pets:
            mesaj=""
        else:
            mesaj="There aren't animals that fit this description"
        context={
        "pets":pets,
        "mesaj": mesaj
    }
       
        return render(request,'search.html',context)
    else:
        return HttpResponse("Form submission method not allowed")


def details(request,idAnimal):
    from .models import Animal, CustomUserIdleId
    if idAnimal:
        pets = Animal.objects.get(id=idAnimal)
        print(pets)
    else:
        pets = Animal.objects.all()

    if pets:
        custom_user_idle_ids = CustomUserIdleId.objects.filter(idle=pets.id)
    if custom_user_idle_ids: 
        hasOwner = 1
        for c in custom_user_idle_ids:
            ownerFirstName = c.customuser.first_name
            ownerLastName = c.customuser.last_name
            ownerPhone = c.customuser.phone
            ownerEmail = c.customuser.username
    else:
        hasOwner = 0
        ownerFirstName = ""
        ownerLastName = ""
        ownerEmail = ""
        ownerPhone = ""
    context={
        "pets":pets,
        "hasOwner":hasOwner,
        "ownerFirstName": ownerFirstName,
        "ownerLastName": ownerLastName,
        "ownerPhone": ownerPhone,
        "ownerEmail":ownerEmail
    }
    return render(request, 'details.html', context)

def about(request):
    return render(request, 'adoptionProcess.html')

def aboutGiving(request):
    return render(request, 'givingProces.html')

def about_dogs(request):
    return render(request, 'aboutDogs.html')

def about_cats(request):
    from .models import Animal
    pets = Animal.objects.all()
    return render(request, 'home.html', {'pets': pets})

def singup(request):
    return render(request, 'signup.html')

def loginPagina(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        return render(request, 'account.html')

def logout_view(request):
    from .models import Animal
    pets = Animal.objects.all().order_by('name')
    paginator = Paginator(pets, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    logout(request)
    return render(request, 'home.html', {'page_obj': page_obj})

    
def loginAdoptator(request):
    
    username = request.POST["username"]
    password = request.POST["password"]
    mesaj=""
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        mesaj="Welcome, "+ user.first_name
        context={
            "mesaj":mesaj
        }
        print("Success")
        return render(request, 'account.html',context)
    else:
        mesaj="Username or password wrong!"
        print("Eroare la login")
        context={
            "mesaj":mesaj
        }
        return render(request, 'login.html',context)


def createUserAdoptator(request):
    from .models import CustomUser
    lastname = request.POST.get('lastname')
    firstname = request.POST.get('firstname')
    password = request.POST.get('password')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    role = request.POST.get('adopt')
    animal = request.POST.get('animal')
    race = request.POST.get('race')
    size = request.POST.get('size')
    hair = request.POST.get('hair')
    gender = request.POST.get('gender')
    age = request.POST.get('age')
    type_age = request.POST.get('type_age')
    housing = request.POST.getlist('housing')
    exp_his = request.POST.getlist('exp_his')
    description = request.POST.getlist('description')
    address = request.POST.get('address')
    mesaj = ""
    if lastname is None or lastname=="":
        mesaj="The last name field must be filled in!"
        context={
        "mesaj":mesaj
        }
        return render(request, 'signup.html',context)
    if firstname is None or firstname=="":
        mesaj="The first name field must be filled in!"
        context={
        "mesaj":mesaj
        }
        return render(request, 'signup.html',context)
    if email is None or email=="":
        mesaj="The email field must be filled in!"
        context={
        "mesaj":mesaj
        }
        return render(request, 'signup.html',context)
    if phone is None or phone=="":
        mesaj="The phone field must be filled in!"
        context={
        "mesaj":mesaj
        }
        return render(request, 'signup.html',context)
    if password is None or password=="":
        mesaj="The password field must be filled in!"
        context={
        "mesaj":mesaj
        }
        return render(request, 'signup.html',context)
    
    else:
        r=1
        if role == "Adopt":
            r=1
        else:
            r=0
            if address is None or address=="":
                mesaj="The address field must be filled in!"
                context={
                "mesaj":mesaj
                }
                return render(request, 'signup.html',context)
        housing2 = ""
        for h in housing:
            housing2= housing2 + h +"."
        exp_his2 = ""
        for eh in exp_his:
            exp_his2= exp_his2 + eh +"."
        description2 = ""
        for i in description:
            description2 = description2 + i + "."
        
        if age is None or age == "":
            age = None
        if type_age is None or type_age == "":
            type_age = None
        try : 
            user = CustomUser(
                username = email,
                first_name = firstname,
                last_name = lastname,
                email = email,
                phone= phone,
                role=r,
                animal=animal,
                race=race,
                age = age,
                type_age = type_age,
                size = size,
                hair = hair,
                gender = gender,
                description = description2,
                housing_environment = housing2,
                experience_history = exp_his2, 
                address=address
            )
            user.set_password(password)
            user.save()
            mesaj="Welcome, "+user.first_name
            context={
                "mesaj":mesaj
            }
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
            return render(request, 'account.html',context)
        except Exception as e :
            print(e)
            mesaj="Something went wrong!"
            context ={
                "mesaj":mesaj
            }
            return render(request, 'signup.html',context)

def accountView(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        return render(request, 'account.html')
    
def showCompatibleAnimals(request):
    from .models import Animal
    pets = Animal.objects.all()
    user = request.user
    mesaj=""
    pets = pets.filter(adopted=0)
    if user.animal is not None:
        pets = pets.filter(Q(animal__iexact=user.animal))
    if user.race is not None:
        if user.race != "Open to any breed":
            pets = pets.filter(Q(race__iexact=user.race))
    if user.type_age is not None and user.type_age!="":
        pets = pets.filter(Q(type_age__iexact=user.type_age))
    if user.age is not None and user.age!="":
        pets = pets.filter(Q(age__iexact=user.age))
    if user.size is not None and user.size!="":
        pets = pets.filter(Q(size__iexact=user.size))
    if user.hair is not None and user.hair!="":
        pets = pets.filter(Q(hair__iexact=user.hair))
    if user.gender is not None and user.gender!="":
        pets = pets.filter(Q(gender__iexact=user.gender))
    if user.description is not None and user.description!="":
        pets = findCompatibleAnimals(user.description,pets)
        
    if pets.exists():
        mesaj=""
    else:
        mesaj = "There are no animals that fit that exact criteria!"
    context={
        "pets":pets,
        "mesaj":mesaj
    }
    return render(request,'account.html',context)

def updateAnimalPreferencesView(request):
    user = request.user
    animal=""
    age=""
    size=""
    hair=""
    gender=""
    description = ""
    type_age=""
    housingEnv = ""
    experience = ""
    race=""
    if user.animal is None:
        animal="No preferences"
    else :
        animal=user.animal
    if user.age is None or user.age == "":
        age = ""
    else:
        age = user.age
       
    if user.type_age is None or user.type_age == "":
        type_age = "No preferences"
    else:
        type_age = user.type_age
        
    if user.race is None or user.race == "Open to any breed":
        race = "Open to any breed"
    else:
        race=user.race
    if user.size is None or user.size=="":
        size="No preferences"
    else:
        size=user.size
    if user.hair is None or user.hair=="":
        hair="No preferences"
    else:
        hair=user.hair
    if user.gender is None or user.gender=="":
        gender="No preferences"
    else:
        gender=user.gender
    if user.description is None:
        description="No preferences"
    else:
        description=user.description
    housingEnv = user.housing_environment
    experience = user.experience_history
    context = {
        "uap": 1,
        "animal":animal,
        "age":age,
        "size":size,
        "hair":hair,
        "gender": gender,
        "description":description,
        "type_age":type_age,
        "race":race,
        "housingEnv" : housingEnv,
        "experience":experience
    }    
    
    return render(request,'account.html', context)

def updateAnimalPreferences(request):
    user=request.user
    animal = request.POST.get('animal2')
    race = request.POST.get('breed2')
    size = request.POST.get('size2')
    hair = request.POST.get('hair2')
    gender = request.POST.get('gender2')
    age = request.POST.get('age2')
    type_age = request.POST.get('type_age2')
    description = request.POST.getlist('details2')
    description2 = request.POST.get('description2')
    housing = request.POST.getlist('housing2')
    housing2 = request.POST.get('housingEnv')
    housing = request.POST.getlist('housing2')
    housing2 = request.POST.get('housingEnv')
    exp_his = request.POST.getlist('exp_his2')
    exp_his2 = request.POST.get('experience')
    mesaj=""
    
    if animal != user.animal:
        user.animal = animal
    if race != user.race:
        user.race = race
    if size != user.size:
        if size != "No preferences":
            user.size = size
        else:
            user.size=None
    if hair != user.hair:    
        if hair != "No preferences":        
            user.hair = hair
        else:
            user.hair=None
    if gender != user.gender:
        if gender != "No preferences":
            user.gender = gender
        else:
            user.gender=None
    if age != user.age and age!="" and age is not None:
        user.age = age
    else:
        user.age = None
    
    if type_age != user.type_age and type_age != "" and type_age is not None and type_age != "No preferences":
        user.type_age = type_age
    else:
        user.type_age = None
    
    if description2 != user.description:
        user.description = description2 + "."
    if description is not None:
        for d in description:
            user.description = user.description + d + "."
   
    if housing2 != user.housing_environment:
        user.housing_environment = housing2  + "."
    if housing is not None:
        for h in housing:
            user.housing_environment = user.housing_environment + h + "."
    
    if exp_his2 != user.experience_history:
        user.experience_history = exp_his2  + "."
    if exp_his is not None:
        for eh in exp_his:
            user.experience_history = user.experience_history + eh + "."

    try:
        user.save()
        mesaj = "The changes were succesfully applied!"
    except Exception as e:
        mesaj = "The changes could not be applied!"
        print(e)

    context={
        "mesaj":mesaj
    }
    return render(request, 'account.html',context)
def updatePersonalInfoView(request):
    user = request.user
    upi=1
    context={
        "upi":upi,
        "firstname":user.first_name,
        "lastname":user.last_name,
        "email":user.email,
        "phone":user.phone
    }

    return render(request, 'account.html',context)

def updatePersonalInfo(request):
    user=request.user
    lastname=request.POST.get('lastname2')
    firstname=request.POST.get('firstname2')
    email = request.POST.get('email2')
    phone = request.POST.get('phone2')
    pass1 = request.POST.get('password2')
    pass2 = request.POST.get('password3')
    mesaj=""
    if pass1 is not None and pass1!="":
        if pass2 is not None and pass2!="":
            if pass1 != pass2:
                mesaj = "The password must must match!"
                context={
                "mesaj":mesaj
                }
                return render(request, 'account.html',context)
    if user.first_name!=firstname:
        user.first_name=firstname
    if user.last_name!=lastname:
        user.last_name = lastname
    if user.username != email:
        user.username = email
    if user.email != email:
        user.email = email
    if user.phone != phone:
        user.phone = phone

    try:
        if pass1 is not None and pass1!="":
            if pass2 is not None and pass2!="":
                if pass1==pass2:
                    user.set_password(pass1)
        
        user.save()
        mesaj = "The changes were succesfully applied!"
    except Exception as e:
        mesaj = "The changes could not be applied!"
        print(e)

    context={
        "mesaj":mesaj
    }
    return render(request, 'account.html',context)

def postAnAnnouncementView(request):
    mesaj=""
    paav = 1
    context={
        "mesaj":mesaj,
        "paav":paav
    }
    return render(request,"account.html", context)

def postAnAnnouncement(request):
    from .models import Animal, CustomUserIdleId
    user=request.user
    path = request.FILES['path']
    animal_input = request.POST.get('animal3')
    race = request.POST.get('breed3')
   
    weight = request.POST.get('weight')
    size = request.POST.get('size3')
    hair = request.POST.get('hair3')
    gender = request.POST.get('gender3')
    age = request.POST.get('age3')
    type_age = request.POST.get('type_age3')
    description = request.POST.getlist('details3')
    file_name = path.name  
    adopted = 0
    description2 = ""
    name = request.POST.get('name_animal')
    if not all([path, animal_input, race, weight, size, hair, gender, age, type_age, name, description]):
        print("Some required fields are missing")
        paav = 1
        context={
            "mesaj":"All fields must be filled!",
            "paav":paav
        }
        return render(request,'account.html',context)
    else:
        print('proceed')
    directory = os.path.join('static', 'images', 'animals')

    new_path = os.path.join(directory, file_name)

    if os.path.exists(new_path):
       
        count = 1
        while True:
            new_file_name = f"{os.path.splitext(file_name)[0]}_{count}{os.path.splitext(file_name)[1]}"
            new_path = os.path.join(directory, new_file_name)
            if not os.path.exists(new_path):
                break
            count += 1
    with open(new_path, 'wb+') as destination:
        for chunk in path.chunks():
            destination.write(chunk)
        
    mesaj=""
    if race is not None or race != "":
        race = race.capitalize()
    
    for desc in description:
        description2 = description2+desc+"."
    try:
        animal = Animal(
            path=new_path,
            animal = animal_input,
            name=name,
            race=race,
            age=age,
            type_age=type_age,
            size=size,
            hair=hair,
            gender=gender,
            weight = weight,
            adopted=adopted,
            description = description2
        )
        animal.save()
        last_animal = Animal.objects.latest('id')
        last_animal_id = last_animal.id

        print(last_animal_id)
        legatura = CustomUserIdleId(
            customuser=user,
            idle = last_animal
        )
        legatura.save()
        mesaj="The pet was added to the database!"
    except Exception as e:
        mesaj = "The operation could not be made! Try again later!"

        print(e)
   
    context={
        "mesaj":mesaj
    }
    return render(request,'account.html',context)

def showAnimals(request):
    from .models import CustomUserIdleId
    user = request.user
    user_idle_ids = CustomUserIdleId.objects.filter(customuser=user)

    user_animals = []
    if user_idle_ids:
        for user_idle_id in user_idle_ids:
            user_animals.append(user_idle_id.idle)
    if user_animals:
        mesaj2 = ""
    else:
        mesaj2 = "No animals yet!"
    context = {
        "user_animals": user_animals,
        "mesaj2":mesaj2
    }
    return render(request, 'account.html',context)

def updateAnimalInfoView(request,idAnimal):
    from .models import CustomUserIdleId
    user = request.user
    user_idle_ids = CustomUserIdleId.objects.filter(customuser=user)
    user_animals = []
    if user_idle_ids:
        if idAnimal:
            user_animals = user_idle_ids.filter(idle_id=idAnimal)
    for animal in user_animals:
        path = animal.idle.path
        name2=animal.idle.name
        a = animal.idle.animal
        race = animal.idle.race
        age = animal.idle.age
        type_age = animal.idle.type_age
        size = animal.idle.size
        hair = animal.idle.hair
        gender = animal.idle.gender
        weight = animal.idle.weight
        description = animal.idle.description
    
    context={
        "uaiv":1,
        "path":path,
        "animal":a,
        "idAnimal":idAnimal,
        "name2":name2,
        "race":race,
        "age":age,
        "type_age":type_age,
        "size":size,
        "hair":hair,
        "gender":gender,
        "weight":weight,
        "type_age":type_age,
        "description":description
    }
    return render(request,'account.html',context)
    
def updateAnimalInfo(request,idAnimal):
    from .models import CustomUserIdleId
    user=request.user
    user_idle_ids = CustomUserIdleId.objects.filter(customuser=user)
    name2 = request.POST.get('name_animal2')
    animal = request.POST.get('animal4')
    race = request.POST.get('breed4')
    size = request.POST.get('size4')
    hair = request.POST.get('hair4')
    gender = request.POST.get('gender4')
    weight = request.POST.get('weight2')
    age = request.POST.get('age4')
    type_age = request.POST.get('type_age4')
    adopted_status = request.POST.get('adopt')
    description = request.POST.getlist('details4')
    description2 = request.POST.get('desc2')
    print(adopted_status)
    a = 0
    
    mesaj=""
    try:
        user_animals = []
        if user_idle_ids:
            if idAnimal:
                user_animals = user_idle_ids.filter(idle_id=idAnimal)
        for animall in user_animals:
            if request.FILES.get('path2'):
                animall.idle.path = request.FILES['path2']
            if animall.idle.name != name2:
                animall.idle.name = name2
            if animall.idle.animal != animal:
                animall.idle.animal = animal
            if animall.idle.race != race:
                animall.idle.race = race
            if animall.idle.size != size:
                animall.idle.size = size
            if animall.idle.hair != hair:
                animall.idle.hair = hair
            if animall.idle.gender != gender:
                animall.idle.gender = gender
            if animall.idle.weight != weight:
                animall.idle.weight = weight
            if animall.idle.type_age != type_age:
                animall.idle.type_age = type_age
            if animall.idle.age != age:
                animall.idle.age = age
            if adopted_status=="Yes":
                a = 1
                print(a)
                if animall.idle.adopted!=a:
                    animall.idle.adopted=a
                    print( animall.idle.adopted)
                    animalGotAdopted(idAnimal)
            else:
                animalGotAdopted(idAnimal)
            if description2 != animall.idle.description:
                animall.idle.description = description2  + "."
            if description is not None:
                for d in description:
                    animall.idle.description = animall.idle.description + d + "."
            animall.idle.save()
        mesaj = "The changes were succesfully applied!"
    except Exception as e:
        mesaj = "The changes could not be applied!"
        print(e)

    context={
        "name2":name2,
        "mesaj":mesaj
    }
    return render(request, 'account.html',context)

def deleteAnimal(request, idAnimal):
    from .models import Animal
    if request.method == 'POST':
        try:
            animal = Animal.objects.get(id=idAnimal)
            animal.delete()
            mesaj = "Animal deleted successfully!"
            
        except Animal.DoesNotExist:
            mesaj= "Animal does not exist!"
           
    else:
        mesaj = "Something went wrong! Please try again later!"
    context = {
        "mesaj":mesaj,
        "idAnimal":idAnimal
    }
    return render(request, 'account.html',context)

def considerForAdoptionView(request,idAnimal):
    from .models import Animal, CustomUserIdAnimalScore
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    elif request.user.role == 0:
        return render(request,'signup.html')
    else:
        user=request.user
        age = ""
        type_age = ""
        hair = ""
        size = ""
        gender = ""
        stars = []
        if user.age is None or user.age == "":
            age = "No preferences"
        else:
            age=user.type_age
        if user.type_age is not None and user.type_age !="":
            type_age=user.type_age
        if user.hair is None or user.hair =="":
            hair = "No preferences"
        else:
            hair = user.hair
        if user.size is None or user.size =="":
            size = "No preferences"
        else:
            size = user.size
        if user.gender is None or user.gender =="":
            gender = "No preferences"
        else:
            gender = user.gender
    
        userName = user.first_name
        pets = Animal.objects.all()
        pets = pets.filter(id=idAnimal)
        pets2=pets.get(id=idAnimal)
        props = [prop.strip() for prop in user.description.split('.') if prop.strip()]
        user1 = CustomUserIdAnimalScore.objects.filter(customuser=user,idAnimal=pets2.id).first()
        idAnimal = 0
        s = 0
        for pet in pets:
            idAnimal = pet
            petName= pet.name
            petID = pet.id
            print(petID)
            if user.animal == pet.animal:
                stars.append(5)
            else:
                stars.append(0)
            if pet.race == user.race:
                stars.append(5)
            elif user.race == "Open to any breed":
                stars.append(3.5)
            else:
                stars.append(0)
            if type_age == pet.type_age:
                if age == pet.age:
                    stars.append(5)
                elif age!=pet.age:
                    stars.append(4)
            else:
                if type_age=="":
                    stars.append(3.5)
            if pet.size==size:
                stars.append(5)
            elif size=="No preferences":
                stars.append(3.5)
            else:
                stars.append(0)
            if pet.hair == hair:
                stars.append(5)
            elif hair=="No preferences":
                stars.append(3.5)
            else:
                stars.append(0)
            if pet.gender==gender:
                stars.append(5)
            elif gender=="No preferences":
                stars.append(3.5)
            else:
                stars.append(0)
    
            for p in props:
                if p in pet.description:
                    s = s + 1
            
            stars.append(s)
            props2 = [prop.strip() for prop in pet.description.split('.') if prop.strip()]
            s2 = housingEnvScore(pet.animal, props2, user.housing_environment)
            s3 = experienceScore(pet.animal, props2, user.experience_history, pet.gender)
            stars.append(s2)
            stars.append(s3)
            suma = sum(stars)
            print(suma)
            score = int(round(suma/45,2) * 100)
            try:
                if score > 60 :
                    print("scor mai mare ca 60")
                    if user1:
                        print("user1")
                        if user1.state!="Inquiered" and user1.state!="Done":
                            print("in if")
                            saveCustomUserAnimalScore(user,idAnimal,score,s2,s3, "Interested")
                    else:
                        saveCustomUserAnimalScore(user,idAnimal,score,s2,s3, "Interested")
            except Exception as e:
                print(e)
            scoreText = str(score) + "% percentaje of compatibility"
            print(stars)
        context={
            "username":userName,
            "petName":petName,
            "idAnimal":petID,
            "user":user,
            "pets":pets,
            "age":age,
            "type_age":type_age,
            "hair":hair,
            "size":size,
            "gender":gender,
            "stars":stars,
            "scoreText":scoreText,
            "score":score

        }
        return render(request, 'considerForAdoption.html', context)
    
def ForwardAdopting(request, score, idAnimal):
    from .models import Animal, CustomUserIdAnimalScore, CustomUserIdleId
    mesaj = ""
    user = request.user
    print(idAnimal)

    
    user1 = CustomUserIdAnimalScore.objects.filter(customuser=user, idAnimal=idAnimal).first()
    users = CustomUserIdAnimalScore.objects.filter(idAnimal=idAnimal).exclude(customuser=user)
    animal = Animal.objects.filter(id=idAnimal).first()
    owner = CustomUserIdleId.objects.filter(idle=animal).first()
    print(owner.customuser.address)
    address= owner.customuser.address
    petName = animal.name
    check = 0
    #print(user1.state)
    if user1:
        if user1.state=="Inquiered" or user1.state=="Done":
            mesaj = "You already tried this way!"  
            print("tactu")
            check = 0
            context = {
                "mesaj":mesaj,
                "score":score,
                "idAnimal":idAnimal,
                "check":check,
                "petName":petName,
                 "address":address
            }
            return render(request, 'forwardAdopting.html',context)
    
    if score < 60:
        mesaj = "We don't believe you are matched well enough for this pet!"
        check = 0
        context = {
            "mesaj":mesaj,
            "score":score,
            "idAnimal":idAnimal,
            "check":check,
            "petName":petName,
            "address":address
        }
        return render(request, 'forwardAdopting.html',context)
    else:
        print("mata1")
        if users : 
            print("mata")
            for u in users:
                print(u.customuser.email)
                
                if u.state == "Inquiered" and user1.state == "Interested":
                    mesaj = "Someone is already ahead of you! Try again later!"
                    print(mesaj)
                    check = 0
                elif u.state == "Interested" and user1.state == "Interested":
                    if u.score==user1.score:
                        if u.ehScore + u.heScore > user1.ehScore + user1.heScore:
                            mesaj = "Someone is a litter better than you! Try again later!"
                            check = 0
                            print(mesaj)
                        else:
                            mesaj = "Are you prepared for this responsability?"
                            check = 1
                            print(mesaj)
                    elif u.score<=user1.score:
                        mesaj = "Are you prepared for this responsability?"
                        check = 1
                    else:
                        mesaj = "Someone has a higher score! Try again later!"
                        check = 0
                else:
                    mesaj = "Are you prepared for this responsability?"
                    check = 1
        else:
            mesaj = "Are you prepared for this responsability?"
            check = 1
    context = {
        "mesaj":mesaj,
        "score":score,
        "idAnimal":idAnimal,
        "check":check,
        "petName":petName,
        "address":address
    }
    return render(request, 'forwardAdopting.html',context)

def contactOwner(request,idAnimal):
    from .models import Animal, CustomUserIdleId, CustomUserIdAnimalScore
    if request.method == 'POST':
        user = request.user
        messageS = request.POST.get('startTime')
        message = request.POST.get('endDate')
        print(message)
        messagee = request.POST.get('endTime')
        print(messagee)
        mes = str(message) + " " + str(messageS) + " " + str(messagee)
        print(mes)
        from_email = settings.EMAIL_HOST_USER
        print(from_email)
        to_email = ""
        print(idAnimal)
        check = 0
        if idAnimal:
            pets = Animal.objects.get(id=idAnimal)
            n = CustomUserIdAnimalScore.objects.filter(customuser=user, idAnimal=idAnimal).first()
            if n :
                s = n.score
                s2 = n.heScore
                s3 = n.ehScore
            
            subject = user.last_name + " " + user.first_name + ", " + pets.name + ", " + str(s) + "%"
            subject2 = "Someone wants to meet "+ pets.name
            message2 = user.last_name + " " + user.first_name + ", " + pets.name + ", " + str(s) + "%"
            receiver = ""
            print(subject)
            if pets:
                ownerPet = CustomUserIdleId.objects.filter(idle=pets.id)
            if ownerPet:
                for op in ownerPet:
                    to_email = op.customuser.email
                    receiver = op.customuser
            else:
                to_email = settings.EMAIL_HOST_USER
            print(to_email)
            if subject and message and from_email:
                try:
                    send_mail(subject2, message2, from_email, [to_email,])
                    isNew = 0
                    saveCustomUserAnimalScore(user,idAnimal,s,s2,s3, "Inquiered")
                    saveMessages(user,receiver, pets, subject, mes, isNew,None)
                    mesaj = "The message was sent!"+"\n"+"Now please wait for the date and time to be set!"
                except Exception as e:
                    mesaj = "Something's wrong! Come back later!"
                    print(e)
    
        else:
            mesaj = "The pet's ID is invalid! "
        
    else:
        mesaj = "Something's wrong! Come back later!"
    context = {
        "check":check,
        "mesaj":mesaj
    }
    return render(request, 'forwardAdopting.html',context)

def showAnimalsMessagesAdoptator(request):
    from .models import CustomUserIdAnimalScore, CustomUserMessages
    user = request.user
    color = []
    adoptatori = CustomUserIdAnimalScore.objects.filter(customuser=user, state="Inquiered")
    for a in adoptatori:
        print("primu for ",a.customuser.first_name)

    if adoptatori:
        for a in adoptatori:
            print("for 2 ",a.idAnimal.name)
            messages = CustomUserMessages.objects.filter(receiver=user, idAnimal=a.idAnimal, isNew=0)
            if messages.exists():
                color.append(0)
            else:
                color.append(1)

        mesaj3 =""
    else:
        mesaj3 = "No new messages!"

    if len(adoptatori)==1:
        for a in adoptatori:
            if a.idAnimal.adopted==1:
                mesaj3 = "No new messages!"
   
    print(color)
    print(len(adoptatori))
    lung = len(adoptatori)
    adoptatori3 = zip(adoptatori, color)
    context = {
        "sam":1,
        "lung1":lung,
        "mesaj3":mesaj3,
        "adoptatori":adoptatori3,
        "color":color
    }
    return render(request, 'account.html',context)

def showAnimalsMessagesGiveToAdopt(request):
    from .models import CustomUserMessages, CustomUserIdleId, CustomUserIdAnimalScore
    user = request.user
    color = []
    animals = CustomUserIdleId.objects.filter(customuser=user)
    
    animals2 = CustomUserIdleId.objects.none()
    mesaj3 = ""
    if animals:
        for a in animals:
            messages2 = CustomUserMessages.objects.filter(receiver=user, idAnimal=a.idle)
            
            for m in messages2:
                #print(m.idAnimal.name)
                user1 = CustomUserIdAnimalScore.objects.filter(customuser=m.sender, idAnimal=a.idle).first()
                if user1.state!="Done":
                    animals2 |= CustomUserIdleId.objects.filter(idle=a.idle)
    
    if animals2:
        for a in animals2:
            print(a.idle.name)
            messages = CustomUserMessages.objects.filter(receiver=user, idAnimal=a.idle.id, isNew=0)
            if messages.exists():
                color.append(0)
            else:
                color.append(1)
    else:
        mesaj3 = "No new messages!"
    if len(animals2)==1:
        for a in animals2:
            if a.idle.adopted==1:
                mesaj3 = "No new messages!"
    print(color)
    print(len(animals2))
    lung2 = len(animals2)
    animals3 = zip(animals2, color)
    context = {
        "sam":2,
        "lung2":lung2,
        "mesaj3":mesaj3,
        "animals":animals3,
        "color":color
    }
    return render(request, 'account.html',context)

def convoAdoptator(request,idAnimal):
    from .models import CustomUserMessages, Animal, CustomUserIdAnimalScore, CustomUserIdleId
    user = request.user
    sender, receiver, to_email, s = whichSenderReceiver(user, idAnimal)
    animal = Animal.objects.get(id=idAnimal)
    owner = CustomUserIdleId.objects.filter(idle=animal).first()
    address= owner.customuser.address
    print("adresa",address)
    if user.role==1:
        corep = getOwner(idAnimal)
    else:
        corep = getCorespondent(idAnimal)    
    print("corespondant ",corep)
    if idAnimal:
            pets = Animal.objects.get(id=idAnimal)
            n = CustomUserIdAnimalScore.objects.filter(customuser=user, idAnimal=idAnimal).first()
            if n :
                s = n.score
                
    messages = CustomUserMessages.objects.none()
    try:
       messages1 = CustomUserMessages.objects.filter(sender=sender, receiver=receiver, idAnimal=animal)
       messages2 = CustomUserMessages.objects.filter(sender=receiver, receiver=sender,idAnimal=animal)
       messages =messages1|messages2
       messages3 = messages.order_by('-date')
       
       latest_message = messages3.first()

       print("status ",latest_message.status)
      
       for m in messages3:
            #print(m.isNew)
           
            if user==m.receiver and m.idAnimal==animal:
                m.isNew = 1
                m.save()
    except Exception as e:
        print(e)
    if latest_message.sender==user and latest_message.receiver!=user and latest_message.status==None:
           check = 3
    else:
        if latest_message.status == "Accepted":
            check = 1
        else:
            check = 2    

    context = {
            "caa":1,
            "sender":corep,
            "score":s,
            "messages":messages3,
            "idAnimal":idAnimal, 
            "animal":animal,
            "latest_message":latest_message.message,
            "address":address,
            "check":check
        }
    return render(request, 'account.html',context)

def sendMessageBack(request,idAnimal):
    from .models import Animal, CustomUserIdleId
    if request.method == 'POST':
        user = request.user
        if user.role==1:
            corep = getOwner(idAnimal)
        else:
            corep = getCorespondent(idAnimal)
        
        print("corespondant ",corep)
        sender, receiver, to_email, s = whichSenderReceiver(user, idAnimal)
        mesaj=""
        animal = Animal.objects.get(id=idAnimal)
        owner = CustomUserIdleId.objects.filter(idle=animal).first()
        address= owner.customuser.address
        print("adresa 2 ",address)
        accept_value = request.POST.get('accept')
        end_date = request.POST.get('endDate2')
        start_time = request.POST.get('startTime2')
        end_time = request.POST.get('endTime2')
        location = request.POST.get('location')
        print("location ", location)
        try:
            if location!=None and location != "":
                if address != location:
                    owner.customuser.address=location
                    address = location
                    owner.customuser.save()
        except Exception as e:
            print(e)
        if accept_value == "Accept":
            message = getLatestMessage(user, idAnimal)
            status = "Accepted"
            check = 1
        else:
            message = str(end_date) + " " + str(start_time) + " " + str(end_time)
            status = "Declined"
            check = 0
        from_email = settings.EMAIL_HOST_USER
        print(from_email)
        pets = Animal.objects.filter(id=idAnimal).first()
        animalName = pets.name
        if user.role == 1:
            subject = user.last_name + " " + user.first_name +", " + animalName + ", " + str(s) + "%"
        else:
            subject = user.last_name + " " + user.first_name
        subject2 = "You have a new message from " + subject
        if subject and message and from_email:
            try:
                send_mail(subject2, message, from_email, [to_email,])
                isNew = 0
                saveMessages(sender,receiver, pets, subject, message, isNew,status)
                #mesaj = "The message was sent!Now please wait for the date and time to be set!"
            except Exception as e:
                mesaj = "Invalid header found!"
                print(e)
        else:
            
            mesaj = "Make sure all fields are entered and valid!"
    else:
        mesaj = "Something's wrong! Come back later!"
    print("mesaj ",mesaj)
    latest_message = getLatestMessage(user, idAnimal)
    
    print(latest_message)
    context = {
            "caa":1,
            "latest_message":latest_message,
            "idAnimal":idAnimal,
            "mesaj4":mesaj,
            "sender":corep,
            "score":s,
            "check":check, 
            "address":address
        }
    return render(request, 'account.html',context)


def petfinderArticlesDogs(request):
    url = 'https://www.petfinder.com/dogs-and-puppies/health-wellness/grooming/'
    url4 = 'https://www.petfinder.com/dogs-and-puppies/health-wellness/concerns/'
    url5 = 'https://www.petfinder.com/dogs-and-puppies/health-wellness/lifespan/'
    url6 = 'https://www.petfinder.com/dogs-and-puppies/health-wellness/poisonous-items/'
    url7 = 'https://www.petfinder.com/dogs-and-puppies/health-wellness/seasonal-tips/'
    url8 = 'https://www.petfinder.com/dogs-and-puppies/health-wellness/spaying-neutering/'
    url9 = 'https://www.petfinder.com/dogs-and-puppies/health-wellness/vaccinations-shots/'
    url2 = 'https://www.petfinder.com/dogs-and-puppies/behavior/anxiety/'
    url3 = 'https://www.petfinder.com/dogs-and-puppies/behavior/barking-howling/'
    url10 = 'https://www.petfinder.com/dogs-and-puppies/behavior/biting/'
    url11 = 'https://www.petfinder.com/dogs-and-puppies/behavior/chewing/'
    url12 = 'https://www.petfinder.com/dogs-and-puppies/behavior/other-problem-behaviors/'
    url13 = 'https://www.petfinder.com/dogs-and-puppies/feeding/food-and-treats/'
    url14 = 'https://www.petfinder.com/dogs-and-puppies/feeding/nutrition/'
    url15 = 'https://www.petfinder.com/dogs-and-puppies/feeding/vitamins-supplements/'
    url16 = 'https://www.petfinder.com/dogs-and-puppies/feeding/can-dogs-eat/'
    articles = scrapePetfinderArticles(url)
    articles2 = scrapePetfinderArticles(url2)
    articles3 = scrapePetfinderArticles(url3)
    articles4 = scrapePetfinderArticles(url4)
    articles5 = scrapePetfinderArticles(url5)
    articles6 = scrapePetfinderArticles(url6)
    articles7 = scrapePetfinderArticles(url7)
    articles8 = scrapePetfinderArticles(url8)
    articles9 = scrapePetfinderArticles(url9)
    articles10 = scrapePetfinderArticles(url10)
    articles11 = scrapePetfinderArticles(url11)
    articles12 = scrapePetfinderArticles(url12)
    articles13 = scrapePetfinderArticles(url13)
    articles14 = scrapePetfinderArticles(url14)
    articles15 = scrapePetfinderArticles(url15)
    articles16 = scrapePetfinderArticles(url16)
    articles23 = articles2 + articles3 + articles10 + articles11 + articles12
    articles04 = articles + articles4 + articles5 + articles6 + articles7 + articles8 + articles9
    articles33 = articles13 +  articles14 + articles15 + articles16
    
    context={
        'articles': articles04,
        'articles23':articles23,
        'articles33':articles33
    }

    return render(request, 'dogArticles.html',context )

def viewArticle(request, link):
    content = extractContentFromArticle(link)
    context = {
        'content':content
    }
    return render(request, 'viewArticle.html', context)

def petfinderArticlesCats(request):
    url = 'https://www.petfinder.com/cats-and-kittens/health-wellness/grooming/'
    url4 = 'https://www.petfinder.com/cats-and-kittens/health-wellness/concerns/'
    url5 = 'https://www.petfinder.com/cats-and-kittens/health-wellness/lifespan/'
    url6 = 'https://www.petfinder.com/cats-and-kittens/health-wellness/seasonal-tips/'
    url7 = 'https://www.petfinder.com/cats-and-kittens/health-wellness/spaying-neutering/'
    url8 = 'https://www.petfinder.com/cats-and-kittens/health-wellness/vaccinations-shots/'

    url2 = 'https://www.petfinder.com/cats-and-kittens/behavior/body-language/'
    url3 = 'https://www.petfinder.com/cats-and-kittens/behavior/playing/'
    url10 = 'https://www.petfinder.com/cats-and-kittens/behavior/problems/'
    url11 = 'https://www.petfinder.com/cats-and-kittens/behavior/socializing/'
   

    url13 = 'https://www.petfinder.com/cats-and-kittens/feeding/nutrition/'
    url14 = 'https://www.petfinder.com/cats-and-kittens/feeding/vitamins-supplements/'
    url15 = 'https://www.petfinder.com/cats-and-kittens/feeding/can-cats-eat/'
   
    articles = scrapePetfinderArticles(url)
    articles2 = scrapePetfinderArticles(url2)
    articles3 = scrapePetfinderArticles(url3)
    articles4 = scrapePetfinderArticles(url4)
    articles5 = scrapePetfinderArticles(url5)
    articles6 = scrapePetfinderArticles(url6)
    articles7 = scrapePetfinderArticles(url7)
    articles8 = scrapePetfinderArticles(url8)
    
    articles10 = scrapePetfinderArticles(url10)
    articles11 = scrapePetfinderArticles(url11)
    
    articles13 = scrapePetfinderArticles(url13)
    articles14 = scrapePetfinderArticles(url14)
    articles15 = scrapePetfinderArticles(url15)
    
    articles23 = articles2 + articles3 + articles10 + articles11
    articles04 = articles + articles4 + articles5 + articles6 + articles7 + articles8
    articles33 = articles13 +  articles14 + articles15 
    
    context={
        'articles': articles04,
        'articles23':articles23,
        'articles33':articles33
    }

    return render(request, 'catArticles.html',context )

def mapView(request):
    key = settings.GOOGLE_API_KEY
    context = {
        'key':key,
    }
    return render(request, 'map.html',context)

from datetime import datetime
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def housingEnvScore(typeAnimal, props2, housing_env):
    s = 0
    props2 = [p.lower() for p in props2]
    print(props2)
   
    houseEnv = [prop.strip().lower() for prop in housing_env.split('.') if prop.strip()]
    print(houseEnv)
    for h in houseEnv:
        if  "house" in h:
            if typeAnimal == "Dog" or typeAnimal == "Cat":
                s = s + 1
        if "courtyard" in h:
            if typeAnimal== "Dog" :
                s = s + 2
            for p in props2:
                if "active" in p:
                    s = s + 1
        if  "apartament" in h:
            if typeAnimal == "Dog" or typeAnimal == "Cat":
                s = s + 1
            for p in props2:
                if "poty trained" in p:
                    s = s + 2
                if "does not shed much" in p:
                    s = s + 1
    return s
 

def experienceScore(typeAnimal, props2, exp_his, gender):
    s = 0
    props2 = [p.lower() for p in props2]
    print(props2)
    expHis = [prop.strip().lower() for prop in exp_his.split('.') if prop.strip()]
    print(expHis)
    gender = gender.lower()
    for eh in expHis:
        if gender in eh:
                s = s + 1
        if typeAnimal == "Cat":
            if "had cats" in eh:
                s = s + 2
        if typeAnimal == "Dog":
            if "had dogs" in eh:
                s = s + 2
        for p in props2:
            if  "good with other animals" in p:
                if "i have cats" in eh:
                    s = s + 1
                if  "i have dogs" in eh:
                    s = s + 1
    return s

def saveCustomUserAnimalScore(user, idAnimal, score, s2,s3, state):
    from .models import CustomUserIdAnimalScore
    user1 = CustomUserIdAnimalScore.objects.filter(customuser=user, idAnimal=idAnimal)
    try:
        if user1.exists():
            for u in user1:
                if u.score != score:
                    u.score = score
                if u.heScore != s2:
                    u.heScore = s2
                if u.ehScore != s3:
                    u.ehScore = s3
                if u.state != state:
                    u.state = state
                u.save()
        else:
            animalScore = CustomUserIdAnimalScore(
                                customuser=user,
                                idAnimal=idAnimal,
                                score=score,
                                heScore=s2,
                                ehScore=s3,
                                state=state
                            )
            animalScore.save()
    except Exception as e:
        print(e)

def findCompatibleAnimals(descriptionUser, pets):
    from .models import Animal
    descUser = [prop.strip().lower() for prop in descriptionUser.split('.') if prop.strip()]
    pets2 = Animal.objects.none()
    
    for pet in pets:
        descPet = [prop2.strip().lower() for prop2 in pet.description.split('.') if prop2.strip()]
        for desc in descPet:
            if desc in descUser:
                print(desc)
                pets2 |= Animal.objects.filter(id=pet.id)
        
    return pets2         

def saveMessages(sender, receiver, idAnimal, subject, message, isNew, status):
    from .models import CustomUserMessages
    currentDate = timezone.now()
    print(currentDate)
    try:
        message = CustomUserMessages(
            sender = sender,
            receiver=receiver,
            idAnimal=idAnimal,
            date=currentDate,
            subject=subject,
            message=message,
            isNew=isNew,
            status=status
        )
        message.save()
    except Exception as e:
        print(e)


def updateMessages(sender, receiver, idAnimal):
    from .models import CustomUserMessages
    message = CustomUserMessages.objects.filter(sender=sender, receiver=receiver, idAnimal=idAnimal, isNew=0)
    try:
       for m in message:
        m.isNew = 1
        m.save()
    except Exception as e:
        print(e)
        
def whichSenderReceiver(user, idAnimal):
    from .models import CustomUserIdleId, Animal, CustomUserIdAnimalScore
    s = ""
    if idAnimal:
        pets = Animal.objects.get(id=idAnimal)
        n = CustomUserIdAnimalScore.objects.filter(customuser=user, idAnimal=idAnimal).first()
        if n :
            s = n.score
    else:
        mesaj = "The pet's ID is invalid! "
    if user.role == 0:
        if pets:
            ineteresteInPet = CustomUserIdAnimalScore.objects.filter(idAnimal=pets.id, state="Inquiered").first()
        if ineteresteInPet:
                to_email = ineteresteInPet.customuser.email
                receiver = ineteresteInPet.customuser
    else:
        receiver = ""
        
        if pets:
            ownerPet = CustomUserIdleId.objects.filter(idle=pets.id)
        if ownerPet:
            for op in ownerPet:
                to_email = op.customuser.email
                receiver = op.customuser
    return user, receiver, to_email, s

def getMessages(user,idAnimal):
    from .models import CustomUserMessages, Animal
    pet = Animal.objects.get(id=idAnimal)
    sender, receiver, to_email, s = whichSenderReceiver(user, idAnimal)
    messages = CustomUserMessages.objects.none()
    try:
       messages1 = CustomUserMessages.objects.filter(sender=sender, receiver=receiver, idAnimal=pet)
       messages2 = CustomUserMessages.objects.filter(sender=receiver, receiver=sender, idAnimal=pet)
       messages =messages1|messages2
       messages3 = messages.order_by('date')
    except Exception as e:
        print(e)
    return messages3

def getLatestMessage(user, idAnimal):
    from .models import CustomUserMessages, Animal
    pet = Animal.objects.get(id=idAnimal)
    sender, receiver, to_email, s = whichSenderReceiver(user, idAnimal)

    try:
      
        messages1 = CustomUserMessages.objects.filter(sender=sender, receiver=receiver, idAnimal=pet)
        messages2 = CustomUserMessages.objects.filter(sender=receiver, receiver=sender, idAnimal=pet)
        messages = (messages1 | messages2).order_by('-date')
        
        latest_message = messages.first()
    except Exception as e:
        print(e)
        latest_message = None
    
    return latest_message.message


def animalGotAdopted(idAnimal):
    from .models import Animal, CustomUserIdAnimalScore
    pets = Animal.objects.get(id=idAnimal)
    user1 = CustomUserIdAnimalScore.objects.filter(idAnimal=pets.id, state="Inquiered")
    try:
        for u in user1:
            print(u.customuser.email)
            u.state="Done"
            u.save()
    except Exception as e:
        print(e)


def scrapePetfinderArticles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = []
    for li_tag in soup.find_all('li', class_="ArticleGrid-module--articleGrid_item--eb3f5"):
        a_tag = li_tag.find('a')
        if a_tag and 'href' in a_tag.attrs:
            href = a_tag['href']
            full_url = urljoin(url, href)
            title = href.split('/')[-2].replace('-', ' ').title()
            
            article_data = {
                'title': title,
                'link': full_url
            }
            articles.append(article_data)
    return articles 


def extractContentFromArticle(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    body_div = soup.find('div', class_='body')
    if body_div:
        for img_tag in body_div.find_all('img'):
            img_tag.decompose()
        
        return body_div.prettify()
    return None
    
def getOwner(idAnimal):    
    from .models import Animal, CustomUserIdleId
    if idAnimal:
        pets = Animal.objects.get(id=idAnimal)
        
    else:
        pets = Animal.objects.all()

    if pets:
        custom_user_idle_ids = CustomUserIdleId.objects.filter(idle=pets.id)
    if custom_user_idle_ids: 
        for c in custom_user_idle_ids:
            ownerFirstName = c.customuser.first_name
            ownerLastName = c.customuser.last_name
           
    mesaj = ownerFirstName + " " + ownerLastName
    return mesaj

def getCorespondent(idAnimal):
    from .models import Animal, CustomUserIdAnimalScore
    pet = Animal.objects.get(id=idAnimal)
    user1 = CustomUserIdAnimalScore.objects.get(idAnimal=pet.id, state="Inquiered")
    print(user1.customuser.first_name)
    print(user1.customuser.last_name)
    print(user1.idAnimal.name) 
    mesaj = user1.customuser.first_name + " " + user1.customuser.last_name + ",  " + user1.idAnimal.name + " " + str(user1.score) +"%"
    return mesaj

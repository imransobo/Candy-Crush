from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt

from .serializers import PlayerListSerializer, ScoreBoardSerializer, ScoreListSerializer
import random
import string
from django.core.mail import send_mail
from . import models


# Create your views here.



class PlayerList(generics.ListCreateAPIView):
    queryset = models.Player.objects.all()
    serializer_class = PlayerListSerializer

class ScoreList(generics.ListCreateAPIView):
    queryset = models.Score.objects.all()
    serializer_class = ScoreListSerializer

class ScoreBoard(generics.ListCreateAPIView):
    queryset = models.Score.objects.all().order_by('-score')
    serializer_class = ScoreBoardSerializer



class PlayerDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Player.objects.all()
    serializer_class = PlayerListSerializer

@csrf_exempt
def user_login(request):
    email = request.POST['email']
    password = request.POST['password']
    try:
        userData = models.Player.objects.get(email=email, password=password)
    except models.Player.DoesNotExist:
        userData = None

    if userData:
        return JsonResponse( { 'bool': True, 'playerId': userData.id, 'playerName': userData.player_name } )
    else:
        return JsonResponse( { 'bool': False } )








def generate_pass():
    all_chars = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    password_length = 8
    random.shuffle(all_chars)
    password = []

    for i in range(password_length):
        password.append(random.choice(all_chars))
    
    random.shuffle(password)
    newPass = "".join(password)

    return newPass




@csrf_exempt
def reset_user_pass(request):
    email = request.POST['email']
    user = models.Player.objects.get(email=email)

    if user:
        newPass = generate_pass()
        print(newPass)
        user.password = newPass
        user.save()

        send_mail('Promjena lozinke za: ' + user.email,
                  'Poštovani ' + user.player_name + ", Vaša nova lozinka za račun je: " + newPass,
                  'imranjedantri@gmail.com',
                  [user.email],
                  fail_silently=False)
        return JsonResponse( { 'status': "Ulogujte se s novom lozinkom koja Vam je poslana na mail.", 's1': True } )
    else:
        return JsonResponse( { 'status': "Korisnik sa ovim mailom ne postoji." , 's1': False } )

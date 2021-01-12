import json
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from .models import ContactList, User
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.authtoken.models import Token
# for throttling
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import throttle_classes
# Create your views here.


# for user in User.objects.all():
# uid = models.CharField(max_length=100, unique=True, null=True)
# address = models.TextField(null=False)
# phone_number = models.IntegerField(unique=True, null=False)
# email = models.EmailField(unique=True, null=False)
# name

@api_view(["POST"])
def register(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data)
        email = data["email"]
        address = data["address"]
        phone_number = data["phone_number"]
        name = data["name"]
        try:
            user = User.objects.create_user(
                email=email, address=address, username=phone_number, phone_number=phone_number, name=name)
            user.save()
            return Response({"message": "created"}, status=status.HTTP_201_CREATED)

        except:
            return Response({"message": "not_created"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        phone = data["phone_number"]

        try:
            user = User.objects.get(username=phone)
        except:
            return Response({"message": "No such number exists in database"}, status=status.HTTP_401_UNAUTHORIZED)

        if "uid" not in data and user.uid == None:
            return Response({"message": "please send a valid uid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif "uid" not in data and user.uid is not None:
            uid = user.uid
        else:
            if user.uid is not None:
                if data["uid"] == user.uid:
                    uid = data["uid"]
                else:
                    return Response({"message": "invalid uid format or wrong uid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                print(1)
                if len(data["uid"]) == 0:
                    return Response({"message": "please send a valid uid"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                print(1)
                print(len(data["uid"]))

                uid = data["uid"]
                user.uid = uid
                user.set_password(uid)
                user.save()

        # return JsonResponse({"message": "missing_attribute"})

        try:
            # check if user exists and if user can be authenticated return token

            user_check = User.objects.get(username=phone)
            user = authenticate(request, username=phone, password=uid)
            print(user)
            if user is not None:
                token = Token.objects.get_or_create(user=user)
                token = str(token[0])
                print(1)
                address = user.address
                email = user.email
                name = user.name
                phone_number = user.phone_number
                #login(request, user)

                return JsonResponse({"token": token, "name": name, "email": email, "address": address, "phone": phone_number})

            # if user exists but password is wrong
            elif user_check:
                return JsonResponse({"token": "wrong_password"})

        # if user does not exists create user
        except:
            try:
                # if user does not exists create user
                # user = User.objects.create_user(
                # email=email, address=address, username=phone_number, phone_number=phone_number, name=name)
                # user.save()

                # user = authenticate(request, username=email, password=password)
                # token = Token.objects.get_or_create(user=user)
                # token = str(token[0])
                #login(request, user)
                return JsonResponse({"token": "wait_why", "message": "new_user_also_created"})
            # if user can not be created
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        # if user is not None:
        #     login(request, user)
        #     return JsonResponse({"message": "user_logged_in"})
        # else:
        #     return JsonResponse({"message": "no_user_found"})


@api_view(["POST"])
@throttle_classes([UserRateThrottle])
def users_list(request):
    try:
        data = JSONParser().parse(request)
        token = data["token"]
        user_name = data["phone_number"]
        #user = request.user

        user = User.objects.get(username=user_name)
        real_token = str(Token.objects.get(user=user))
        if token == real_token:
            '''
            token check
            write your own logic after the comment
            '''
            user_list = User.objects.all()
            user_dict = {}
            count = 1
            for every_user in user_list:
                key = "user "+str(count)
                user_dict[key] = every_user.username
                count += 1
            return JsonResponse(user_dict)
        else:
            return Response({"message": "unauthorized_action1"}, status=status.HTTP_403_FORBIDDEN)
    except:
        return JsonResponse({"message": "unauthorized_action2"}, status=status.HTTP_401_UNAUTHORIZED)

#--------------both add and update inside update functions inside update-------------#
# @api_view(["POST"])
# def add_contacts(request):
#     data = JSONParser().parse(request)
#     user = data["phone_number"]
#     Contact_list = data["contacts"]
#     print(Contact_list)
#     # print(json(Contact_list))
#     #token = data["token"]
#     try:
#         userc = User.objects.get(username=user)
#         #token1 = str(Token.objects.get(user=userc))
#         # if token1 == token:
#         #     pass
#         cl = ContactList(user=userc, contacts=Contact_list)
#         cl.save()
#         return Response({"message": "contacts_saved"}, status=status.HTTP_200_OK)
#     except:
#         return Response({"message": "bad_context"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def update_contacts(request):
    data = JSONParser().parse(request)
    user = data["phone_number"]
    new_contacts = data["contacts"]
    #token = data["token"]
    try:
        userc = User.objects.get(username=user)
        print(userc)
        #token1 = str(Token.objects.get(user=userc))
        # if token1 == token:
        #     pass
        cl = ContactList.objects.filter(user=userc)
        print(cl)
        print()
        if len(cl) == 0:
            cl = ContactList(user=userc, contacts=new_contacts)
            cl.save()
            return Response({"message": "contacts added"}, status=status.HTTP_200_OK)
        cl = cl[0]
        c_l = eval(str(cl.contacts))
        new_contacts = eval(new_contacts)
        updated_dicts = c_l
        for e in new_contacts:
            updated_dicts[e] = new_contacts[e]
        cl.contacts = updated_dicts
        cl.save()
        return Response({"message": "contacts updated", "new_contacts": updated_dicts}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "bad_context"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def view_contacts(request):
    data = JSONParser().parse(request)
    user = data["phone_number"]
    #token = data["token"]
    try:
        userc = User.objects.get(username=user)
        print(userc)
        #token1 = str(Token.objects.get(user=userc))
        # if token1 == token:
        #     pass
        cl = ContactList.objects.filter(user=userc)[0]
        print(cl.contacts)
        cl = eval(str(cl.contacts))
        return Response(cl, status=status.HTTP_200_OK)
    except:
        return Response({"message": "bad_context"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_authtokens_logout(request):
    try:
        data = JSONParser().parse(request)
        user = data["phone"]
        print(user)

        #user = request.user.username
        user = User.objects.get(email=user)
        user.auth_token.delete()
        return Response({"message": "deleted"}, status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

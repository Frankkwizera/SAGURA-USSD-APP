from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .sms import send_SMS
import json
from django.core import serializers

def mainMenu():
    response = "CON Welcome to SAGURA Platform \n"
    response += "1. English \n"
    response += "2. Kinyarwanda"
    return response

def secondaryMenu():
    response = "CON 1. Market Place \n"
    response += "2. Fruits Info \n"
    response += "3. Vegetables Info \n"
    response += "4. Cereals Info \n"
    response += "5. Subscribe \n"
    response += "99. Main Menu"
    return response

@csrf_exempt
def index(request):
    if request.method == 'POST':
        session_id = request.POST.get('sessionId')
        service_code = request.POST.get('serviceCode')
        phone_number = request.POST.get('phoneNumber')
        text = request.POST.get('text')
        response = ""
        
        #Getting latest inputs
        textArray = text.split('*')
        lastestInput = textArray[-1]

        #converting to int
        if lastestInput:
            try:
                lastestInput = int(lastestInput)
            except Exception as e:
                pass

        #checking if it's a returning session or new session
        try:
            session = SessionLevel.objects.get(session_id = session_id)
            level = session.level

        except ObjectDoesNotExist:
            session = SessionLevel.objects.create(session_id=session_id,phone_number=phone_number)
            session.save()
            level = session.level

        #render main menu from all levels
        if lastestInput == 99:
            response = mainMenu()
            session.level = 0
            session.save()

            return HttpResponse(response)
        
        #checking level & rendering appropriate menu
        if level == 0:
            response = mainMenu()
            session.level = 1
            session.save()
        
        elif level == 1:
            if lastestInput == 1:
                response = secondaryMenu()
                session.level = 2
                session.save()

            elif lastestInput == 2:
                response = "END Kinyarwanda functionality Coming soon,Now focus on English thanks"
            else:
                response = "END Wrong Input, Enter correct choice"
        
        elif level == 2:
            if lastestInput == 1:
                response = "CON Welcome to the market Place\n"
                response += "1. Sell \n"
                response += "2. Buy \n"
                response += "99. Main Menu"

                session.level = 24
                session.save()
                 

            elif lastestInput == 2:
                response = "CON Fruits Section \n"
                fruits = Crops.objects.filter(crop_type='FRUITS')[:5]
                cropsInSession = {}
                for index,fruit in enumerate(fruits):
                    response += str(index+1) +". "+fruit.name + "\n"
                    cropsInSession[index+1] =  serializers.serialize('json', [ fruit, ])

                response += "99. Main Menu"
                session.session_data = {"crops":cropsInSession}
                session.level = 21
                session.save()
            
            elif lastestInput == 3:
                response = "CON Vegetable Section \n"
                vegetables = Crops.objects.filter(crop_type='VEGETABLES')[:5]
                cropsInSession = {}
                for index,vegetable in enumerate(vegetables):
                    response += str(index+1) +". "+vegetable.name + "\n"
                    cropsInSession[index+1] =  serializers.serialize('json', [ vegetable, ])

                response += "99. Main Menu"
                session.session_data = {"crops":cropsInSession}
                session.level = 21
                session.save()

            elif lastestInput == 4:
                response = "CON Cereal Section \n"
                vegetables = Crops.objects.filter(crop_type='CEREALS')[:5]
                cropsInSession = {}
                for index,vegetable in enumerate(vegetables):
                    response += str(index+1) +". "+vegetable.name + "\n"
                    cropsInSession[index+1] =  serializers.serialize('json', [ vegetable, ])

                response += "99. Main Menu"
                session.session_data = {"crops":cropsInSession}
                session.level = 21
                session.save()

            #user subscription 5
            elif lastestInput == 5:

                try:
                    sagura_user = SaguraUsers.objects.get(phone_number=phone_number)
                    
                    if sagura_user is not None:
                        subscriber = Subscribers.objects.get(user=sagura_user)
                        
                        if subscriber is not None:
                            response = "END "+ sagura_user.name +" You are subscriber!!"
                            return HttpResponse(response)

                    else:
                        subscription = Subscribers.objects.create(user=sagura_user)
                        response = "END Thanks "+ sagura_user.name +" for subscribing to SAGURA Platform"
                        return HttpResponse(response)

                except ObjectDoesNotExist:
                    response = "CON Enter your name (e.g: Frank Kwizera)"
                    session.level = 41
                    session.save()
        
        elif level == 21:
            cropsInSession = session.session_data['crops']
            cropSelected = json.loads(cropsInSession[str(lastestInput)])

            response = "CON "+cropSelected[0]['fields']['name'] + " details: \n"
            response += "1. Preferable Weather \n"
            response += "2. Land Preparation \n"
            response += "3. Maturity Process \n"
            
            session.level = 22
            session.save()
        
        elif level == 22:
            cropSelected_index = textArray[-2]
            cropsInSession = session.session_data['crops']
            cropSelected = json.loads(cropsInSession[str(cropSelected_index)])

            if lastestInput == 1:
                response = "CON "+ cropSelected[0]['fields']['name'] +" Preferable Weather: \n"
                response += cropSelected[0]['fields']['prefered_climate'] +" \n"
                response += "0. Back \n"
                response += "99. Main Menu \n"
                
                session.level = 23
                session.save()

            elif lastestInput == 2:
                response = "CON "+ cropSelected[0]['fields']['name'] +" Land Preparation: \n"
                response += cropSelected[0]['fields']['land_preparation'] + " \n"
                response += "0. Back \n"
                response += "99. Main Menu \n"

                session.level = 23
                session.save()

            elif lastestInput == 3:
                response = "CON "+ cropSelected[0]['fields']['name'] +" Land Preparation: \n"
                response += cropSelected[0]['fields']['maturity_process'] + " \n"
                response += "0. Back \n"
                response += "99. Main Menu \n"

                session.level = 23
                session.save()
            else:
                response = "END invalid input"
        
        elif level == 23:
            if lastestInput == 0:
                response = secondaryMenu()
                session.level = 2
                session.save()
            else:
                response = "END entered invalid choice"
        
        elif level == 24:
            #checking if the user is registered
            try:
                sagura_user = SaguraUsers.objects.get(phone_number=phone_number)
                
                if lastestInput == 1:
                    response = "CON Sell your harvest \n"
                    response += "Enter Crop Name: \n"
                    session.level = 25
                    session.save()

                elif lastestInput == 2:
                    #harvest on sale
                    response = "CON Harvest on sale: \n"
                    crops_on_sale = Harvest.objects.all()
                    harvestInSession = {}
                    for index,crop in enumerate(crops_on_sale):
                        response += str(index+1) +". "+crop.crop_name + "  " + crop.crop_quantity +" Kg \n"
                        harvestInSession[index+1] = serializers.serialize('json',[crop, ])
                    
                    session.session_data = {"requests":harvestInSession}
                    session.level = 28
                    session.save()

            except ObjectDoesNotExist:
                response = "CON You have to be Registered \n"
                response += "Enter Your Name (e.g: Frank Kwizera) \n"
                session.level = 41
                session.save() 

        elif level == 25:
            response = "CON Crop quantity in Kg (e.g: 100)"
            session.level = 26
            session.save()

        elif level == 26:
            response = "CON price per Kg (e.g: 500)"
            session.level = 27
            session.save()

        elif level == 27:
            #saving harvest
            sagura_user = SaguraUsers.objects.get(phone_number=phone_number)
            crop_name = textArray[-3]
            crop_quantity = textArray[-2]
            crop_price = textArray[-1]

            harvest = Harvest.objects.create(crop_name=crop_name,
                                            crop_quantity=crop_quantity,
                                            crop_price=crop_price,
                                            farmer=sagura_user)
            harvest.save()

            response = "END Thanks "+sagura_user.name+" \n"
            response += crop_quantity +" Kg of "+ crop_name+" is on sell at "+crop_price+" RWF per Kg"

        elif level == 28:
            print(" Latest input ",lastestInput)
            harvestInSession = session.session_data['requests']
            harvestSelected = json.loads(harvestInSession[str(lastestInput)])

            response = "CON Harvest Selected Details: \n"
            response += " Name : " + harvestSelected[0]['fields']['crop_name']+" \n"
            response += " QUANTITY : " + harvestSelected[0]['fields']['crop_quantity'] +" Kg \n"
            response += " PRICE/kg : " + harvestSelected[0]['fields']['crop_price'] + " \n"
            response += "1. Order \n"
            response += "0. Back \n"
            response += "99. Main Menu"

            session.level = 29
            session.save()

        elif level == 29:
            if lastestInput == 1:
                #order quantity
                response = "CON How many Kgs do you want: \n"
                session.level = 30
                session.save()

            else:
                #harvest on sale
                response = "CON Harvest on sale: \n"
                crops_on_sale = Harvest.objects.all()
                harvestInSession = {}
                for index,crop in enumerate(crops_on_sale):
                    response += str(index+1) +". "+crop.crop_name + "  " + crop.crop_quantity +" Kg \n"
                    harvestInSession[index+1] = serializers.serialize('json',[crop, ])
                
                session.session_data = {"requests":harvestInSession}
                session.level = 28
                session.save()

        elif level == 30:
            #ordering harvest
            quantity = lastestInput
            harvestInSession = session.session_data['requests']
            harvestSelected = json.loads(harvestInSession[str(textArray[-3])])
            harvest_id = harvestSelected[0]['pk']
            harvest = Harvest.objects.get(id=harvest_id)
            sagura_user = SaguraUsers.objects.get(phone_number=phone_number)
            
            order = Orders.objects.create(harvest = harvest,
                                          buyer = sagura_user,
                                          quantity = quantity)
            
            order.save()

            buyerMessage = " Hello " + sagura_user.name + " You have successfully ordered " + str(quantity) + " Kg of " + harvest.crop_name
            buyerNotification = send_SMS([sagura_user.phone_number],buyerMessage)

            farmerMessage = " Hello "+ harvest.farmer.name + " Harvest order: "+ str(quantity) + "Kg of "+harvest.crop_name +" have been ordered by :" + sagura_user.name + " Phone Number " + sagura_user.phone_number
            farmerNotification = send_SMS([harvest.farmer.phone_number],farmerMessage)


            response = "END Thanks "+sagura_user.name+" for ordering "+harvest.crop_name


        #User subscription 41
        elif level == 41:
            response = "CON Enter your National ID"
            session.level = 42
            session.save()
        
        #User subscription 42
        elif level == 42:
            response = "CON Enter your Location"
            session.level = 43
            session.save()
        
        #User subscription 43
        elif level == 43:
            location = textArray[-1]
            nationa_id = textArray[-2]
            name = textArray[-3]
            
            sagura_user = SaguraUsers.objects.create(name=name,
                                                     phone_number=phone_number,
                                                     national_id=nationa_id,
                                                     address=location)
            
            subscription = Subscribers.objects.create(user=sagura_user)

            response = "END Thanks "+name+" for Registering on SAGURA Platform"
        
        else:
            response = "END unknown session level, terminate and try again"

        return HttpResponse(response)
    else:
        return HttpResponse("GET Method not allowed")


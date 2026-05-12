from django.shortcuts import render

import requests

from datetime import datetime

import pytz


def send_telegram_message(message):

    token = "8321370989:AAG4TGus6A5wLNExz7JVcRUChsM7q3ZFT6E"

    chat_id = "8910395942"

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": message
    }

    requests.post(url, data=data)


def home(request):

    ip = request.META.get('REMOTE_ADDR')

    india = pytz.timezone('Asia/Kolkata')

    time = datetime.now(india)

    message = f"""
New Website Visitor

IP: {ip}

Time: {time}
"""

    send_telegram_message(message)

    if request.method == "POST":

        mother = request.POST.get("mother")
        mother_rh = request.POST.get("mother_rh")

        father = request.POST.get("father")
        father_rh = request.POST.get("father_rh")

        ml=[]
        fl=[]
        mlr=[]
        flr=[]

        if(mother=="A"):
            ml.extend(["a","a","a","i"])

        elif(mother=="B"):
            ml.extend(["b","b","b","i"])

        elif(mother=="AB"):
            ml.extend(["a","b"])

        elif(mother=="O"):
            ml.extend(["i","i"])

        if(father=="A"):
            fl.extend(["a","a","a","i"])

        elif(father=="B"):
            fl.extend(["b","b","b","i"])

        elif(father=="AB"):
            fl.extend(["a","b"])

        elif(father=="O"):
            fl.extend(["i","i"])

        if(mother_rh=="+"):
            mlr.extend(["+","+","+","-"])

        else:
            mlr.extend(["-","-"])

        if(father_rh=="+"):
            flr.extend(["+","+","+","-"])

        else:
            flr.extend(["-","-"])

        a=0
        b=0
        ab=0
        o=0

        rp=0
        rn=0

        for i in ml:

            for j in fl:

                k=i+j

                if(k=="aa" or k=="ai" or k=="ia"):

                    a+=1

                elif(k=="bb" or k=="bi" or k=="ib"):

                    b+=1

                elif(k=="ab" or k=="ba"):

                    ab+=1

                elif(k=="ii"):

                    o+=1

        cl=[a,b,ab,o]

        for ir in mlr:

            for jr in flr:

                kr=ir+jr

                if(kr=="++" or kr=="+-" or kr=="-+"):

                    rp+=1

                elif(kr=="--"):

                    rn+=1

        clr=[rp,rn]

        l=[]

        for i1 in cl:

            for j1 in clr:

                l.append(i1*j1)

        y=sum(l)

        if(y==0):

            y=1

        result = {

            "A+": round(l[0]/y*100,2),

            "A-": round(l[1]/y*100,2),

            "B+": round(l[2]/y*100,2),

            "B-": round(l[3]/y*100,2),

            "AB+": round(l[4]/y*100,2),

            "AB-": round(l[5]/y*100,2),

            "O+": round(l[6]/y*100,2),

            "O-": round(l[7]/y*100,2),
        }

        anemia = None

        cri=rp/sum(clr)*100

        if(father_rh=="+" and mother_rh=="-"):

            anemia = f"The second child has {round(cri,2)}% chance to get severe anemia."

        return render(request,"index.html",{
            "result":result,
            "anemia":anemia
        })

    return render(request,"index.html")

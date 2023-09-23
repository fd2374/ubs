import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/Asteriod', methods=['POST'])
def evaluate2():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    input_value = data.get("test_cases")
    result=[]
    for s in input_value:
        dict={}
        working(dict,s)
        result.append(dict)
    
    logging.info("My result :{}".format(result))

    return result

def get_the_point(num):
    if num>=10:
        return num*2
    elif num>=7:
        return num*1.5
    else:
        return num

def working(dict,s):
    restr=[]
    for i in range(len(s)):
        if i==0:
            restr.append([s[i],1,0])
        elif s[i]!=s[i-1]:
            restr[-1][2]=i-restr[-1][1]//2-1
            restr.append([s[i],1,0])
        else:
            restr[len(restr)-1][1]+=1
    restr[-1][2]=len(s)-restr[-1][1]//2-1
    #logging.info(restr)
    dict["input"]=s
    dict["score"]=0
    dict["origin"]=0
    for i in range(len(restr)):
        score=get_the_point(restr[i][1])
        l=i-1
        r=i+1
        while((l>=0) and (r<len(restr)) and (restr[l][0]==restr[r][0])):
            score+=get_the_point(restr[l][1]+restr[r][1])
            l-=1
            r+=1
            logging.info("%d",(l>=0) and (r<len(s)) and (restr[l][0]==restr[r][0]))
            
        
        if score>dict["score"]:
            dict["score"]=score
            dict["origin"]=restr[i][2]
    return restr
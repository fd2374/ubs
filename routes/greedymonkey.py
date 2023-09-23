import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


@app.route('/greedymonkey', methods=['POST'])
def evaluate3():
    data = request.get_data()
    data=json.loads(data)
    logging.info("data sent for evaluation {}".format(data))
    w = data.get("w")
    v= data.get("v")
    f= data.get("f")
    result=working(w,v,f)
    logging.info("My result :{}".format(result))

    return str(result)

def working(w,v,mon):
    f=[[0 for _ in range(v+1)] for _ in range(w+1)]
    for i in range(len(mon)):
        for j in range(w,mon[i][0]-1,-1):
            for k in range(v,mon[i][1]-1,-1):
                f[j][k]=max(f[j-mon[i][0]][k-mon[i][1]]+mon[i][2],f[j][k])
    return f[w][v]

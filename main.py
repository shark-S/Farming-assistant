from flask import Flask, render_template, request, redirect, url_for, abort, session, send_file
import pickle
from weather import Weather
import numpy as np
weather = Weather()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'F34TF$($e34D';

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/getAnswer', methods=['POST'])
def dislayResult():
    input_list = []
    state = request.form['state']
    district = request.form['district']

    ### weather api
    location = weather.lookup_by_location(district+' '+state)
    condition = location.condition()
    forecasts = location.forecast()
    i=0
    sum1=0
    for forecast in forecasts:
        sum1 = sum1+int(forecast.high())
        sum1 = sum1+int(forecast.low())
        i =i+2

    sum1 = sum1/i





    season = request.form['season']
    area= float(request.form['area'])
    prod=area*1.5
    state=state.lower()
    district=district.lower()
    x11 = state.split(' ')
    ans=''
    for i in x11:
        ans = ans+i
    x11 = district.split(' ')
    for i in x11:
        ans +=i
    # load state_dis map
    state_id_map = pickle.load(open("dump/state_id_map.p","rb"))
    input_list.append(state_id_map[ans])
    input_list.append(2017)
    season = season.lower()
    f=0
    if season=="rabi":
        f=1
    # year = 2017
    input_list.append(f)
    input_list.append(area)
    input_list.append(prod)
    input_list.append(sum1)


    ## load model
    x=[]
    x.append(input_list)

    loaded_model = pickle.load(open('dump/classify.sav','rb'))
    id_crop = pickle.load(open('dump/id_crop_map.p','rb'))

    val = loaded_model.predict_proba(x)
    val = val[0]
    # print(id_crop[val])
    data = np.array(val)
    sorted_id = np.argsort(data)
    ans = sorted_id[len(sorted_id)-3:]
    # print (ans)
    for i in ans:
        print(id_crop[i])



    return render_template('result.html', crop1=id_crop[ans[0]], crop2=id_crop[ans[1]], crop3=id_crop[ans[2]])

if __name__ == '__main__':
    app.run()
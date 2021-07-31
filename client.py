import requests
import json
import vk_api
import shutil
import os
import numpy as np
import face_recognition
from skimage import io
import pymysql
import time

server='http://127.0.0.1:8000'

vk_session = vk_api.VkApi(input(), input())
vk_session.auth()
vk = vk_session.get_api()
do_n = 360
do_counter=0
while do_counter<=do_n:
    r = requests.get(server)
    r=json.loads(r.text)
    print(r)
    c = r['counter']
    time.sleep(1)
    res = vk.users.search(count=1000,
                                    fields='id, photo_max_orig, has_photo, '
                                        'first_name, last_name',
                                    city=r['city'],
                                    sex=r['gender'],
                                    age_from=r['years'],
                                    age_to=r['years'],
                                    birth_day=r['day'],
                                    has_photo=1,
                                    birth_month=r['month'])
    def get_face_descriptor(x):
        try:
            img =face_recognition.load_image_file('jpg/'+x)
            faces=face_recognition.face_encodings(img)
            os.remove('jpg/'+x)
            con = pymysql.connect(host='localhost',
                user='root',
                password='',
                db='faces',
                charset='utf8mb4')
            with con: 
                cur = con.cursor()
                for face in faces:
                    cur.execute("insert into faces (user_id, face_disc) values ("+x[:-6]+",'"+str(face)+"')")
                    con.commit()
        except Exception as ex:

            print(ex)
    def get_photos_by_id(user_id_):
        try:
            request_result = vk.photos.getAll(owner_id=user_id_,
                                            count=15,
                                            no_service_albums=0)
            prev = ''
            flag = 0
            photos = []
            for item in request_result['items']:
                for size in item['sizes']:
                    url_ = str(size['url'])
                    mas_ = url_.split('/')
                    ident = mas_[4]
                    if prev != ident:
                        prev = ident
                        flag = 0
                    else:
                        flag += 1
                        if flag == 3:
                            photos.append(url_)
            max_flag = 0
            for photo in photos:
                max_flag += 1
                if max_flag < 10:
                    load_file(str(user_id_) + '_' + str(max_flag), photo)
        except Exception as ex:
            print(ex)
    def load_file(name, url):
        if not os.path.exists('jpg/' + str(name) + '.jpg'):
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                with open('jpg/' + str(name) + '.jpg', 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
    counter=0
    for re in res['items']:
        counter+=1
        print(str(counter)+" of "+str(len(res['items'])))
        get_photos_by_id(re['id'])
        files = os.listdir('jpg')
        z = 0
        for x in files: 
            z += 1
            file_name = 'npy/' + (x.replace('.jpg', ''))
            if not os.path.exists(file_name + '_1.npy'):
                get_face_descriptor(x)
    do_counter+=1
    requests.post('http://127.0.0.1:8000/done',params={'counter':c})
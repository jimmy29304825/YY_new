import sys  # get argument from PC
from picamera import PiCamera  # control Camera Module
from time import sleep
from io import BytesIO  # write temp data into memory
from PIL import Image  # read images file
import numpy as np  # math
import pymysql
from datetime import datetime

db = pymysql.connect(host='192.168.0.29',
                     port=3306,
                     user='yy_raspi',
                     password='yyraspi',
                     db='yyostech')
cursor = db.cursor()
ids = str(sys.argv[1])  # save argument from PC
# ids = 'testlocal1'
stream = BytesIO()  # build a memory argument
camera = PiCamera()  # build camera module
# camera.rotation = 270
camera.resolution = (3280, 2464)
camera.framerate = 15
camera.start_preview()
sleep(2)
camera.capture(stream, format='jpeg')
camera.stop_preview()
photo_date = str(datetime.now().strftime("%Y%m%d%H%M%S"))
stream.seek(0)
with BytesIO() as output:
    with Image.open(stream) as img:
        img.save(output, 'jpeg')
        # img.save('/home/pi/Desktop/1234.jpg')  # 存入本地端，之後改為存入資料庫
    streamdb = output.getvalue()
sql_insert_blob_query = "INSERT INTO raspi_data(`photo_id`, `image`, `photo_date`) VALUES (%s,%s,%s)"

result = cursor.execute(sql_insert_blob_query, (ids, streamdb, photo_date))
db.commit()
db.close()
print('OK')






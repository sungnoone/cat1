#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
from pymongo import *
import sys
import json
import os

app = Flask(__name__)

## Data Folder variable
log_file = 'cat1_log.txt'
UPLOAD_FOLDER = '/tmp/cat1_Uploads'
DOWNLOAD_FOLDER = '/tmp/cat1_Downloads'

## DB Connection Info
DB_IP = '192.168.1.101'
DB_PORT = 27017
DB_NAME = 'cat1'
DB_COLLECTION = 'posts'
DB_FILE_COLLECTION = 'images'

@app.route('/')
def hello_world():
    log = open(os.path.join('log', log_file), 'a+')
    log.write('>>>Client Connecting into [/api/write/] service.\r\n')
    return 'Hello World!'


@app.route('/api/write/', methods=['GET', 'POST'])
def write_data():
    log = open(log_file, 'a+')
    log.write('>>>Client Connecting into [/api/write/] service.\r\n')

    if request.method == 'POST':
        ##write data
        log.write('Client request [POST].\r\n')
        request_data = request.data
        request_form = request.form
        log.write('System default encoding ['+ sys.getdefaultencoding() + '].\r\n')
        log.write('Client send data [type:'+str(type(request_data))+' value:'+str(request_data, encoding='utf-8') + '].\r\n')
        log.write('Client send form ['+str(request_form) + '].\r\n')

        data = json.loads(str(request_data, encoding='utf-8'))#convert to json
        log.write('data type:'+str(type(data))+'\r\n')

        #in_db_data = {}
        # for item in data:
        #     in_db_data.update()
        #     log.write('item:'+str(item)+'\r\n')
        ##write into db
        ##connect to db operation
        db_connect = MongoClient(DB_IP, DB_PORT)
        db = db_connect[DB_NAME]
        db_collection = db[DB_COLLECTION]
        doc_id = db_collection.save(data)

        log.write('doc id'+str(doc_id)+'\r\n')

        db_connect.close()
        log.close()
        return str('POST OK! '+str(doc_id))
    else:
        ##other method call
        log.write('Client request [' + request.method + '].\r\n')
        return request.method

if __name__ == '__main__':
    app.debug = True
    app.run('192.168.1.109')
import json
import requests
import re
from datetime import datetime
from loggen import fetch_query

global Alarm_list
Alarm_list = []

def calling_log(result):
    extract = json.loads(result)
    if extract['Alarm_Name']:
        func_name = re.sub(r'[^a-zA-Z0-9\s]','',extract['Alarm_Name'])
        start_time = extract['Start_Time']
        start_dt = datetime.strptime(start_time,"%Y-%m-%dT%H:%M:%S.%f%z")
        start_dt = start_dt.replace(microsecond=0,second=0)
        t_stamp = int(start_dt.timestamp())
        start_stamp = int(t_stamp - 600)
        end_stamp = t_stamp
        fun_obj = globals()[func_name]
        fun_obj(func_name,start_stamp,end_stamp)

def "Define_Function_Name"(Alarmname,starttime,endtime):   #Define function same like Alarm name
    print("Alram Name:",Alarmname)
    log_pattern = 'YOUR_ERROR_PATTERN'
    log_group = 'LOG_GROUP_NAME'
    output = fetch_query(log_group=log_group,start_timestamp=starttime,end_timestamp=endtime,query=log_pattern)
    format_test = {'name':Alarmname,'message':output}
    slack_integration(str(json.dumps(format_test)))

def "Defin_Function_name"(Alarmname_1,starttime_1,endtime_1):   #Define function same like Alarm name
    print("Alram Name:",Alarmname_1)
    log_pattern_1 = 'YOUR_ERROR_PATTERN'
    log_group_1 = 'LOG_GROUP_NAME'
    output_1 = fetch_query(log_group=log_group_1,start_timestamp=starttime_1,end_timestamp=endtime_1,query=log_pattern_1)
    format_test_1 = {'name':Alarmname_1,'message':output_1}
    slack_integration(str(json.dumps(format_test_1)))

def "Define Function Name"(Alarmname_4,starttime_4,endtime_4):
    print("Alram Name:",Alarmname_4)
    log_pattern_4 = 'ERROR_PATTERN'
    log_group_4 = 'LOG_GROUP_NAME'
    output = fetch_query(log_group=log_group_4,start_timestamp=starttime_4,end_timestamp=endtime_4,query=log_pattern_4)
    format_test = {'name':Alarmname_4,'message':output}
    slack_integration(str(json.dumps(format_test)))

def slack_integration(output):
    print(output)
    user = 'USER_NAME'   # you can give any name
    chennal = 'CHENNAL_NAME'
    url = 'WEBHOOK_URL'
    message = {
        'channel':chennal,
        'user':user,
        'text':output
    }
    response = requests.post(url,data=json.dumps(message))
    print(response.text)
    
def lambda_handler(event, context):
    print(event)
    Alarm_details = json.loads(event['Records'][0]['Sns']['Message'])
    Alarm_format = {
            'Alarm_Name': Alarm_details['AlarmName'],
            'Start_Time': Alarm_details['StateChangeTime']}
    Alarm_result = json.dumps(Alarm_format)
    calling_log(Alarm_result)

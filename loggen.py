import boto3
from datetime import datetime
import time
import json
global total
import re
total = []
def fetch_query(log_group, query, start_timestamp, end_timestamp):
    response = client_2.start_query(
        logGroupName=log_group,
        startTime=start_timestamp,
        endTime=end_timestamp,
        queryString=query
    )
    query_id = response['queryId']
    print(f"Query started with ID: {query_id}")
    while True:
        time.sleep(2)
        result = client_2.get_query_results(queryId=query_id)
        status = result['status']
        if status == 'Complete':
            return process_results(result,start_timestamp,end_timestamp)
        elif status == 'Failed' or status == 'Cancelled':
            print(f"Query failed or was cancelled. Status: {status}")
            break

def process_results(results,start,end):
    for row in results['results']:
        try:
            return_output = str(row)
            desc_pattern, id_pattern = r'"errors"\s*:\s*\[\s*\{\s*.*?"desc"\s*:\s*"([^"]*)".*?\}\s*\]',r'\[([0-9]+)\]'  # Give the pattern to tae out error details depends on your log events
            desc_search, id_search = re.search(desc_pattern,return_output), re.search(id_pattern,return_output)
            desc,userid = desc_search.group(1), id_search.group(1)
            #output = {'Start':start,'End':end,'Description':desc}
            output = {'User_ID':userid,'Description':desc}
            total.append(output)
        except AttributeError as e:
            desc = 'Not Matched'
            userid = 'NULL'
            output = {'Start':start,'End':end,'Description':desc}
            total.append(output)
            continue
    print(start)
    print(end)
    return total

client_2 = boto3.client('logs')

import json
import boto3

ec2client = boto3.client('ec2',region_name='us-east-1')

def lambda_handler(event, context):

    allInstances = ec2client.describe_instances()
    instanceIdList=[]
    for i in allInstances['Reservations']:
      for j in i['Instances']:
        print (j['InstanceId'])
        instanceIdList.append(j['InstanceId'])            

    print(instanceIdList)
    return instanceIdList
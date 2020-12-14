import json
import boto3

ec2client = boto3.client('ec2',region_name='us-east-1')
snsclient = boto3.client('sns',region_name='us-east-1')

def lambda_handler(event, context):

    ec2_instance_id=event['detail']['instance-id']
    responseTags=ec2client.describe_tags(
        Filters=[
            {
            'Name': 'resource-id',
            'Values': [ec2_instance_id]
            }
            ]
        )
    
    alltags=responseTags['Tags']
    companyTagCode='Company Tag not found'
    for item in alltags:
        if(item['Key']=='companycode'):
            if(item['Value']==''):
                companyTagCode='Company Tag with no value'
            else:
                companyTagCode='OK'
                break

    print(companyTagCode)
    
    if(companyTagCode!='OK'):
        snsarn='arn:aws:sns:us-east-1:558355200489:validationCompanyTag'
        errorMessage='The EC2 instance '+ ec2_instance_id+' has an issue: '+companyTagCode
        
        response = snsclient.publish(
            TopicArn=snsarn,
            Message=errorMessage,
            Subject='EC2 '+ ec2_instance_id+' does not have the set propertly the company tag code'
        )

    return response

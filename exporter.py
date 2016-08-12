import boto3
import csv

s3 = boto3.resource('s3','eu-west-1')

def create_csv():
    regions = [ 'eu-west-1', 'eu-central-1', 'us-east-1', 'ap-southeast-1' ]
    with open('instances.csv', 'wb') as csvfile:
        instancewriter = csv.writer(csvfile, delimiter=',',
                                quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        instancewriter.writerow(['InstanceName', 'InstanceId', 'Platform', 'InstanceType', 'Region'])

        for region in regions:
            ec2 = boto3.client('ec2',region)
            data = ec2.describe_instances()

            for instance in data['Reservations']:
                instanceid = instance['Instances'][0]['InstanceId']
                instancetype = instance['Instances'][0]['InstanceType']
                tags = instance['Instances'][0]['Tags']
                for tag in tags:
                    if 'Name' in tag['Key']:
                        instancename = tag['Value']
                instancewriter.writerow([instancename, instanceid, instancetype, region])
    upload = s3.meta.client.upload_file(
        'instances.csv',
        'lumesse-ie-config',
        'instance_export.csv'
    )

create_csv()

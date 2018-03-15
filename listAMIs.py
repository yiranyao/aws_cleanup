#!/usr/bin/python3

import boto3
from datetime import datetime

cutoff_date = datetime(2018,1,1)
regions = boto3.client('ec2').describe_regions()['Regions']

def list_all_ami(region):
    ec2 = boto3.resource('ec2', region_name=region)
    all_ami = ec2.images.filter(Owners=['self']).all()
    return all_ami

ami_str = 'Region,AMI ID,AMI Name,Create Date,Platform,Description,Tags\r\n'
for region in regions:
    all_ami = list_all_ami(region['RegionName'])
    for ami in all_ami:
        #if datetime.strptime(ami.creation_date, "%Y-%m-%dT%H:%M:%S.%fZ") < cutoff_date:
            ami_str += region['RegionName'] + "," + ami.image_id + "," + ami.name + "," + str(ami.creation_date) + "," 
            try:
                ami_str += str(ami.platform) + ','
            except TypeError:
                ami_str += ','
            try:
                ami_str += '"' + str(ami.description) + '",'
            except TypeError:
                ami_str += ','

            try:
                for tag in ami.tags:
                    ami_str += tag['Key'] + ':' + tag['Value'] + ' '
            except TypeError:
                pass
            except KeyError:
                pass
            ami_str += '\r\n'

print(ami_str)

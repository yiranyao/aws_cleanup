#!/usr/bin/python3

import boto3
from sys import argv
dry_run = False

try:
    filename = argv[1]
except IndexError:
    filename = 'ami_list.csv'

listfile = open(filename, "r")
delete_count = 0
for line in listfile.readlines():
    try:
        region = line.split(',')[0]
        ami_id = line.split(',')[1]
        try:
            if ami_id and ami_id != 'AMI ID':
                ec2 = boto3.client('ec2', region_name=region)
                if dry_run:
                    print(ami_id + " from " + region + " is deleting...")
                    delete_count += 1
                else:    
                    delete_status = ec2.deregister_image(ImageId=ami_id)
                    print(ami_id + " from " + region + " is deleting: " + str(delete_status) + "...")
                    delete_count += 1
        except Exception as err:
            print ("Failed deleting " + ami_id + " from " + region + ": " + str(err))

    except IndexError:
        pass

print(str(delete_count) + " AMI are deleted!")

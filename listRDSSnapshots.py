#!/usr/bin/python3

import boto3
from datetime import datetime, timedelta

cutoff_days = 30
cutoff_date = datetime.now() - timedelta(days=cutoff_days)

def list_all_snapshots(region):
    try:
        rds = boto3.client('rds', region_name=region).describe_db_snapshots()
    except ClientError as err:
        return "Error retrieving snapshot for " + region + ": " + str(err)

    rds_list = rds['DBSnapshots']

    try:
        while rds['Marker']:
            rds = boto3.client('rds', region_name=region).describe_db_snapshots(Marker=rds['Marker'])
            rds_list.append(rds['DBSnapshots'])
    except KeyError:
        pass
    return rds_list

regions = boto3.client('ec2').describe_regions()['Regions']
rds_string = 'Region,SnapshotID,DBInstance,CreateTime,StorageType,StorageSize,SnapshotType\r\n'
for region in regions:
    all_rds = list_all_snapshots(region['RegionName'])
    for rds in all_rds:
        #if rds['SnapshotCreateTime'].replace(tzinfo=None) < cutoff_date:
        if rds['SnapshotType'] != 'automated':
            rds_string += region['RegionName'] + "," + rds['DBSnapshotIdentifier'] + "," + rds['DBInstanceIdentifier'] + "," + str(rds['SnapshotCreateTime']) + "," + rds['StorageType'] + "," + str(rds['AllocatedStorage']) + "GB," + rds['SnapshotType'] + "\r\n"

print (rds_string)

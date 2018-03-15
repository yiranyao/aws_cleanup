#!/usr/bin/python3

import boto3
from datetime import datetime

cutoff_date = datetime(2018,1,1)
regions = boto3.client('ec2').describe_regions()['Regions']

def in_use_snapshots(region):
    volumes = boto3.resource('ec2', region_name=region).volumes.all()
    snapshots = []
    for vol in volumes:
        if vol.snapshot_id not in snapshots:
            snapshots.append(vol.snapshot_id)
    return snapshots

def list_all_snapshots(region):
    snapshots = boto3.client('ec2', region_name=region).describe_snapshots(OwnerIds=['self'])
    snapshot_list = []
    for snapshot in snapshots['Snapshots']:
        snapshot_list.append(snapshot)
    return snapshot_list



snapshot_str = 'Region,SnapshotID,StartTime,Size,Description,Tags,...,...\r\n'
for region in regions:
    all_snapshots = list_all_snapshots(region['RegionName'])
    inuse_snapshots = in_use_snapshots(region['RegionName'])

    for snapshot in all_snapshots:
        if snapshot['StartTime'].replace(tzinfo=None) < cutoff_date and snapshot['SnapshotId'] not in inuse_snapshots:
            snapshot_str += region['RegionName'] + ',' + snapshot['SnapshotId'] + ',"' + str(snapshot['StartTime']) + '",' + str(snapshot['VolumeSize']) + 'GiB,'
            try:
                snapshot_str += '"' + snapshot['Description'] + '",'
            except KeyError:
                snapshot_str += ','
            try:
                tags = ''
                for tag in snapshot['Tags']:
                    tags += str(tag['Key']) + ':' + str(tag['Value']) + ","
                snapshot_str += tags
            except KeyError:
                pass
            snapshot_str += "\r\n"

print(snapshot_str)

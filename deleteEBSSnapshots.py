#!/usr/bin/python3

import boto3
dry_run = False

listfile = open("snapshot_list.csv", "r")
delete_count = 0
for line in listfile.readlines():
    try:
        region = line.split(',')[0]
        snapshotid = line.split(',')[1]
        try:
            if snapshotid and snapshotid != 'SnapshotID':
                ec2 = boto3.client('ec2', region_name=region)
                if dry_run:
                    print(snapshotid + " from " + region + " is deleting...")
                    delete_count += 1
                else:    
                    delete_status = ec2.delete_snapshot(SnapshotId=snapshotid)
                    print(snapshotid + " from " + region + " is deleting: " + str(delete_status) + "...")
                    delete_count += 1
        except Exception as err:
            print ("Failed deleting " + snapshotid + " from " + region + ": " + str(err))

    except IndexError:
        pass

print(str(delete_count) + " snapshots are deleted!")

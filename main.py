#!/usr/bin/env python
# Syntax: ./main.py <action> <region> <tag>
# Usage: ./main.py start|stop us-west-2 ec2_start_stop

import sys

import boto3


def main(action="start", region="us-west-2", tag_start_stop="ec2_start_stop"):
    print('action: ' + str(action))
    print('region: ' + str(region))
    print('tag: ' + str(tag_start_stop))

    ec2 = boto3.client('ec2', region_name=region)
    filters = [
        {
            'Name': 'tag:StartStop',
            'Values': [tag_start_stop]
        }
    ]
    describes = ec2.describe_instances(Filters=filters)

    x = 0
    instances_id = []
    for describe in describes['Reservations']:
        instances_id.append(describe['Instances'][0]['InstanceId'])

    if len(instances_id)>0:
        if action == "start":
            ec2.start_instances(InstanceIds=instances_id)
        elif action == "stop":
            ec2.stop_instances(InstanceIds=instances_id)
        else:
            print('Action ' + str(action) + ' invalid')
            exit(0)

        print(action + 'ing instances: ' + str(instances_id))

    else:
        print('0 instances matched')

    exit(0)


if __name__=="__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])

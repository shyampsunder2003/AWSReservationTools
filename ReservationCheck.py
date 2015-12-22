import pprint
import shlex
import subprocess
from sys import argv
import boto3
import sys

numberOfPossibilities = 5

if len(sys.argv) > 2:
    script, regionMentioned, numberOfPossibilities = argv
elif len(sys.argv) > 1:
    script, regionMentioned = argv
else:
    regionMentioned = ""
numberOfPossibilities = int(numberOfPossibilities)
print regionMentioned, numberOfPossibilities
if regionMentioned == "":
    regionList = ['eu-west-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-central-1', 'ap-northeast-1', 'us-east-1', 'sa-east-1', 'us-west-1', 'us-west-2']
else:
    regionList = [regionMentioned]


for region in regionList:
    print "Checking " + region
    activeReservations = dict()
    client = boto3.client('ec2', region_name=region)
    resource = boto3.resource('ec2',region_name=region)
    response = client.describe_reserved_instances()
    for reservation in response['ReservedInstances']:
        if reservation['State'] == 'active':
            uniqueKey = str(reservation['InstanceType']) + '_' + str(reservation['AvailabilityZone']) + '_' + str(reservation['ProductDescription'])
            if uniqueKey in activeReservations.keys():
                activeReservations[uniqueKey]+=reservation['InstanceCount']
            else:
                activeReservations[uniqueKey]=reservation['InstanceCount']
    instances = resource.instances.filter(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instanceCount = 0
    runningInstances = dict()
    reservationsRunning = dict()
    reservationsRunning.update(activeReservations)
    for instance in instances:
        type = instance.instance_type
        id = instance.id
        if instance.vpc_id is None:
            vpc = 'None'
        else:
            vpc = "Yes"
        if instance.platform is None:
            if vpc == "Yes":
                OS = 'Linux/UNIX (Amazon VPC)'
            else:
                OS = 'Linux/UNIX'
        else:
            if vpc == "Yes":
                OS = 'Windows (Amazon VPC)'
            else:
                OS = 'Windows'
        AZ = instance.placement['AvailabilityZone']
        uniqueKey = type + '_' + AZ + '_'+ OS
        if uniqueKey in activeReservations.keys():
            # if activeReservations[uniqueKey] > 0:
            activeReservations[uniqueKey]-=1
        if uniqueKey in runningInstances.keys():
            runningInstances[uniqueKey]+=1
        else:
            runningInstances[uniqueKey]=1
    unusedReservations = list()
    for key in activeReservations.keys():
        if activeReservations[key] > 0:
            unused = dict()
            unused[key] = activeReservations[key]
            unusedReservations.append(unused)
    if len(unusedReservations) > 0:
        print "\nFollowing are the reservations which are not being utilized right now:"
        for reservation in unusedReservations:
            data = reservation.keys()[0].split('_')
            print "Instance Type: " + data[0],
            print "Region: " + data[1],
            print "OS: " + data[2],
            print "Count: " + str(reservation[reservation.keys()[0]])
    reservationPossibile= False
    for value in activeReservations.values():
        if value < 0:
            reservationPossibile = True
            break
    if reservationPossibile:
        print "\nPossible candidates for extending reservation: "
        ascendingList = sorted(activeReservations, key=activeReservations.get)
        possibilityCount = 0
        for key in ascendingList:
            if activeReservations[key] < 0 and possibilityCount < numberOfPossibilities:
                data = key.split('_')
                print "Instance Type: " + data[0],
                print "Region: " + data[1],
                print "OS: " + data[2],
                print "Running count: " + str(runningInstances[key]),
                print "Reserved count: " + str(reservationsRunning[key]),
                print "Difference: " + str(activeReservations[key]*-1)
                possibilityCount+=1
    ascendingList = sorted(runningInstances, key=runningInstances.get, reverse=True)
    messagePrintOnce = False
    possibilityCount = 0
    for key in ascendingList:
        if key not in reservationsRunning:
            if not messagePrintOnce:
                print "\nPossible candidates which have not been reserved yet: "
                messagePrintOnce = True
            if possibilityCount < numberOfPossibilities:
                data = key.split('_')
                print "Instance Type: " + data[0],
                print "Region: " + data[1],
                print "OS: " + data[2],
                print "Running count: " + str(runningInstances[key])
                possibilityCount+=1



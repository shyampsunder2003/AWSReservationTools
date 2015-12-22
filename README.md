# AWSReservationTools
A bunch of scripts to make reservations easier on AWS

Prerequisites:

1. Boto3, Please ensure that you have this installed in the environment where you want this script to run. https://github.com/boto/boto3 

2. Make sure, Boto3 can pick up the keys for your AWS Setup. You can find this in the Quick Start part of the Boto3 repository.

3. Python 2.xx

Valid Regions
------------- 
eu-west-1, ap-southeast-1, ap-southeast-2, eu-central-1, ap-northeast-1, us-east-1, sa-east-1, us-west-1, us-west-2

Script Usage
------------- 
```
python checkReservation.py [Region] [Number of Possibilities]
```

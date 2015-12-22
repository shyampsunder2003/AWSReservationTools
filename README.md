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

Region (Optional): Specifies the region where this script needs to be run
Number of Possibilities (Optional): Specifies the number of suggesstions the script can make per region about improving reservations
```
This script takes into account the OS, Region, AZ, Type and VPC status of an instance for mapping it to an AWS Reservation.

The OS Field has been broadly split into:

1. Unix/Linux (Amazon VPC)

2. Unix/Linux

3. Windows (Amazon VPC)

4. Windows

Disclaimers
-------------

1. Please note that AWS has several premium OS offerings which will not be detected by this script because there is no reliable way of getting this information via Boto/AWS CLI. Example:
Windows Server 2003 Web or Windows Server 2003 Standard

2. The script has support for tenancy but has not been tested for it.

import boto3
from Helper.AWSSesion import AWS_Session
import pprint
import json

class ES_Describe():

    null = ""

    def  __init__(self, awsClient:AWS_Session, domainNameScale:any, startTime: any, endTime: any):
        self.awsClient = awsClient
        self.domainNameScale = domainNameScale
        self.startTime = startTime
        self.endTime = endTime

    def DescribeESDomain(self):
        esRequest = self.awsClient.client('es')
        response = esRequest.list_domain_names()['DomainNames']
        if response != "":
            for object in response:
                domainName = object['DomainName']
                print('Domain name: ',domainName )
                if domainName != self.domainNameScale:
                    print('not matched scale domain name')
                else:
                    print('found domainname to scale, process checking and scale')
                    self.ScaleDomainName(domainName)
        else:
            print("Dont have any domain name or matched for scale out")

    def ScaleDomainName(self, domainNameScale:any):
        #get domain name config
        esRequest = self.awsClient.client('es')
        response = esRequest.describe_elasticsearch_domain(DomainName=domainNameScale)
        if response != self.null:
            #set condition add node
            volumneAvalable = 5 # with free 5Gb then scale by add more node
            #get volumeSize
            configVolumneSize = response['DomainStatus']['EBSOptions']['VolumeSize']
            vpcEndpoint = response['DomainStatus']['Endpoints']
            resultCheckCloudWatch = self.DescribeCloudWatchAttachmentWithClusterES(domainNameScale,self.startTime,self.endTime)
            if resultCheckCloudWatch == self.null:
                print("Can not checking data. stop services")
                return

    def DescribeCloudWatchAttachmentWithClusterES(self, domainNameScaleToCheck, startTime: any,endTime:any):
        print(startTime)
        print(endTime)
        cwClient = self.awsClient.client('cloudwatch','ap-southeast-1')
        response = cwClient.get_metric_statistics(
            Namespace = "AWS/ES",
            MetricName ="FreeStorageSpace",
            Dimensions = 
            [
                { 
                    'Name':'DomainName',
                    'Value': domainNameScaleToCheck
                }
            ],
            StartTime = startTime,
            EndTime = endTime,
            Period = 86400,
            Statistics = ['Average'],
            Unit = 'Gigabytes',
            )
        print(response)
        return self.null
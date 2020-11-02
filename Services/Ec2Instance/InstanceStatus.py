import boto3
from Helper.AWSSesion import AWS_Session

class InstanceStatus(object):
    null = ""
    
    def __init__(self, config, awsCredential, notificationServices):
        self.config = config
        self.awsCredential = awsCredential
        self.notificationServices = notificationServices

    def CheckInstanceStatus(self):
        awsClient = self.awsCredential.Get_Credentials()
        ec2_client = awsClient.client('ec2',self.config['Credentials']['AWS']['Region'])
        ConditionMonitor = self.config['ConditionMonitor']['Tags']
        instances = ec2_client.describe_instances()['Reservations']
        for instance in instances:
            tags = instance['Instances'][0]['Tags']
            for condition in ConditionMonitor:
                for tag in tags:
                    if condition == tag['Value']:
                        if instance['Instances'][0]['State']['Code'] == 80:
                            #encapsulution message violation instance
                            instanceId = instance['Instances'][0]['InstanceId']
                            self.notificationServices.SendingMessage('Instance stopped','Instance Id: ' + instanceId)

    
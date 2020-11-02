from dependency_injector import containers, providers
from dependency_injector.wiring import Provide

#import class
from Notifications.Teams import MSTeams
from Services.Ec2Instance.InstanceStatus import InstanceStatus
from Helper.AWS_Credential import AWSCredential

#load config
class Configs (containers.DeclarativeContainer):
    config = providers.Configuration('config')

class AWSCredentials(containers.DeclarativeContainer):
    awsConfig = providers.Singleton(AWSCredential, Configs.config)

class NotificationServices(containers.DeclarativeContainer):
    msTeams = providers.Singleton(MSTeams,Configs.config)

class InstanceStatusCheck(containers.DeclarativeContainer):
    instanceCheck = providers.Factory(InstanceStatus,Configs.config, awsCredential = AWSCredentials.awsConfig, notificationServices = NotificationServices.msTeams)



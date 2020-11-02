import os
import logging
import json
from Helper.PreRunningChecking import CheckingEnv
# from Helper.AWSSesion import AWS_Session
from Controller.DescribeElasticSearchServices import ES_Describe
from datetime import datetime,timedelta,timezone
from Containers.containers import NotificationServices,InstanceStatusCheck, Configs, AWSCredentials


# init logging
logging.basicConfig(format='%(asctime)s %(process)d %(levelname)s %(name)s %(message)s', level=logging.INFO,filename="log.txt")
logger = logging.getLogger(__name__)
logger.info('Logger init ... OK')


#define function monitoring aws elasticsearch by 5 minutes

def roundTime(dt=None, roundTo=60):
   if dt == None : dt = datetime.datetime.now()
   seconds = (dt.replace(tzinfo=None) - dt.min).seconds
   rounding = (seconds+roundTo/2) // roundTo * roundTo
   return dt + timedelta(0,rounding-seconds,-dt.microsecond)  

#main function

if __name__ == '__main__':

    preChecking = CheckingEnv()
    # #checking env
    print('Checking system requirement boto3 version and install if needed')
    checkingCMD = "pip3 show boto3"
    resultchecking = preChecking.executioner(checkingCMD,checkingCMD,0)
    if resultchecking:
        print('Passed enviroment and requirement')
    else:
        installModule = 'pip3 install boto3'
        preChecking.executioner(installModule,installModule,0)

    print('Starting services...')
    #loading json config file 
    appConfig = open("Configs/appconfig.json")
    configData = json.load(appConfig)
    #injection config data
    Configs.config.override(configData)

    awsServices = AWSCredentials.awsConfig()
    teamsMessage = NotificationServices.msTeams()

    teamsMessage.SendingMessage("Information Services","Starting services")

    # #set up time interval
    # timeStamp = 1
    Ec2Instance = InstanceStatusCheck.instanceCheck()
    Ec2Instance.CheckInstanceStatus()
        #init scale object
        #int time
        #while True:
        #after 60 minutes then check data
        #currentTime = int(datetime.utcnow().strftime("%M"))
        #if currentTime % timeStamp == 0:
        #utcDate = datetime.now(timezone.utc)
        # startTime = datetime.utcnow() - timedelta(hours=1,minutes=20)
        # startTime = roundTime(startTime)
        # endTime = roundTime(datetime.utcnow())
        #startTime = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
        #endTime = utcDate.strftime("%Y-%m-%d")
        #init ES module
        #esDescribe = ES_Describe(awsClient,scaleDomainName,startTime,endTime)
        #esDescribe.DescribeESDomain()
    print("Terminated")


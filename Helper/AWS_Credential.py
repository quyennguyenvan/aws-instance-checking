from Helper.AWSSesion import AWS_Session

class AWSCredential(object):
    def __init__(self,config):
        self.config = config

    def Get_Credentials(self):
        awsClient = AWS_Session(self.config['Credentials']['AWS']['AccessKey'],self.config['Credentials']['AWS']['SecretKey'])
        awsClient.get_credentials()
        return awsClient

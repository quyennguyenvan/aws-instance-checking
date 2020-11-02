import pymsteams
class MSTeams(object):
    def __init__(self, config):
        self.config = config

    def SendingMessage(self,title, message):
        teamNotify = pymsteams.connectorcard(self.config['Notifications']['Teams']['HookURL'])
        teamNotify.title(title)
        teamNotify.text(message)
        teamNotify.send()
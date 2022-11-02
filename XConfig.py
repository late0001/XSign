from configparser import ConfigParser
class XConfig:
    def __init__(self): 
        cfg = ConfigParser()
        cfg.read('config.ini')
        self.cfg = cfg
        
    def getAccConfig(self):
        cfg =self.cfg
        self.certsign_username = cfg.get('certsign', 'username')
        self.certsign_password = cfg.get('certsign', 'password')
        self.iflow_username = cfg.get('iflow', 'username')
        self.iflow_password = cfg.get('iflow', 'password')
        self.email_username = cfg.get('email', 'username')
        self.email_password = cfg.get('email', 'password')
        self.coeff11n = cfg.get('iflow', '11n')
        self.coeff11ac = cfg.get('iflow', '11ac')
        self.coeff11ax = cfg.get('iflow', '11ax')
        self.mspt_usr = cfg.get('ms_sign', 'username')
        self.mspt_pwd = cfg.get('ms_sign', 'password')
    
    def getBuildEnvConfig(self):
        cfg =self.cfg
        self.tracefmt = cfg.get('BuildEnvironment', 'tracefmt')

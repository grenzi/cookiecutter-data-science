# -*- coding: utf-8 -*-

################################################################################
## imports
try:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
except:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), '..', '..')))
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.getcwd()), '..')))

################################################################################
## logging setup
def getmodname():
    return __name__ or 'project'
logger = logging.getLogger(getmodname())
logger.debug(getmodname() + 'loaded')

################################################################################
## 

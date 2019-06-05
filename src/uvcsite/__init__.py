## i18n
from zope.i18nmessageid import MessageFactory
uvcsiteMF = MessageFactory('uvcsite')


### LOGGING
import logging
logger = logging.getLogger('uvcsite')

def log(message, summary='', severity=logging.INFO, extra_data=None):
    logger.log(severity, '%s %s', summary, message, extra=extra_data)

import logging


def send(cellphone, content):
    """
    发送短信 mock todo
    """
    logging.info('sms_sender mock send %s -> %s ' % (cellphone, content))

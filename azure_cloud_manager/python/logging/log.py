import logging
logging.basicConfig(filename='example.log', format='%(asctime)s %(message)s', filemode='w', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

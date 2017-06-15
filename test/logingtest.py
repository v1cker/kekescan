import logging

logging.basicConfig(level=logging.DEBUG,
	format='[%(asctime)s] [%(levelname)s] %(message)s %(filename)s[line:%(lineno)d]   ',
	datefmt='%a, %d %b %Y %H:%M:%S',
	#format='[%(asctime)s] [%(levelname)s] %(message)s',
	#datefmt= "%H:%M:%S",
	filename='xlcscan.log',
	filemode='a')


console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('kafka')
install('pykafka')
install('tweepy')
install('mysql')
install('mysql-connector-python-rf')

import kafka_push_listener
# import mysql_db
# starts in python-scripts container

import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# installations, could be with requirements.txt
install('kafka')
install('pykafka')
install('tweepy')
install('mysql')
install('mysql-connector-python-rf')

# starting listener
import kafka_push_listener
import logging
import sys
import main

sys.path.insert(0,"/var/www/app/")
logging.basicConfig(stream=sys.stderr)

app = main.app


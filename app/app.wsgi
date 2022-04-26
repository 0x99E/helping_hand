#!/usr/bin/python3
import logging
import sys
import main

sys.path.insert(0,"/var/www/app/")
logging.basicConfig(stream=sys.stderr)

application = main.app


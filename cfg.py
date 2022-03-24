import logging
import os
import sys

g_loglevel = logging.INFO

#WORKING DIRECTORY Log Path
g_logpath = os.getcwd()

#Or CUSTOM Log Path
# g_logpath = ""

g_logname = "smtp_oauth_python_gmail.log"
g_log = os.path.join(g_logpath, g_logname)

fh = logging.FileHandler(filename=g_log)
fh.setLevel(logging.DEBUG)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
handlers = [fh, sh]
logging.basicConfig(format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
                    handlers=handlers
                    )
SMTP_SERVER = 'smtp.gmail.com'  # Email Server (don't change!)
SMTP_PORT = 587  # Server Port (don't change!)
SMTP_EMAIL = "yourusername@example.com"
#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
import logging
import os
import sys
import logging.config

"""
logging.config.fileConfig("common/logging.conf")

fh = logging.FileHandler("log/vmservice.log")
fh.setLevel("DEBUG")
formatter = logging.Formatter('%(asctime)s %(filename)s:%(lineno)s-%(levelname)s-%(message)s')
fh.setFormatter(formatter)
#logger = logging.getLogger("")
logger = get_task_logger(__name__)
logger.addHandler(fh)
"""

LOGGING_MSG_FORMAT  = '[%(asctime)s] [%(levelname)s] [%(filename)s] [%(funcName)s] [%(lineno)d] %(message)s'
LOGGING_DATE_FORMAT	= '%Y-%m-%d %H:%M:%S'

logging.basicConfig(level=logging.DEBUG,format=LOGGING_MSG_FORMAT,datefmt=LOGGING_DATE_FORMAT)
logger = logging.getLogger(__name__)
log_path = os.path.join(r"./")
if not os.path.exists(log_path):
   os.makedirs(log_path)
log_file = os.path.join(log_path,'notify_adviser.log')
fh = logging.handlers.TimedRotatingFileHandler(log_file,'midnight',1)
fh.setFormatter(logging.Formatter(LOGGING_MSG_FORMAT))
logger.addHandler(fh)











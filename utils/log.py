#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
import logging


class LoggerFactory:
   """
   logger工厂类
   """
   LOGGING_MSG_FORMAT = '[%(asctime)s]-[%(levelname)s]-[%(filename)s]-[%(funcName)s]-[%(lineno)d] %(message)s'
   LOGGING_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


   @staticmethod
   def create(filename):
      logging.basicConfig(level=logging.DEBUG, format=LoggerFactory.LOGGING_MSG_FORMAT, datefmt=LoggerFactory.LOGGING_DATE_FORMAT)
      logger = logging.getLogger()
      fh = logging.FileHandler(filename)
      logger.addHandler(fh)

      return logger










# coding: utf-8

import sys
import logging
logger = logging.getLogger("nuage-learning")
logger.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)

logger.addHandler(ch)
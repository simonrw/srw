#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import argparse
import logging
import ds9

logging.basicConfig(
    level='DEBUG', format='%(asctime)s|%(name)s|%(levelname)s|%(message)s')
logger = logging.getLogger(__name__)


def main(args):
    logger.debug(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('-r', '--ra', required=True, type=float)
    parser.add_argument('-d', '--dec', required=True, type=float)
    main(parser.parse_args())

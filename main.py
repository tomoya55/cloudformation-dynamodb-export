#!/opt/brew/opt/python/bin/python3.7
# -*- coding: utf-8 -*-
import re
import sys

from cloudformation_dynamodb_export.cfn2ddb import export

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(export())

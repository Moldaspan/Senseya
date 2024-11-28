#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'senseya.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

import jwt
from django.conf import settings

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTEsImVtYWlsIjoibWFkaW51ckBnbWFpbC5jb20iLCJleHAiOjE3MzI4MTA5NDYsImlhdCI6MTczMjgwNzM0Nn0.USTqRVpHLVhM4oGWaPxSxERiuTLBH4Xottnqw11O-Ns"
try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    print("Decoded payload:", payload)
except jwt.ExpiredSignatureError:
    print("Token has expired!")
except jwt.DecodeError:
    print("Invalid token!")

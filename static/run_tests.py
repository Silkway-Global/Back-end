#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'static.settings')
django.setup()

import unittest
from django.test.runner import DiscoverRunner

if __name__ == '__main__':
    test_runner = DiscoverRunner(verbosity=2)
    failures = test_runner.run_tests([
        'accounts',
        'blog',
        'courses',
        'testimonials',
        'appointments',
        'contacts',
    ])
    sys.exit(bool(failures)) 
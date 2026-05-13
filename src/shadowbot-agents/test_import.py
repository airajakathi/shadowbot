#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src/shadowbot-agents')

import warnings
warnings.simplefilter('always')

print("Testing import with warnings enabled...")
import shadowbotagents
print("Import successful!")
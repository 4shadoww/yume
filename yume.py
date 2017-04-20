#!/usr/bin/env python3

# Import python modules
import sys

# Append lib path
sys.path.append("core/lib/")

# Import core modules
from core.worker import Worker

def main():
	worker = Worker()

	worker.run()

if __name__ == "__main__":
	main()

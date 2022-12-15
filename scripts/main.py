import os
import random
import time

startTime = time.time()

os.system("python post_analysis.py")

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
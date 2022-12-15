import os
import time

startTime = time.time()

os.system("python scripts_hw/post_analysis_hw.py")

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
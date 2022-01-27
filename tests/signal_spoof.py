'''


This script is for testing the backend. It alternates between negative & positive for 'train' every 5 minutes and sends a correspondi.
1. send close signal
2. wait(5min)
3. send open signal
4. repeat
'''
import time
while(True):

    time.sleep(5)
    # send a 1
    print("Train detected.")

    time.sleep(5)
    # send a 0
    print("All clear.")

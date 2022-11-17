import threading, time  
def doWaiting():  
    print ('start waiting1: ' + time.strftime('%H:%M:%S') + "\n")
    time.sleep(3)  
    print ('stop waiting1: ' + time.strftime('%H:%M:%S') + "\n")
def doWaiting1():  
    print ('start waiting2: ' + time.strftime('%H:%M:%S') + "\n")   
    time.sleep(8)  
    print ('stop waiting2: ', time.strftime('%H:%M:%S') + "\n") 


''' 
for i in range(50):
    print(i)
    time.sleep(0.5)
tsk = []    
thread1 = threading.Thread(target = doWaiting)  
thread1.start()  
tsk.append(thread1)
thread2 = threading.Thread(target = doWaiting1)  
thread2.start()  
tsk.append(thread2)
print ('start join: ' + time.strftime('%H:%M:%S') + "\n")  
for tt in tsk:
    tt.join()
print ('end join: ' + time.strftime('%H:%M:%S') + "\n")
 '''

''' for i in range(1, 10):
    print(' '.join([f"{i}*{j} = {i*j:2d}" for j in range(1, 10)]))
 '''


''' N=2
W=[[740, 516, 725, 718, 861, 634, 723],
    [914, 747, 580, 593, 722, 877, 595]]

minn = min([min(w) for w in W]) '''

nums = [100,200,500,2000]
K = 1000
Output: 700
max = 0
for i in range(len(nums)):
    for j in range(i, len(nums)):
        if nums[i] + nums[j] < K:
            if nums[i] + nums[j] > max:
                max = nums[i] + nums[j]

max = [nums[i] + nums[j]] for i in range(len(nums)) for j in range(i, len(nums)) if nums[i] + nums[j] < K

print(max)
    


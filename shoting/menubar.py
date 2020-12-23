start=10
step=1
count=0
for i in range(100):
    start+=step
    count=+1
    if start>20:
        step*=-1
        count*=step
        
    print(count)
    
    

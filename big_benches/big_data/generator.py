import random as rand
its0 = ['car','cat','dog','person','error']
its1 = ['pencil','flower','rock','tree','bush']
with open('meta_input.txt','w+') as f:
    for _ in range(1000000000):
        it = ''
        lis = rand.randrange(1,4)
        i = rand.randrange(0,5)
        if lis > 2:
            it = its1[i]
        else:
            it = its0[i]
        f.write(it+'\n')
        
        

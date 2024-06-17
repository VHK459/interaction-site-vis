import glob 

l = glob.glob('*.csv')

with open('names.txt','a') as f:
    for i in l:
        f.write(f'{i}\n')

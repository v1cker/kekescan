f = open('domain.txt')

def hello(f):
    d_list = []
    for i in f:
        i = i.strip()
        if i not in d_list:
            d_list.append(i)


    print d_list

def findb(f):
    for i in f:
        i = i.strip()
        i_list =i.split('.')
        if len(i_list) > 2:
            if not(( i_list[2]  == 'cn' and i_list[1]  == 'gov')  or ( i_list[2]  == 'cn' and i_list[1]  == 'com')or ( i_list[2]  == 'cn' and i_list[1]  == 'edu')):
                print i
        
        
findb(f)

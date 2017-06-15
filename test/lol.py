attack_target_list  = [u'33,111']
size = 1 
lol = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)] 
for i in lol(attack_target_list,size):
	print i
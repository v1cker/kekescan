import requests
import json
import time

flower_api = "http://127.0.0.1:5555/"

#task add
data = {"args": ['1,100000000000000',]}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain','Connection':'close'}

r = requests.post(flower_api+'api/task/send-task/app.tasks.add', data=json.dumps(data), headers=headers)


print r.status_code
print r.json()
#get task results
resp = r.json()
task_id =  resp['task-id']

#time.sleep(3)
for i in range (1,2):
	r = requests.get(flower_api+'api/task/result/'+task_id,headers=headers)
	print r.json()

# get task info 
time.sleep(2)
r = requests.get(flower_api+'api/task/info/'+task_id,headers=headers)
print r.json()

#	List workers
time.sleep(2)
r = requests.get(flower_api+'api/workers',headers=headers)
print r.json()


# shutdown worker
data = {    "message": "Shutting down!"}
#r = requests.post(flower_api+'api/worker/pool/restart/celery@ubuntu', data=json.dumps(data), headers=headers)
#print r.json()


#restart worker

data = {    "message": "Restarting 'celery@ubuntu' worker's pool"}
#r = requests.post(flower_api+'api/task/send-task/celery@ubuntu', data=json.dumps(data), headers=headers)
#print r.json()

import Queue
import threading
import docker
import time
import numpy as np
import os
# 创建容器时需要将容器oid模式设置为“host”，在容器内部将会使用宿主机的host pid

q = Queue.Queue(maxsize = 128)
erro1 = 'CUBLAS_STATUS_NOT_INITIALIZED'


class Task(object):
	def __init__(self, containerName, taskName):
		self.containerName = containerName
		self.taskName = taskName
		return
			

def task_inqueue(container):
	logs = container.logs(stderr = True)
	error = logs.readlines()
	for err in error:
		if erro1 in err:
			# 获取taskName,container
			os.system('docker exec -d container task_name')
			task = new Task(self, container, task_name)
			q.put(task)


def process_task(task):
	while True:
		os.system('nvidia-smi -q -d Memory |grep -A4 GPU|grep Free >tmp')
		memory_gpu=[int(x.split()[2]) for x in open('tmp','r').readlines()]
		max_source = np.argmax(memory_gpu)
		os.environ['CUDA_VISIBLE_DEVICES']=str(max_source)
		if max_source> 2048:
			#执行当前命令
			taskName = task.taskName
			container = task.containerName
			os.system('docker exec -d container taskName')
			return True

		else:
			time.sleep(2)


def main():
	# 系统打开时，实时监测docker运行情况 
	while True:
		client = docker.docker.Client(host, port)
		# 获取正在运行的container		
		for containner in Containers:
			task_inqueue(container)
		while  not q.isEmpty():
			task = q.get()
			if process_task:
				continue




if __name__ == '__main__':
	main()




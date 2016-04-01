import requests,sys,time

app = sys.argv[1]
cases = sys.argv[2]
buildid = sys.argv[3]

device_url = "http://localhost:5000/getdevicestatusfromjenkins"
newjob_url = "http://localhost:5000/newjobfromjenkins"

devices = requests.get(device_url).json()
if not devices:
	print("[error]no device can be used")
	sys.exit(-1)

runjob_url = "http://localhost:5000/runjobfromjenkins/%s" %buildid
status_url = "http://localhost:5000/getjobstatusfromjenkins/%s" %buildid


data = {
	"app":app,
	"type":3,
	"cases":cases,
	"devices":devices,
	"buildid":buildid
}

print("[action]create new testjob with buildid:%s" %buildid)
result_new = requests.post(newjob_url,data=data).json()

if result_new["result"]:
	print("[status]success")
	print("[action]running testjob with buildid:%s" %buildid)
	result_run = requests.get(runjob_url).json()
	started = False
	if result_run["result"]:
		start = time.time()
		while time.time() - start < 600 :
			r = requests.get(status_url).json()
			if not r["result"]:
				if not started:
					started = True
					print("[status]%s" %r["errorMsg"])

				time.sleep(2)
			else:
				if r["status"]:
					print("[status]success")
					sys.exit(0)
				else:
					print("[status]failed:AutomationTest Failed!")
					sys.exit(-1)
		else:
			print("[status]failed:Job timeout - 1800s")
	else:
		print("[status]failed:%s" %result_run["errorMsg"])
		print("see details: http://localhost:5000")
		sys.exit(-1)

else:
	print("[status]failed:%s" %result_new["errorMsg"])
	sys.exit(-1)
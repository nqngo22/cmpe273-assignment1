#Nguyen Ngo
import sys, requests, base64, os, json, yaml
from flask import Flask

app = Flask(__name__)
url = None
repository = None
apiURL = "https://api.github.com/repos/"

@app.route("/")
def hello():
	return "Hello from Dockerized Flask App!!"

@app.route("/v1/<fileName>")
def getFile(fileName):
	jsonFormat = False
	#Check whether user wants yml or json
	if fileName.endswith(".json"):
		jsonFormat = True
		#If user wants json, retrieve content by converting extension to yml
		fileName = os.path.splitext(fileName)[0]+'.yml'
	#Full url for github API
	fullURL = apiURL + fileName
	r = requests.get(fullURL)
	if r.status_code == requests.codes.ok:
		#Get file content in base64 encoding
		contentBase64 = r.json()['content']
		#Decode base64 string
		contentDecoded = base64.b64decode(contentBase64)
		if jsonFormat == True:
			#Convert content to JSON by user request
			contentDecoded = json.dumps(yaml.load(contentDecoded), indent=2)
		return contentDecoded
	else:
		return str(r.status_code)

if __name__ == "__main__":
	if len(sys.argv) == 2:
		url = sys.argv[1]
		#split github link and user repository
		repository=url.split("https://github.com/",1)[1]
		apiURL = apiURL + repository + "/contents/"
		app.run(debug=True,host='0.0.0.0')
	else:
		print "Usage: app.py <github url>"

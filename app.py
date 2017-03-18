#Nguyen Ngo
import sys, json, yaml, os
from flask import Flask
from github import Github

app = Flask(__name__)
user = None
repository = None
GitHubURL = "https://github.com/"

@app.route("/")
def hello():
	return "Hello from Dockerized Flask App!!"

@app.route("/v1/<fileName>")
def getFile(fileName):
	if not (fileName.endswith("-config.yml") or fileName.endswith("-config.json")):
		return "File must be in {environment}-config.yml or {environment}-config.json format"

	jsonFormat = False
	#Check whether user wants yml or json
	if fileName.endswith(".json"):
		jsonFormat = True
		#If user wants json, retrieve content by converting extension to yml
		fileName = os.path.splitext(fileName)[0]+'.yml'
	g = Github()

	repo = g.get_user(user).get_repo(repository)

	try:
		contentDecoded = repo.get_file_contents(fileName).content.decode('base64')
	except Exception as e:
		return str(e)

	if jsonFormat == True:
		contentDecoded = json.dumps(yaml.load(contentDecoded), indent=2)

	return contentDecoded

if __name__ == "__main__":
	if len(sys.argv) == 2:
		url = sys.argv[1]
		if url.startswith(GitHubURL):
			#split github link and user repository
			args = url.split('/', 4)
			user = args[3]
			repository = args[4]
			app.run(debug=True,host='0.0.0.0')
		else:
			print "Invalid GitHub url"
	else:
		print "Usage: app.py <github url>"

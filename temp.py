
if __name__ == "__main__":
	linecounter = 0
	body_started = False
	with open('seattle.html') as f:
		for line in f:
			if (not body_started) and ('<pre>' in line):
				body_started = True
			
			if body_started:
				linecounter += 1
				if linecounter > 6 and linecounter < 31:
					print(line)

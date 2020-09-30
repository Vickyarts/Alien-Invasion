import json

files = 'save.json'

def dump_res(xwidth,xheight):
	"""To change the resolution of the game"""
	try:	
		with open(files) as f:
			reses = json.load(f)
	except Exception:
		with open(files,'w') as f:
			xdimen = (xwidth,xheight,0)
			json.dump(xdimen,f)
	else:	
		with open(files,'w') as f:
			xdimen = (xwidth,xheight,reses[2])
			json.dump(xdimen,f)

width = int(input('Enter the width: '))
height = int(input('Enter the height: '))

dump_res(width,height)

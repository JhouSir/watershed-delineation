import time, sys, getopt

typex = 90
lenx = None

dir_arr = [None] * 10
dir_arr[0] = [0,0]
dir_arr[1] = [-1,1]
dir_arr[2] = [0,1]
dir_arr[3] = [1,1]
dir_arr[4] = [-1,0]
dir_arr[5] = [0,0]
dir_arr[6] = [1,0]
dir_arr[7] = [-1,-1]
dir_arr[8] = [0,-1]
dir_arr[9] = [1,-1]

def find_watershed(x, y, watershed_image_data):
	global lenx
	if typex == 500:
		w = 1741
		h = 1057
		x=x-1
		y=h-y-1
	else:
		w=5900
		h=3680
		y=h-y-1

	
	matrix = [None] * (w*h)
	matrix[x+(w*y)] = 1
	j = 1
	dirf = [-1,0,1,-1,1,-1,0,1]
	dirg = [1,1,1,0,0,-1,-1,-1] 
	e = [9, 8, 7, 6, 4, 3, 2, 1]

	
	process = [None] * (11000*4)
	process[0] = x
	process[1] = y
	c = 2
	o1 = 0
	o2 = 5500
	
	while c>o1:
		numbr3 = o1
		o1 = o2
		o2 = numbr3 + o1 - o2
		lenx = c
		c = o1
		k = o2
		r2 = range(7,-1,-1)
		for i in range(k,lenx,2):
			arx = process[i]
			ary = process[i+1]
			for j in r2:
				nx = arx + dirf[j]
				ny = ary + dirg[j]
				ind = ny*w+nx
				if watershed_image_data[ind] == e[j]:		
					process[c]=nx
					c+=1
					process[c]=ny
					c+=1
					matrix[ind]=1
		
	
	
	dirx = [0,0,1,0,-1]
	diry = [0,-1,0,1,0]
	dirxyr = [0,-w,1,w,-1]
	found = 1
	curX = x
	curY = y
	dirnew = 1
	border = []
	sdir1 = [1,2,3,4,1]
	sdir3 = [3,4,1,2,3]
	sdir4 = [2,3,4,1,2]
	offsetx = 1
	if typex == 500:
		pass

	else:
		dir1 = sdir1[dirnew]
		dir3 = sdir3[dirnew]
		dir4 = sdir4[dirnew]
		ofs = curX+w*curY
		if not matrix[ofs+dirxyr[dir1]]:
			dirnew = dir1
		elif not matrix[ofs+dirxyr[dirnew]]:
			pass
		elif not matrix[ofs+dirxyr[dir3]]:
			dirnew = dir3
		elif not matrix[ofs+dirxyr[dir4]]:
			dirnew = dir4
		else:
			dirnew = 0

		curX = curX + dirx[dirnew]
		curY = curY + diry[dirnew]
		border.append(11.5+curX+offsetx)
		border.append(88.5+curY)

		icurX = curX
		icurY = curY

		dir1 = sdir1[dirnew]
		dir3 = sdir3[dirnew]
		dir4 = sdir4[dirnew]
		ofs = curX+w*curY
		if not matrix[ofs+dirxyr[dir1]]:
			dirnew = dir1
		elif not matrix[ofs+dirxyr[dirnew]]:
			pass
		elif not matrix[ofs+dirxyr[dir3]]:
			dirnew = dir3
		elif not matrix[ofs+dirxyr[dir4]]:
			dirnew = dir4
		else:
			dirnew = 0

		curX = curX + dirx[dirnew]
		curY = curY + diry[dirnew]
		border.append(11.5+curX+offsetx)
		border.append(88.5+curY)

		while found>0:
			dir1 = sdir1[dirnew]
			dir3 = sdir3[dirnew]
			dir4 = sdir4[dirnew]
			ofs = curX+w*curY
			if not matrix[ofs+dirxyr[dir1]]:
				dirnew = dir1
			elif not matrix[ofs+dirxyr[dirnew]]:
				pass
			elif not matrix[ofs+dirxyr[dir3]]:
				dirnew = dir3
			elif not matrix[ofs+dirxyr[dir4]]:
				dirnew = dir4
			else:
				dirnew = 0

			curX = curX + dirx[dirnew]
			curY = curY + diry[dirnew]
			if icurX == curX and icurY == curY:
				found = 0
			else:
				border.append(11.5+curX+offsetx)
				border.append(88.5+curY)


	print("Total Border Length: ", len(border))

	return border


def save_to_bin(border, file):
	pass

def save_to_kml(border, file):
	dx = 0.0011797277777777777
	dy = 0.0011797277777777777
	kml = ''
	# kml generation
	for i in range(0,lenx):
		lng=-96.9579313+border[2*i]*dx
		lat=40.3024337946+(3680-border[2*i+1]-1)*dy
		kml+=''+str(round(lng,6))+','+str(round(lat,6))+',0 '
	content = '<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://www.opengis.net/kml/2.2" xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom"><Document><Placemark><name>Watershed boundary generated by IFIS</name><Style id="basin_boundary"><LineStyle><color>FF0000FF</color><width>1</width></LineStyle><PolyStyle><color>26000000</color><fill>1</fill></PolyStyle></Style><Polygon><outerBoundaryIs><LinearRing><coordinates> ' + kml + ' </coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark></Document></kml>';
	with open(file, "w+") as f:
		f.write(content)

def get_data_from_image(img):
	from PIL import Image
	t2 = time.time()
	imgobj = Image.open(img)
	pixels = imgobj.convert('RGBA')
	watershed_image_data = pixels.getdata(0)
	t3 = time.time()
	print('Data Length: '+str(len(watershed_image_data)))
	print('Image Draw Time: '+str((t3-t2))[:4]+' sec(s)')
	return watershed_image_data


def get_data_from_bin(bin):
	pass


def no_print(*args, **kwargs):
	pass

def main(argv):
	t1 = time.time()
	outputfile = "ws.out" 
	inputfile = ""
	inputtype = "bin"
	outputtype = "kml"
	err = """Usage: python watershed.py 	[-h] [-i inputfile] [-o outputfile] [-t bin|png]
				[-z bin|kml] [-x xvalue] [-y yvalue] [-r]
Options:
-r 			: don't print outputs
-h 			: help
-i inputfile		: indicate input file's path
-o outputfile		: indicate output file's path, default=ws.out
-t bin|png 		: type of input, either bin or png, default=bin
-z bin|kml 		: type of output, either kml or bin, defaul=kml
-x xvalue		: x value of the target point, should be integer
-y yvalue 		: y value of the target point, should be integer"""

	try:
		opts, args = getopt.getopt(argv,"rhi:o:x:y:t:z:",["ifile=","ofile=","itype=", "otype=", "xvalue=", "yvalue="])
	except getopt.GetoptError:
		print(err)
		sys.exit(2)

	if ('-r', '') in opts:
		__builtins__.print = no_print

	for opt, arg in opts:
		if opt == '-h':
			print(err)
			sys.exit()
		elif opt in ("-i", "--ifile"):
			print("Input File: ", arg)
			inputfile = arg
		elif opt in ("-o", "--ofile"):
			print("Output File: ", arg)
			outputfile = arg
		elif opt in ("-t", "--itype"):
			print("Input Type: ", arg)
			inputtype = arg
		elif opt in ("-z", "--otype"):
			print("Output Type: ", arg)
			outputtype = arg
		elif opt in ("-x", "--xvalue"):
			print("X: ", arg)
			x = int(arg)
		elif opt in ("-y", "--yvalue"):
			print("Y: ", arg)
			y = int(arg)

	# print(opts)
	if inputtype not in ["bin", "png"]:
		print("Input type should be either png or bin.")
		sys.exit()

	if outputtype not in ["bin", "kml"]:
		print("Output type should be either bin or kml.")
		sys.exit()

	if inputfile == "":
		print("Please provide an input file.")
		sys.exit()

	if outputfile == "":
		print("Please provide an output file name.")
		sys.exit()

	if inputtype == "png":
		try:
			data = get_data_from_image(inputfile)
		except:
			print("Pillow cannot be imported.")
			sys.exit()
	elif inputtype == "bin":
		data = get_data_from_binary(inputfile)


	border = find_watershed(x, y, data)

	if outputtype == "kml":
		save_to_kml(border, outputfile)

	elif outputtype == "bin":
		save_to_bin(border, outputfile)

	t2 = time.time()

	print('Total Elapsed Time: ', str(t2 - t1)[:4], 'sec(s)')
	
if __name__ == '__main__':
	main(sys.argv[1:])


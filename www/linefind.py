import Image
import os
import math
import sys

#thada = math.radians(13.5)    ##Set the degrees from the camera to the laser
thada = 13.5
ctw = 228      ##In mm the distance from the center to the wall
Pw = 248      ## Pixal location of the wall
Pc = 190      ## Pixal location of the center


thelist = []

sithad = math.sin(thada)

magic = (Pw-Pc)/sithad	##this is magic. you can survive anything if
							##magic made it
	

class prcone:
	height = 0
	def calxyz(this, Px, sliceangle, h): 
		mx = ((((Pw-Px)/sithad)*ctw)/magic)-ctw
		if mx > 0:
			return [math.sin(sliceangle)*(-1)*mx,math.cos(sliceangle)*(-1)*mx, (this.height-h)]
		return 0

	def fileproc(this, dirrr ,sliceangle):
		image = Image.open(dirrr)

		rimage = image.split()[0]

		width = image.size[0]
		height = image.size[1]
		imstrm = rimage.getdata()
		top = []
		x=[]
		tval = []
		for h in range(height):
			localmax=0
			localx=0
			for w in range(width):
				currentv = imstrm[(h*width)+w]
				currentx = w
				if currentv > localmax:
					localmax = currentv
					localx = w
			if currentx > 70:
				tval.append(localmax)
				x.append(localx)
				hold = this.calxyz(localx, sliceangle, h)
				if hold:
					top.append(hold)
			else:
				tval.append(0)
				top.append(0)
			

		#print top
		#print tval
		#for t in range(len(top)):
		#	print str(top[t]) + " " + str(x[t]) 
		return top 
		#image.show()

		rimage.show()

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print sys.argv
		print "oh know I need 2 args,  the file path with the images and the file to write"
	else:
		dirrr = os.listdir(sys.argv[1])
		dirrr.sort()
		poplist = []
		for x in range(len(dirrr)):
			print "x is " +str(x)
			if not dirrr[x].endswith(".jpg"):
				print "adding to poplist" + str(x) + " " + dirrr[x]
				poplist.append(x-len(poplist))
		for x in poplist:
			print "x is "+ str(x) + " popping "+ str(dirrr[x])
			dirrr.pop(x)
		f = open(sys.argv[2], 'w')
		
		for files in range(len(dirrr)):
			t = prcone()
			print str(sys.argv[1])
			print str(dirrr[files])

			thelist +=  t.fileproc(str(sys.argv[1])+'/'+str(dirrr[files]), math.radians(files*(3)))

		f.write('o theobject\n')
		
		for x in thelist:
			f.write('v ')
			for y in x:
				f.write(str(y)+" ")
			f.write("\n")

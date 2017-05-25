import mdl
from display import *
from matrix import *
from draw import *

"""======== first_pass( commands, symbols ) ==========

  Checks the commands array for any animation commands
  (frames, basename, vary)
  
  Should set num_frames and basename if the frames 
  or basename commands are present

  If vary is found, but frames is not, the entire
  program should exit.

  If frames is found, but basename is not, set name
  to some default value, and print out a message
  with the name being used.

  jdyrlandweaver
  ==================== """
  

num_frames = 1
basename = ''
anim = False

def first_pass( commands ):
	global num_frames
	global basename
	global anim
	for command in commands:
		if command[0] == "frames":
			num_frames = int(command[1])
		if command[0] == "basename":
			basename = command[1]
		if command[0] == "vary":
			anim = True
	if anim and num_frames == 0:
		print "'vary' used but number of frames not set. Exiting."
		exit()
	if basename == '':
		basename = 'anim'
		print "No base name found. Using 'anim' as default base name."
	second_pass( commands )

"""======== second_pass( commands ) ==========

  In order to set the knobs for animation, we need to keep
  a seaprate value for each knob for each frame. We can do
  this by using an array of dictionaries. Each array index
  will correspond to a frame (eg. knobs[0] would be the first
  frame, knobs[2] would be the 3rd frame and so on).

  Each index should contain a dictionary of knob values, each
  key will be a knob name, and each value will be the knob's
  value for that frame.

  Go through the command array, and when you find vary, go 
  from knobs[0] to knobs[frames-1] and add (or modify) the
  dictionary corresponding to the given knob with the
  appropirate value. 
  ===================="""

knobs = []

def second_pass( commands ):
	global num_frames
	global basename
	global anim
	for frame in range(num_frames):
		knobs.append({})
	for command in commands:
		if command[0] == "vary":
			if int(command[2]) > int(command[3]):
				print "Invalid range: start frame of knob %s is greater than end frame. Exiting."%command[1]
			if int(command[3]) > num_frames:
				print "Invalid range: end frame of knob %s is greater than number of frames. Exiting."%command[1]
			if int(command[2]) < 0 or int(command[3]) < 0:
				print "Invalid range: frames of knob %s cannot be negative. Exiting."%command[1]
			for frame in range(num_frames):
				if int(command[4]) < int(command[5]):
					current = int(command[4])
					increment = (float(command[5])-float(command[4]))/(float(command[3])-float(command[2]))
					knobs[frame][command[1]] = current
					current += increment
				else:
					current = int(command[5])
					increment = (float(command[5])-float(command[4]))/(float(command[3])-float(command[2]))
					knobs[frame][command[1]] = current
					current += increment

def run(filename):
	global num_frames
	global basename
	global anim
	"""
	This function runs an mdl script
	"""
	color = [255, 255, 255]
	tmp = new_matrix()
	ident( tmp )

	p = mdl.parseFile(filename)

	if p:
		(commands, symbols) = p
	else:
		print "Parsing failed."
		return

	ident(tmp)
	stack = [ [x[:] for x in tmp] ]
	screen = new_screen()
	tmp = []
	step = 0.1
	first_pass(commands)
	print num_frames
	for frame in range(num_frames):
		if frame < 10:
			file = 'anim/' + basename + '00' + str(frame) + '.png'
		elif frame < 100:
			file = 'anim/' + basename + '0' + str(frame) + '.png'
		else:
			file = 'anim/' + basename + '00' + str(frame) + '.png'
		for command in commands:
			print command
			c = command[0]
			args = command[1:]
			if c == 'box':
				if str(args[-1]) == args[-1]:
					new_args = []
					for i in range(len(args)-1):
						if type(args[i]) is int or type(args[i]) is float:
							new_args.append(args[i] * float(knobs[frame][args[-1]]))
						else:
							new_args.append(args[i])
				else:
					new_args = args
				add_box(tmp,
						new_args[0], new_args[1], new_args[2],
						new_args[3], new_args[4], new_args[5])
				matrix_mult( stack[-1], tmp )
				draw_polygons(tmp, screen, color)
				tmp = []
			elif c == 'sphere':
				if str(args[-1]) == args[-1]:
					new_args = []
					for i in range(len(args)-1):
						if type(args[i]) is int or type(args[i]) is float:
							new_args.append(args[i] * float(knobs[frame][args[-1]]))
						else:
							new_args.append(args[i])
				else:
					new_args = args
				add_sphere(tmp,
						   new_args[0], new_args[1], new_args[2], new_args[3], step)
				matrix_mult( stack[-1], tmp )
				draw_polygons(tmp, screen, color)
				tmp = []
			elif c == 'torus':
				if str(args[-1]) == args[-1]:
					new_args = []
					for i in range(len(args)-1):
						if type(args[i]) is int or type(args[i]) is float:
							new_args.append(args[i] * float(knobs[frame][args[-1]]))
						else:
							new_args.append(args[i])
				else:
					new_args = args
				add_torus(tmp,
						  new_args[0], new_args[1], new_args[2], new_args[3], new_args[4], step)
				matrix_mult( stack[-1], tmp )
				draw_polygons(tmp, screen, color)
				tmp = []
			elif c == 'move':
				if str(args[-1]) == args[-1]:
					new_args = []
					for i in range(len(args)-1):
						if type(args[i]) is int or type(args[i]) is float:
							new_args.append(args[i] * float(knobs[frame][args[-1]]))
						else:
							new_args.append(args[i])
				else:
					new_args = args
				tmp = make_translate(new_args[0], new_args[1], new_args[2])
				matrix_mult(stack[-1], tmp)
				stack[-1] = [x[:] for x in tmp]
				tmp = []
			elif c == 'scale':
				if str(args[-1]) == args[-1]:
					new_args = []
					for i in range(len(args)-1):
						if type(args[i]) is int or type(args[i]) is float:
							new_args.append(args[i] * float(knobs[frame][args[-1]]))
						else:
							new_args.append(args[i])
				else:
					new_args = args
				tmp = make_scale(new_args[0], new_args[1], new_args[2])
				matrix_mult(stack[-1], tmp)
				stack[-1] = [x[:] for x in tmp]
				tmp = []
			elif c == 'rotate':
				if str(args[-1]) == args[-1]:
					new_args = []
					for i in range(len(args)-1):
						if type(args[i]) is int or type(args[i]) is float:
							new_args.append(args[i] * float(knobs[frame][args[-1]]))
						else:
							new_args.append(args[i])
				else:
					new_args = args
				theta = new_args[1] * (math.pi/180)
				if new_args[0] == 'x':
					tmp = make_rotX(theta)
				elif new_args[0] == 'y':
					tmp = make_rotY(theta)
				else:
					tmp = make_rotZ(theta)
				matrix_mult( stack[-1], tmp )
				stack[-1] = [ x[:] for x in tmp]
				tmp = []
			elif c == 'push':
				stack.append([x[:] for x in stack[-1]] )
			elif c == 'pop':
				stack.pop()
			if not anim:
				if c == 'display':
					display(screen)
				if c == 'save':
					save_extension(screen, args[0])
		if anim:
			save_extension(screen, file)
	if anim:
		make_animation(basename)

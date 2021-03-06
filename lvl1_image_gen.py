#!/usr/bin/env python

import os
import numpy as np
import sys
import argparse
from pyhdf.SD import *
#from colour import Color
from PIL import Image

fill_val = 65515
widths = [128,512]
heights = [512,2048]

#This is the offset scale factor used when the resolution scaling is needed
offset_scale_factor = [1,4]

offset = 		[0.0,	0.0,	16.0,	0.0,	16.0,	#1
				 0.0,	0.0,	0.0,	16.0,	0.0,	#2
				 0.0,	0.0,	0.0,	16.0,	0.0,	#3
				 0.0,	0.0,	0.0,	0.0,	0.0,	#4
				 0.0,	0.0,	0.0,	0.0,	0.0,	#5
				 0.0,	0.0,	-16.0,	0.0,	0.0,	#6
				 0.0,	-16.0,	0.0,	0.0,	-16.0,	#7
				 0.0,	0.0,	-16.0,	0.0,	-16.0,	#8
				 0.0,	-16.0,	0.0,	-16.0,	-16.0,	#9
				 0.0,	-16.0,	0.0,	-16.0,	-16.0,	#10
				 0.0,	-16.0,	-16.0,	-16.0,	0.0,	#11
				 -16.0,	-16.0,	-16.0,	-16.0,	0.0,	#12
				 -16.0,	-16.0,	-16.0,	-16.0,	-16.0,	#13
				 -16.0,	-16.0,	-16.0,	-16.0,	-16.0,	#14
				 -16.0,	-16.0,	-16.0,	-16.0,	-16.0,	#15
				 -16.0,	-16.0,	-16.0,	-16.0,	-16.0, 	#16
				 -16.0,	-16.0,	-16.0,	-16.0,	-16.0,	#17
				 -32.0,	-16.0,	-16.0,	-16.0,	-16.0,	#18
				 -16.0,	-16.0,	-16.0,	-16.0,	-16.0,	#19
				 -16.0,	-32.0,	-16.0,	-16.0,	-16.0,	#20
				 -16.0,	-16.0,	-16.0,	-16.0,	-16.0,	
				 -16.0,	-16.0,	-16.0,	-16.0,	-16.0,	
				 -16.0,	-16.0,	-16.0,	-16.0,	-16.0,	
				 -16.0,	-16.0,	-16.0,	-16.0,	-16.0,	
				 0.0,	-16.0,	-16.0,	-16.0,	-16.0,
				 -16.0,	0.0,	-16.0,	-16.0,	-16.0,
				 0.0,	-16.0,	-16.0,	0.0,	-16.0,
				 0.0,	-16.0,	-16.0,	0.0,	-16.0,
				 0.0,	-16.0,	0.0,	0.0,	-16.0,
				 0.0,	-16.0,	0.0,	0.0,	-16.0,
				 0.0,	0.0,	0.0,	0.0,	-16.0,
				 0.0,	0.0,	0.0,	0.0,	0.0,
				 0.0,	0.0,	0.0,	0.0,	0.0,
				 0.0,	0.0,	0.0,	0.0,	0.0,
				 0.0,	0.0,	16.0,	0.0,	0.0,
				 16.0,	0.0,	0.0,	16.0,	0.0]

offset = map(int,offset)

# This makes images for a certain color bandwidth given the block data,
# height and width and color : 0 = red, 1 = green , 2 = blue
def color_channel_img_gen(block, block_width, block_height, clr):
 
 	# Generate a new image with the block width and height
	img = Image.new('RGB',(block_width,block_height))

	# Flatten the numpy array so that it is one dimensional
	block = block.ravel()

	# Reshape the numpy array to be in the same form of pixels in which it is row major.
	# Then flatten again back to a 1-dimensional array
	block = block.reshape(block_height,block_width,order='F').ravel()

	#Convert the radiance value to a rgb value scale by dividing it by the maximum number and multipying with 256
	block = np.int_((np.float_(np.float_(block)/40896))*256)

	#Create a list with block_width*block_height zeroes
	other = [0]*len(block)

	# Zip will sort the block values such that each tuple will have (block[0],0,0) and (block[1],0,0) etc (red in this case)
	if clr is 0: pixels = zip(block,other,other)
	elif clr is 1: pixels = zip(other,block,other)
	elif clr is 2: pixels = zip(other,other,block)

	# Place the pixel list of tuples into img
	img.putdata(pixels)
	return img

# This will set cropping offsets to fit the largest rectangle box around the block image that does not contain any fill values
def set_crop_offsets(block, block_width, block_height):

	top_left = 0
	top_right = 0
	bottom_left = block_height - 1
	bottom_right = block_height - 1
	mid = int(block_height/2)

	avg_left = 0
	avg_right = 0
	avg1_left = 0
	avg1_right = 0
	r = block_width - 1
	for j in range(block_height):

			# The top left and right side are averaged out with every 4 blocks before them
			if (j > 3 and j < mid): 
				avg_left = (int(block[0][j-4]) + int(block[0][j-3]) + int(block[0][j-2]) + int(block[0][j-1]) + int(block[0][j]))/5
				avg_right = (int(block[r][j-4]) + int(block[r][j-3]) + int(block[r][j-2]) + int(block[r][j-1]) + int(block[r][j]))/5

			# The bottom left and right side are averaged out with every 4 blocks after them
			if (j < (block_height - 5) and j > mid):
					avg1_left = (int(block[0][j]) + int(block[0][j+1]) + int(block[0][j+2]) + int(block[0][j+3]) + int(block[0][j+4]))/5
					avg1_right = (int(block[r][j]) + int(block[r][j+1]) + int(block[r][j+2]) + int(block[r][j+3]) + int(block[r][j+4]))/5

			# Once the top corners averages are computed, if they produce a fill value and the current block is fill, take the block after the last fill_value
			if (avg_left == fill_val) and (j < mid) and (block[0][j] == fill_val): top_left = j + 1
			if (avg_right == fill_val) and (j < mid) and (block[r][j] == fill_val): top_right = j + 1

			# Same case with top corners but the block before the current block is extracted instead
			if (avg1_left == fill_val) and (j > mid) and (j < bottom_left) and (block[0][j] == fill_val): bottom_left = j - 1
			if (avg1_right == fill_val) and (j > mid) and (j < bottom_right) and (block[r][j] == fill_val): bottom_right = j - 1

	# The top part is cropped to the maximum of the two values, and the bottom part is cropped to the minimum for the two values
	return (max(top_left, top_right),min(bottom_left, bottom_right))

	
def main():

	#Flags:
	block_min = 0
	block_max = 0
	block_setting = 0
	crop = 0

	# Set up input arguments
	parser = argparse.ArgumentParser(description='This will take in either MISR level 1 image file and generate an images depending upon input arguments')
	parser.add_argument('-b', '--block',default=0,required=True,help='Starting block number')
	parser.add_argument('-b_m', '--block_end',default=-1,help='Ending block number for block ranges')
	parser.add_argument('-i','--input',required=True,help='Input hdf file name')
	parser.add_argument('-o','--output',required=True,help='Output image file name')

	parser.add_argument('-c','--crop',action='store_true',help='Add flag if cropped image is desired')
	parser.add_argument('-R','--high_res',action='store_true',help='Add flag if want highest resolution possible if available')
	args = parser.parse_args()

	#block_min indicates either the single block or the start of the range of blocks
	block_min = int(args.block)

	# If the crop flag was included, set crop to 1
	crop = 1 if args.crop == True else 0 

	# If the second block number was also part of the arguments, assign it to block max. If not, set to block_min
	block_max = int(args.block_end) if args.block_end != -1 else block_min

	# Check for out of bounds of 0 and 179
	if block_min < 0: block_min = 0
	if block_max > 179: block_max = 179

	# Ensure that block min does not exceed block_max
	if block_min > block_max: sys.exit("Last block must not be smaller than starting block")

	# Crop cannot be set when a block range is chosen
	if crop == 1 and block_max != block_min:
		sys.exit("Block ranges cannot be cropped")

	# If block_min equals to block max, it means that only a block image is generated
	if block_min == block_max: block_setting = 0
	else: block_setting = 1
	
	#Obtaining file name
	hdf_file_name = args.input
	image_file_name = args.output
	
	if(hdf_file_name.find('.hdf') == -1):sys.exit("Please choose a proper hdf file as input")

	hdf = SD(hdf_file_name)

	#Make dataset list or red, blue, green colors
	color_band_ds = [hdf.select('Red Radiance/RDQI'),hdf.select('Green Radiance/RDQI'),hdf.select('Blue Radiance/RDQI')]


	# If resolution flag is set to 1 and the highest resolution is 512*2048, set res to 1
	res = 1 if (args.high_res == True and len(color_band_ds[1][1]) == 512)  else 0

	# b_w and b_h = 128*512 if res  = 0, 512*2048 if otherwise
	b_w = widths[res]
	b_h =heights[res]
	offset_scale = offset_scale_factor[res]

	#Calculate total blocks
	total_blocks = (block_max - block_min) + 1
	
	#Get maximum offsets in both directions
	max_coor = 0
	min_coor = 0
	calc = 0
	for i in range (block_min, block_max+1):
		calc += offset[i]

		#Find most possible offset
		if(calc > max_coor): max_coor = calc

		#Find most minimum offset
		if(calc < min_coor): min_coor = calc


	print "\nMax Y: " + str(offset_scale*max_coor)
	print "Min Y: " + str(offset_scale*min_coor)

	#Make absolute value minimum offset at the top (so essentially top->bottom : left ->right)
	prev_offset = abs(min_coor)

	#Make a new background image with width being the total width of all possible blocks and height summed up with offsets in both direction
	background = Image.new('RGB', (b_w*total_blocks, b_h+offset_scale*(abs(min_coor) + max_coor)), (0,0,0))
	
	#red block
	red_current_block = color_band_ds[0]
	red_block_width = len(red_current_block[0])
	red_block_height = len(red_current_block[0][0])

	#green block
	green_current_block = color_band_ds[1]
	green_block_width = len(green_current_block[0])
	green_block_height = len(green_current_block[0][0])

	#blue block
	blue_current_block = color_band_ds[2]
	blue_block_width = len(blue_current_block[0])
	blue_block_height = len(green_current_block[0][0])

	print "\nLoading image..."

	# Create each image and paste onto the background
	for idx,blk in enumerate(range(block_min, block_max + 1)):


		# Set up red, green, blue 2d arrays with fill_val replaced by black
		# Set up blocks as numpy arrays
		red_block = red_current_block[blk,:,:]

		# Set up the blocks such that all the fill values are zeroed out
		red_block[red_block == fill_val] = 0
		green_block = green_current_block[blk,:,:]
		green_block[green_block == fill_val] = 0
		blue_block = blue_current_block[blk,:,:]
		blue_block[blue_block == fill_val] = 0

		
		if(crop == 1):

			# Call the function to obtain top and bottom crop offset
			offset_tuple = set_crop_offsets(blue_block, blue_block_width, blue_block_height)
			offset_top = offset_tuple[0]
			offset_bottom = offset_tuple[1]

			#In the case if the image resolution is smaller than the block resolution
			if(b_w < blue_block_width):

				# Divide by the factor of block res/image res
				offset_top = offset_top/4
				offset_bottom = offset_bottom/4
		

		# Create the real image of the current block with the intended dimensions
		real_img = Image.new('RGB',(b_w,b_h))

		# If there are discrepancies between resolution in the blocks (occurs in some hdf files)
		# What happens here is that each block color channel are generated as separate images, resized to the same size and combined later
		if(red_block_width != green_block_width  or red_block_width != blue_block_width or green_block_width != blue_block_width):
			red_img = color_channel_img_gen(red_block, red_block_width, red_block_height, 0)
			green_img = color_channel_img_gen(green_block, green_block_width, green_block_height, 1)
			blue_img = color_channel_img_gen(blue_block, blue_block_width, blue_block_height, 2)
			
			# All images are resized to the correct size
			if(b_w < max(red_block_width,green_block_width, blue_block_width)):
				if(red_block_width == 512):
					red_img = red_img.resize((b_w,b_h),1)
				if(green_block_width == 512):
					green_img = green_img.resize((b_w,b_h),1)
				if(blue_block_width == 512):
					blue_img = blue_img.resize((b_w,b_h),1)

			# The array of tuples for each image are loaded back into three separate arrays
			red_p = red_img.load()
			green_p = green_img.load()
			blue_p = blue_img.load()

			# Set up the pixel array with the values in the appropiate places for the real image
			pixel = [(0,0,0)]*(b_w*b_h)
			for i in range(b_w):
				for j in range(b_h):
					pixel[j*b_w + i] = (red_p[i,j][0], green_p[i,j][1], blue_p[i,j][2])

			real_img.putdata(pixel)


		# When all the channel blocks are the same resolution
		else:
			
			# Convert all the blocks to a 1-dimensional array
			red_block = red_block.ravel()
			green_block = green_block.ravel()
			blue_block = blue_block.ravel()

			# Convert arrays to rgb value format and reshape arrays to be row major
			red_block = np.int_((np.float_(np.float_(red_block)/40896))*256)
			red_p = red_block.reshape(red_block_height,red_block_width,order='F').ravel()

			green_block = np.int_((np.float_(np.float_(green_block)/40896))*256)
			green_p = green_block.reshape(green_block_height,green_block_width, order='F').ravel()

			blue_block = np.int_((np.float_(np.float_(blue_block)/40896))*256)
			blue_p = blue_block.reshape(blue_block_height,blue_block_width, order='F').ravel()
		
			# Pack red, green and blue rgb values into one pixel array that contains tuples
			pixel = zip(red_p, green_p, blue_p)
			real_img = Image.new('RGB',(red_block_width,red_block_height))
			real_img.putdata(pixel)
			real_img = real_img.resize((b_w,b_h),1)

		# If block range is not desired
		if block_setting == 0:

			# Generate cropped image
			if crop == 1: real_img = real_img.crop((0,offset_top,b_w,offset_bottom))
			real_img = real_img.transpose(Image.FLIP_TOP_BOTTOM)
			real_img.save(image_file_name)
			real_img.show()
			print "\nSaved image inside " + image_file_name


		#Stitch image onto correct offset in background
		elif block_setting == 1:
			print "Real Offset " + str(blk) + " idx " + str(idx) + ' : ' + str(offset[blk]*offset_scale)
			real_offset = (idx*b_w, offset_scale*(prev_offset + offset[blk]))
			prev_offset = prev_offset + offset[blk]
			background.paste(real_img, real_offset)
	
	#Flip horizontal to get correct orientation
	if block_setting == 1:
		background = background.transpose(Image.FLIP_TOP_BOTTOM)
		background.save(image_file_name)
		background.show()
		print "\nSaved image inside " + image_file_name


if __name__ == '__main__':
	main()

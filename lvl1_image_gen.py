#!/usr/bin/env python
# Property of Atiqah Hamzah

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import sys
from pyhdf.SD import *
from colour import Color
from PIL import Image

fill_val = 65515
widths = [128,512]
heights = [512,2048]
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

def color_channel_img_gen(block, block_width, block_height, clr):

	img = Image.new('RGB',(block_width,block_height))
	pixels = [(0,0,0)]*(block_width*block_height)
	for i in range(block_width):
			for j in range(block_height):
				if i == 0: tup = (int(block[i][j]*256/40896),0,0)
				if i == 1: tup = (0,int(block[i][j]*256/40896),0)
				if i == 2: tup = (0,0,int(block[i][j]*256/40896))
				pixels[j*block_width + i] = tup
	img.putdata(pixels)
	return img

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
			if (j > 3 and j < mid): 
				avg_left = (int(block[0][j-4]) + int(block[0][j-3]) + int(block[0][j-2]) + int(block[0][j-1]) + int(block[0][j]))/5
				avg_right = (int(block[r][j-4]) + int(block[r][j-3]) + int(block[r][j-2]) + int(block[r][j-1]) + int(block[r][j]))/5

			if (j < (block_height - 5) and j > mid):
					avg1_left = (int(block[0][j]) + int(block[0][j+1]) + int(block[0][j+2]) + int(block[0][j+3]) + int(block[0][j+4]))/5
					avg1_right = (int(block[r][j]) + int(block[r][j+1]) + int(block[r][j+2]) + int(block[r][j+3]) + int(block[r][j+4]))/5

			if (avg_left == fill_val) and (j < mid) and (block[0][j] == fill_val): top_left = j + 1
			if (avg_right == fill_val) and (j < mid) and (block[r][j] == fill_val): top_right = j + 1
			if (avg1_left == fill_val) and (j > mid) and (j < bottom_left) and (block[0][j] == fill_val): bottom_left = j - 1
			if (avg1_right == fill_val) and (j > mid) and (j < bottom_right) and (block[r][j] == fill_val): bottom_right = j - 1
	return (max(top_left, top_right),min(bottom_left, bottom_right))

	
def main():

	if (len(sys.argv) < 2):
		print "error: need input file"
		sys.exit(1)

	if (len(sys.argv) < 3):
		print "error: need output file"
		sys.exit(1)

	#Obtaining file name
	hdf_file_name = sys.argv[1]
	image_file_name = sys.argv[2]

	#Obtaining the hdf datasets
	hdf = SD(hdf_file_name)

	#Make dataset list or red, blue, green colors
	color_band_ds = [hdf.select('Red Radiance/RDQI'),hdf.select('Green Radiance/RDQI'),hdf.select('Blue Radiance/RDQI')]

	block_min = -1
	block_max = 180
	print '\n'

	block_setting = 0
	crop = 0

	#Obtain block range
	while True:
		print "Please input setting: 0: One block image or 1: Block range image"
		block_setting = int(sys.stdin.readline())
		if block_setting < 0 and block_setting > 1: print "Input correct setting number\n"
		else: break

	if block_setting == 0:
		while True:
			print "Cropped or not cropped? 0: No 1: Yes"
			crop = int(sys.stdin.readline())
			if(crop >= 0 and crop < 2):
				break
			print "Input correct crop choice\n"
		while(block_min < 0 or block_min > 179):
			print "\nPlease put in block number"
			block_min = int(sys.stdin.readline())
			block_max = block_min
			if(block_min < 0 or block_min > 179):
				print "Error: please input correct block number"

	while True and block_setting == 1:
		
		while(block_min < 0):
			print "\nPlease put in block range minimum value"
			block_min = int(sys.stdin.readline())
			if(block_min < 0 or block_min > 179):
				print "Error: please input correct block range minimum value"

		while(block_max > 179):
			print "\nPlease put in block range maximum value"
			block_max = int(sys.stdin.readline())
			if(block_max < 0 or block_max > 179):
				print "Error: please input correct block range maximum value"

		if(block_min <= block_max): break
		else:
			block_min = -1
			block_max = 180

	b_w = 128
	b_h = 512
	offset_scale = 1

	if len(color_band_ds[1][1]) == 512:
		while True:
			print "\nPlease choose resolution by typing the number: 0: 128x512 or 1: 512x2048"
			res = int(sys.stdin.readline())
			if(res > 1 or res < 0): print "Error: Wrong resolution input. Please type again\n"
			else: 
				b_w = widths[res]
				b_h = heights[res]
				offset_scale = offset_scale_factor[res]
				break

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

	#Create each black and paste onto the background
	for idx,blk in enumerate(range(block_min, block_max + 1)):


		#Set up red, green, blue 2d arrays with fill_val replaced by black
		red_block = red_current_block[blk,:,:]
		red_block[red_block == fill_val] = 0
		green_block = green_current_block[blk,:,:]
		green_block[green_block == fill_val] = 0

		blue_block = blue_current_block[blk,:,:]

		if(crop == 1):

			offset_tuple = set_crop_offsets(blue_block, blue_block_width, blue_block_height)
			offset_top = offset_tuple[0]
			offset_bottom = offset_tuple[1]

			if(b_w < blue_block_width):
				offset_top = offset_top/4
				offset_bottom = offset_bottom/4
		
		blue_block[blue_block == fill_val] = 0
		
		#Set up images for all three colors and their pixel arrays
		red_img = Image.new('RGB',(red_block_width,red_block_height))
		green_img = Image.new('RGB',(green_block_width,green_block_height))
		blue_img = Image.new('RGB',(blue_block_width,blue_block_height))
		red_p = [(0,0,0)]*(red_block_width*red_block_height)
		green_p = [(0,0,0)]*(green_block_width*green_block_height)
		blue_p = [(0,0,0)]*(blue_block_width*blue_block_height)

		# Create true size red pixel array
		for i in range(0,red_block_width):
			for j in range(0,red_block_height):
				red_p[j*red_block_width + i] = (int(red_block[i][j]*256/40896),0,0)

		#Put pixel rgb array onto red image
		red_img.putdata(red_p)

		# Create true size green pixel array
		for i in range(0,green_block_width):
			for j in range(0,green_block_height):
				green_p[j*green_block_width + i] = (0,int(green_block[i][j]*256/40896),0)
				
		#Put pixel rgb array onto green image
		green_img.putdata(green_p)

		#Put pixel rgb array onto blue image
		for i in range(0,blue_block_width):
			for j in range(0,blue_block_height):
				blue_p[j*blue_block_width + i] = (0,0,int(blue_block[i][j]*256/40896))

		#Put pixel rgb array onto blue image
		blue_img.putdata(blue_p)

		#If any off images are the biggest resolution, reduce resolution to that of 128*512 if there is an option
		if(b_w < max(red_block_width,green_block_width, blue_block_width)):
			if(red_block_width == 512):
				red_img = red_img.resize((b_w,b_h),1)
				red_p = red_img.load()
			if(green_block_width == 512):
				green_img = green_img.resize((b_w,b_h),1)
				green_p = green_img.load()
			if(blue_block_width == 512):
				blue_img = blue_img.resize((b_w,b_h),1)
				blue_p = blue_img.load()


		#Reload pixel arrays just in case of resize to avoid type conflicts
		red_p = red_img.load()
		green_p = green_img.load()
		blue_p = blue_img.load()

		#Make true color image of block by combining red, green, blue values into tuple
		real_img = Image.new('RGB',(b_w,b_h))
		pixel = [(0,0,0)]*(b_w*b_h)
		for i in range(b_w):
			for j in range(b_h):
				red = (red_p[i,j])[0]
				green = (green_p[i,j])[1]
				blue = (blue_p[i,j])[2]
				pixel[j*b_w + i] = (red,green,blue)

		real_img.putdata(pixel)

		if block_setting == 0:
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

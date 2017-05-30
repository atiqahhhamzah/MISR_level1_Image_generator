# MISR_level1_Image_generator

<b>Introduction</b>
<p>
This is a pretty simple image generator that will generate any image for any level 1 MISR hdf file regardless of resolution (since it'll check for that). This is written for hdf4 files and uses the pyhdf API which you can get from the hdfeos website.
I've listed which python libraries I am using under libraries and you can just install those libraries using pip or conda if you don't have them and it should work. It's a little slow if you stitch many images together and does take a lot of computing resources, so take heed of that.
</p>
<b>Operation</b>
<p>
Run "python lvl1_image_gen.py MISR_HDF_Filename.hdf image_name.jpeg"

There will be a bunch of setting options, so some files will have a max resolution of 512x2048 whereas some other files will have an even more scaled down resolution (usually these are the are the non-nadir camera files). You can choose which image size you want depending upon what is available (if only one option is available, it will be that size by default and won't prompt you for it). Other settings include whether you want a single block image or the block range you want and if the latter option is chosen, the blocks will be stitched together following the relative offsets. If there are any problems with the stitching of block images, please inform me asap. The cropping option for single block images will automatically take the largest rectangular image size that does not contain any fill values.
</p>

<b>Libraries</b>
<p>PIL<br>pyhdf<br>numpy<br>colour</p>



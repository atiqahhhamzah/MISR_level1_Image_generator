# MISR_level1_Image_generator

<b>Introduction</b>
<p>
This is a pretty simple image generator that will generate any image for any level 1 MISR. This is written for hdf4 files and uses the pyhdf API which you can get from the hdfeos website. I've listed which python libraries I am using under libraries and you can just install those libraries using pip or conda if you don't have them and it should work. It's a little slow if you stitch many images together and does take a lot of computing resources, so take heed of that. Naming convention isn't great and neither is the code super clean and neat as of now but I will try to fix that as I go
</p>
<b>Operation</b>
<p>
Run "python lvl1_image_gen.py MISR_HDF_Filename.hdf image_name.jpeg"

Do not name your image files that and replace image_name with anything else. I think if you decide to change it to a png format it should also not be problematic (Although I haven't tested that out yet)

These are the setting options:
<ol>
<li><em>Block setting</em></li>
  <p>There are two options, single block image or block range. The offsets and block stitching is handled for you so the image produced should not have any weird defects (If there are, please tell me asap).</p>
  <ul>
  <li>Cropped</li>
    <p>This will crop the image to the largest possible rectangular part of the image in which the none of the pixels contain fill values.</p>
    <li>Uncropped</li>
    <p>This will leave the images in their original size.</p>
    </ul>
 <li><em>Block number or block min and max</em></li>
 <p>This is either the block or block range you wish to have an image of.</p>
 <li><em>Resolution</em></li>
 <p>This option is only available if the blocks were at a 512x2048 size (usually only the nadir camera angle contains this resolution). You can either leave it at that resolution or scale it down to 128x512.</p>
 
 </ol>
 
</p>

<b>Python Libraries</b>
<p>PIL<br>pyhdf<br>numpy<br>colour</p>



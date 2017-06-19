# MISR_level1_Image_generator

<b>Introduction</b>
<p>
This is a pretty simple image generator that will generate any image for any level 1 MISR. This is written for hdf4 files and uses the pyhdf API which you can get from the hdfeos website. I've listed which python libraries I am using under libraries and you can just install those libraries using pip or conda if you don't have them and it should work. It's a little slow if you stitch many images together and does take a lot of computing resources, so take heed of that. Naming convention isn't great and neither is the code super clean and neat as of now but I will try to fix that as I go
</p>
<b>Operation</b>
<p>
Run "python lvl1_image_gen.py -h"
This well tell you about all the new input arguments and flags that you will need to have to produce the image.
</p>

<b>Python Libraries</b>
<p>PIL<br>pyhdf<br>numpy<br>colour</p>



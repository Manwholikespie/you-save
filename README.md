# YouSave

###An ingenious new storage system.

Buddha once said, *"Unity can only be manifested by the Binary. Unity itself and the idea of Unity are already two."* Want to know the reason he's dead? Because natural selection doesn't favor those who believe ones and zeroes are the best way to compress data. No... You see, why write:  
`01100010 01110101 01100100`  
`01100100 01101000 01100001`  
`00100000 01101001 01110011`  
`00100000 01100100 01100101`  
`01100001 01100100 00001010`  

When you can just as easily write:  
`62756464686120697320646561640a`  

This is what this project aimed to highlight. You see, space is precious and valuable. Or, at least it is when it comes to space for storing data. Luckily, we have large corporations making enough money off of our personal information to pay for large data centers. But wait, we can **only store videos** on these servers? Well, looks like we will have to convert our files to video. But wait, they **compress** the videos we upload? That would mean that precious data would get lost! Well, we can't have that. What's the solution? When does this terribly written introduction with all of its rhetorical questions end? Now.

###Introducing YouSave...

Take a file, let's say it is a folder of music. Compress it into a zip, tar, whatever you like. Then, feed it to YouSave.

**Here's a rundown of what happens to the file:**

The file is taken, its binary (in the glorious hexadecimal form) is read (courtesy of xxd), and outputted to a large document (in the end, it's about twice the size as the original document).

Then, this document is split up into sections of 48 lines per section (2880 characters), and fed into qrencode, where multiple QR codes are made and saved.

At this point in the development of the project, these codes are not yet positioned into a video for upload, however that doesn't mean we can't talk about the decoding process.

Next, once the QR codes have been made (remember they haven't been fixed into a video yet), you have the option to decode them and get your file back. To do this, zbarimg scans all of the QR codes in the order you made them, and the output is printed back to another large document. Then, xxd's handy rebuild option is employed to reconstruct the binary package– your original compressed archive.

##The end.

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

With YouSave, you can store all of your personal files in video. Just give the program a file archive (.zip, .tar, .gz, etc.) and let us do the rest.

Disclaimer: at this point in time, all it can do is store it in QR codes.

###Instructions
Open up your favorite Terminal, and make a folder.  
`mkdir folder`  

Then, place your file inside it (make sure its name is file.zip).  
`cp file.zip folder`  

Now, launch with python (2.7.10).  
`cd folder; python yousave.py`  

At the launch screen, choose  
`[1] Encode a file.`   

Let it run, and then you're done! If you want to decode the images later, launch the same program, and choose:  
`[2] Decode a file.`


# coding: utf-8

# In[56]:

import Tkinter
import subprocess 
import os


root = Tkinter.Tk()

root.title('ProSnip')
root.geometry('{}x{}'.format(444, 444))

def callback():
    root.destroy()
    os.system('python snpt.py')
    
    


title = Tkinter.Label(root, text="SNP annotation tool", font=("Arial", 16))
title.pack()

blank = Tkinter.Label(root, text="", font=("Arial", 16))
blank.pack()

name = Tkinter.Label(root, text="ProSnip", font=("Arial", 48, 'bold italic underline'))
name.pack()

blank1 = Tkinter.Label(root, text="", font=("Arial", 30))
blank1.pack()


start_bt = Tkinter.Button(root, text="START", command=callback,font=("Arial", 14))
start_bt.pack()

blank2 = Tkinter.Label(root, text="", font=("Arial", 72))
blank2.pack()

title = Tkinter.Label(root, text="Developed by\nBiomedical Informatics Center,\n ICMR-National Institute of Traditional Medicine,\nBelagavi, Karnataka, India", font=("Arial", 14))
title.pack()



root.mainloop()


# In[ ]:




# In[ ]:




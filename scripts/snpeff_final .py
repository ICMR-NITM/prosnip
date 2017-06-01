from Tkinter import *
import pandas as pd
import numpy as np
import os
from subprocess import *
import subprocess, shlex
search_db_root = Tk()


label1 = Label( search_db_root, text="Enter of Reference Database")
search_term = Entry(search_db_root, bd =5)

def getRefdb():
    print search_term.get()
    os.system('java -jar snpEff.jar databases | grep -i '+search_term.get()+' > snpeff.csv')
    search_db_root.destroy()


submit = Button(search_db_root, text ="SUBMIT", command = getRefdb)

label1.pack()
search_term.pack()

submit.pack(side =BOTTOM) 
search_db_root.mainloop()
sneff_choices = pd.read_csv('snpeff.csv', delimiter='\t', usecols=[1], header = None)
choices = np.array(sneff_choices)

gca_choices = pd.read_csv('snpeff.csv', delimiter='\t', usecols=[0],header = None)
gca_choices = np.array(gca_choices)


all_choices = []
for choice in choices:
    choice = choice[0].replace(" ","")
    all_choices.append(choice)
print all_choices
sneff_downloads = pd.read_csv('snpeff.csv', delimiter='\t', usecols=[4],header = None)
downloads = np.array(sneff_downloads)
all_downloads = []
for download in downloads:
    all_downloads.append(download[0])
    

def select_sneff():
    selected =  var.get()
    search_index = all_choices.index(selected)
    print selected
    downloadsneff = all_downloads[search_index]
    gca_id = gca_choices[search_index]
    print downloadsneff
    command = ''
    command+= ('java -Djava.net.useSystemProxies=true -jar snpEff.jar '+ gca_id +' filtered_snps_final.vcf > filtered_snps_final.ann.vcf')
    #print command 
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    proc = subprocess.Popen('firefox snpEff_summary.html', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
   # os.system('wget '+downloadsneff)
    
    sneff_root.destroy()
    
    
sneff_root = Tk()
sneff_root.title('Select choice to download SnpEFF Data')

var  = StringVar(sneff_root)
var.set(all_choices[0])
choices  = all_choices
option = OptionMenu(sneff_root, var, *choices)
option.pack( side='top', padx =10, pady=10)
sneff_button = Button(sneff_root, text="SUBMIT", command=select_sneff)
sneff_button.pack(side='left', padx=20,pady=10)
sneff_root.mainloop()







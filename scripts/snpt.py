
# coding: utf-8

# In[3]:

import Tkinter
import tkMessageBox
from tkFileDialog import askopenfilename
import os
from subprocess import *
import subprocess, shlex
import ttk

root = Tkinter.Tk()
root.title('SNP')
root.geometry('{}x{}'.format(444, 444))

progbarval = 0

ddup_bam_path = ''
parent_dir = ''
ref_path = ''
sra_path = ''

def index_reference(filename):
    progbarlabel.config(text = "indexing reference file..")
    command = 'bwa index '+filename
    print "Index Refernce..... "
    print command
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed indexing reference file..")
    print err
    print out
    print "Done Index Refernce "
    #4
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval

def sort_reference(filename):
    command = 'samtools faidx '+filename
    print "Sorting the refernce...."
    print command
    progbarlabel.config(text = "Sorting reference file..")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    print err
    print out
    print "Done sorting the reference"
    progbarlabel.config(text = "Completed Sorting reference file..")
    #5
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
def create_dict(filename):
    print "Creating sequence dictionary"
    command = ''
    command+='picard-tools CreateSequenceDictionary '
    command+=('REFERENCE='+filename+ ' ')
    dict_filename = filename
    dict_filename = dict_filename.replace('.fasta','.dict')
    dict_filename = dict_filename.replace('.fa','.dict')
    command+=('OUTPUT='+dict_filename)
    print command
    progbarlabel.config(text = "Creating sequence dictionary...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed creating sequence dictionary...")
    print err
    print out
    print "Done creating sequence dictionary"
    #6
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval

def align_create_sam(reference, fastq_files):
    print reference
    print fastq_files
    progbarlabel.config(text = "Creating .sam file...")
    command = 'bwa mem -R "@RG\tID:Seq01p\tSM:Seq01\tPL:ILLUMINA\tPI:330" '
    command+= reference+' '
    for eachfile in fastq_files:
        command+=eachfile
        command+=' '
    command+= '> '
    sam_file_path = reference.split('/')
    sam_file_path = sam_file_path[:(len(sam_file_path)-1)]
    sam_file = ''
    for path in sam_file_path:
        sam_file+=(path+'/')
    
    global parent_dir
    parent_dir = sam_file
    sam_file+='fastQtoSam.sam'
    command+=sam_file
    print command
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Successfully created .sam file...")
    print err
    print out
    print "Coverted to sam"
    sort_sam(reference,sam_file)
    #7
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval

def openfilefasta():
    filename = askopenfilename() 
    global ref_path 
    ref_path = filename
    index_reference(filename)
    sort_reference(filename)
    create_dict(filename)
    print "Open your fastq files"
    B1 = Tkinter.Button(root, text ="Open fastq file", command = lambda :openfilefastq(filename))
    B1.pack()

    
def openfilefastq(reference):
    fastq_files = askopenfilename(multiple=True)
    print fastq_files
    align_create_sam(reference,fastq_files)
    
    
    
def sort_sam(reference,sam_file):
    command = ''
    command += 'picard-tools SortSam I='
    command+=(sam_file+ ' ')
    bam_file_path = sam_file.split('/')
    bam_file_path = bam_file_path[:(len(bam_file_path)-1)]
    bam_file = ''
    for path in bam_file_path:
        bam_file+=(path+'/')
    bam_file+='samTobam_sorted.bam'
    command+='O='
    command+=(bam_file+ ' ')
    command+='SORT_ORDER=coordinate VALIDATION_STRINGENCY=LENIENT CREATE_INDEX=true'
    print command
    progbarlabel.config(text = "Creating .bam file...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Successfully created .bam file...")
    print err
    print out
    print "Done bam conversion"
    #8
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    mark_dup(reference,bam_file)

def mark_dup(reference,bam_file):
    command = ''
    command+= 'picard-tools MarkDuplicates I='
    command+=bam_file
    command+=' O='
    bam_file_path = bam_file.split('/')
    bam_file_path = bam_file_path[:(len(bam_file_path)-1)]
    bam_file = ''
    for path in bam_file_path:
        bam_file+=(path+'/')
    bam_file+='samTobam_sorted_dedup.bam'
    global ddup_bam_path
    ddup_bam_path = bam_file
    command+=bam_file
    command+= ' METRICS_FILE=metrics.txt REMOVE_DUPLICATES=true'
    progbarlabel.config(text = "Marking Duplicates...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed Marking Duplicates...")
    print err
    print out
    #9
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    BuildBamIndex(reference,bam_file)
    
def BuildBamIndex(reference,bam_file):
    command = 'picard-tools BuildBamIndex INPUT='
    command+=bam_file
    progbarlabel.config(text = "Building bam index...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed building bam index...")
    
    print err
    print out
    print command
    print "Done BuildBamIndex"
    #10
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    CollectMultipleMetrics(reference, bam_file)


def CollectMultipleMetrics(reference, bam_file):
    command = 'picard-tools CollectMultipleMetrics INPUT='
    command+=(bam_file+' OUTPUT=')
    metrics_file_path = bam_file.split('/')
    metrics_file_path = metrics_file_path[:(len(metrics_file_path)-1)]
    metrics_file = ''
    for path in metrics_file_path:
        metrics_file+=(path+'/')
    log_file = metrics_file
    metrics_file+='recal.metrics'
    command+='VALIDATION_STRINGENCY=LENIENT PROGRAM=QualityScoreDistribution REFERENCE_SEQUENCE='
    command+=reference
    command+=(' &> '+log_file+'CollectMultipleMetrics.log')
    progbarlabel.config(text = "Collecting multiple metrics...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed collecting multiple metrics...")
    print err
    print out
    print command
    print "Done  Collect Multiple Metrics "
    #11
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    realignment_target(reference)

def realignment_target(reference):
    command1 = 'java -jar GenomeAnalysisTK.jar -T RealignerTargetCreator -R '
    command1+= (ref_path+ ' -I ')
    command1+= (ddup_bam_path+' -o ')
    command1+= (parent_dir+'realign.list')
    command = command1
    print 'realign'
    print command
    progbarlabel.config(text = "Realigning targets...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed realigning targets...")
    print err
    print out
    #12
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    indel_realignment((parent_dir+'realign.list'))

def indel_realignment(re_intervals):
    command = 'java -jar GenomeAnalysisTK.jar -T IndelRealigner -R '
    command+=ref_path
    command+= ' -I '
    command+=ddup_bam_path
    command+=(' -targetIntervals '+ re_intervals)
    command+= (' -o ' +parent_dir+'realigned.bam' )
    command+='  &> '
    command+=(parent_dir+'snpselectvariant.log-1')
    print command
    progbarlabel.config(text = "Realigning Indels...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed realigning Indels...")
    print err
    print out
    #13
    
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    call_variants()

def call_variants():
    command = 'java -jar GenomeAnalysisTK.jar -T HaplotypeCaller -R '
    command+=ref_path
    command+=' -I '
    command+=(parent_dir+ 'realigned.bam')
    command+= ' -o '
    command+= (parent_dir+'raw_variants.vcf')
    print command
    progbarlabel.config(text = "Calling varinants using GenomeAnalysisTK...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed Calling varinants using GenomeAnalysisTK...")
    print err
    print out
    #14
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    extract_snp()
    
def extract_snp():
    
    command= 'java -jar GenomeAnalysisTK.jar -T SelectVariants -R '
    command+=(ref_path + ' -V '+(parent_dir+'raw_variants.vcf -selectType SNP -o '+(parent_dir+'raw_snps.vcf')) )
    command+=(' &> '+(parent_dir+'snpselectvariant.log-1') )
    print command
    progbarlabel.config(text = "Extracting snp using GenomeAnalysisTK...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed extracting snp using GenomeAnalysisTK...")
    print err
    print out
    #15
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    extract_indels()

def extract_indels():
    command= 'java -jar GenomeAnalysisTK.jar -T SelectVariants -R '
    command+=(ref_path + ' -V '+(parent_dir+'raw_variants.vcf -selectType INDEL -o '+(parent_dir+'raw_indels.vcf')) )
    command+=(' &> '+(parent_dir+'snpselectvariant.log-1') )
    print command
    progbarlabel.config(text = "Extracting Indels using GenomeAnalysisTK...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Done extracting Indels using GenomeAnalysisTK...")
    print err
    print out
    #16
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    filter_snp()

def filter_snp():
    command='java -jar GenomeAnalysisTK.jar -T VariantFiltration -R '+ ref_path +' -V '+(parent_dir+'raw_snps.vcf')+ ' --filterExpression "QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0 || SOR > 4.0" --filterName "basic_snp_filter" -o filtered_snps.vcf'
    print command
    progbarlabel.config(text = "Filtering snp using GenomeAnalysisTK...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed filtering snp using GenomeAnalysisTK...")

    print err
    print out
    #17
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    filter_indel()

def filter_indel():
    command='java -jar GenomeAnalysisTK.jar -T VariantFiltration -R '+ ref_path +' -V '+(parent_dir+'raw_indels.vcf')+ ' --filterExpression "QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0 || SOR > 10.0" --filterName "basic_indel_filter" -o filtered_indels.vcf'
    print command
    progbarlabel.config(text = "Filtering indels using GenomeAnalysisTK...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed filtering indels using GenomeAnalysisTK...")
    print err
    print out
    #18
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    recalibrate1()

def recalibrate1():
    command = 'java -jar GenomeAnalysisTK.jar -T BaseRecalibrator -R '+ ref_path+ ' -I '+ (parent_dir+'realigned.bam')+' -knownSites '+(parent_dir+'filtered_snps.vcf')+' -knownSites filtered_indels.vcf -o '+(parent_dir+'recal_data.table')
    print command
    progbarlabel.config(text = "Recalibrating using GenomeAnalysisTK...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed recalibrating using GenomeAnalysisTK...")
    print err
    print out
    #19
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    recalibrate2()

def recalibrate2():
    command= 'java -jar GenomeAnalysisTK.jar -T BaseRecalibrator -R '+ ref_path+' -I '+ (parent_dir+'realigned.bam')+ ' -knownSites '+(parent_dir+'filtered_snps.vcf')+' -knownSites filtered_indels.vcf '+ ' -BQSR '+ (parent_dir+'recal_data.table')+ ' -o '+(parent_dir+'post_recal_data.table')
    print command
    progbarlabel.config(text = "Recalibrating again using GenomeAnalysisTK...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed recalibrating using GenomeAnalysisTK...")
    print err
    print out
    #20
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    analyze_covariates()
    
    
def analyze_covariates():
    command = 'java -jar GenomeAnalysisTK.jar -T AnalyzeCovariates -R '+ref_path+' -before '+(parent_dir+'recal_data.table')+' -after '+(parent_dir+'post_recal_data.table')+' -plots '+(parent_dir+'recalibration_plots.pdf')
    print command
    progbarlabel.config(text = "Analyzing Covariates using GenomeAnalysisTK...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed Analyzing Covariates using GenomeAnalysisTK...")
    print err
    print out
    #21
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    apply_BQSR()

def apply_BQSR():
    command = 'java -jar GenomeAnalysisTK.jar -T PrintReads -R '+ref_path+' -I '+(parent_dir+'realigned.bam')+' -BQSR '+(parent_dir+'recal_data.table')+ ' -o '+(parent_dir+'recal_reads.bam')
    print command
    progbarlabel.config(text = "Printing Reads using GenomeAnalysisTK...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed Printing Reads using GenomeAnalysisTK...")
    print err
    print out
    #22
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    call_variant_recal()
    
    
def call_variant_recal():
    command = 'java -jar GenomeAnalysisTK.jar -T HaplotypeCaller -R '
    command+=ref_path
    command+=' -I '
    command+=(parent_dir+ 'realigned.bam')
    command+= ' -o '
    command+= (parent_dir+'raw_variants_recal.vcf')
    print command
    progbarlabel.config(text = "Recalling variants using GenomeAnalysisTK...")
    
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed Recalling variants using GenomeAnalysisTK...")
    print err
    print out
    #23
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    extract_snp_recal()    
    
def extract_snp_recal():
    
    command= 'java -jar GenomeAnalysisTK.jar -T SelectVariants -R '
    command+=(ref_path + ' -V '+(parent_dir+'raw_variants_recal.vcf -selectType SNP -o '+(parent_dir+'raw_snps_recal.vcf')) )
    print command
    progbarlabel.config(text = "Recalling extract snp using GenomeAnalysisTK...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed Recalling extract snp using GenomeAnalysisTK...")
    print err
    print out
    #24
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    extract_indels_recal()
    
def extract_indels_recal():
    command= 'java -jar GenomeAnalysisTK.jar -T SelectVariants -R '
    command+=(ref_path + ' -V '+(parent_dir+'raw_variants_recal.vcf -selectType INDEL -o '+(parent_dir+'raw_indels_recal.vcf')) )
    command+=(' &> '+(parent_dir+'snpselectvariant.log-1') )
    progbarlabel.config(text = "Recalling extract indels using GenomeAnalysisTK...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed Recalling extract indels using GenomeAnalysisTK...")
    print err
    print out
    print command
    #25
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    filter_snp_recal()

def filter_snp_recal():
    
    command='java -jar GenomeAnalysisTK.jar -T VariantFiltration -R '+ ref_path +' -V '+(parent_dir+'raw_snps_recal.vcf')+ ' --filterExpression "QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0 || SOR > 4.0" --filterName "basic_snp_filter" -o filtered_snps_final.vcf'
    print command
    progbarlabel.config(text = "Recalling filtering snp using GenomeAnalysisTK...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Recalling filtering snp using GenomeAnalysisTK...")
    print err
    print out
    #26
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    filter_indel_recal()

def filter_indel_recal():
    command='java -jar GenomeAnalysisTK.jar -T VariantFiltration -R '+ ref_path +' -V '+(parent_dir+'raw_indels_recal.vcf')+ ' --filterExpression "QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0 || SOR > 10.0" --filterName "basic_indel_filter" -o filtered_indels_recal.vcf'
    progbarlabel.config(text = "Recalling filtering indels using GenomeAnalysisTK...")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Recalling filtering indels using GenomeAnalysisTK...")
    
    print err
    print out
    print command
    proc = subprocess.Popen("python snpeff_final.py", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    #27
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    
    
def openfilesra():
    filename = askopenfilename()
    global sra_path
    sra_path = filename
    command = ''
    option.pack( side='top', padx =10, pady=10)
    global split_button
    split_button = Tkinter.Button(root, text="SUBMIT", command= split_file)
    split_button.pack()

    
def split_file():
    
    chosen = var.get()
    command = ''
    print chosen
    if(chosen=='Single-end'):
        command+=('fastq-dump'+ ' '+ sra_path)
    else:
        command+=('fastq-dump --split-files '+ sra_path)
    
    progbarlabel.config(text = "Splitting files using fastq-dump....")
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    print err
    print out
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    progbarlabel.config(text = "Splitting files using fastq-dump completed")

    
    split_button.destroy()
    adadp_fastq.pack()


def select_adapter(fastq_files):
    Bsra.destroy()
    option.destroy()
    command = ''
    proc = subprocess.Popen('chmod 777 ./FastQC/fastqc', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    for each in fastq_files:
        command+='./FastQC/fastqc -f fastq '+ (each+' ')
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    open_browser = 'firefox '
    all_html = ''
    
    for each in fastq_files:
        print each
        newfile = each.split('.')
        print newfile
        all_html+= (newfile[0]+'_fastqc.html'+' ')
        print all_html
    open_browser+=all_html
    progbarlabel.config(text = "Generating FastQC...")
    proc = subprocess.Popen(open_browser, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    progbarlabel.config(text = "Completed generating FastQC..")
        
    global adapter_root
    adapter_root = Tkinter.Tk()
    adapter_root.title('Adapter content removal')
    adapter_root.geometry('{}x{}'.format(444, 444))
    adapter_submit = Tkinter.Button(adapter_root, text ="SUBMIT", command = lambda : getadapter(fastq_files,adapter_term.get()))
    label1 = Tkinter.Label( adapter_root, text="Enter Adapter content sequece")
    adapter_term = Tkinter.Entry(adapter_root, bd =5)
    label1.pack()

    adapter_term.pack()
    adapter_submit.pack()
    label2 = Tkinter.Label( adapter_root, text="Illumina Universal Adapter - AGATCGGAAGAG")
    label3 = Tkinter.Label( adapter_root, text="Illumina Small RNA Adapter - ATGGAATTCTCG")
    label4 = Tkinter.Label( adapter_root, text="Nextera Transposase Sequence - CTGTCTCTTATA")
    label5 = Tkinter.Label( adapter_root, text="SOLID Small RNA Adapter - CGCCTTGGCCGT")
    label2.pack()
    label3.pack()
    label4.pack()
    label5.pack()
    #2
    
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    

    
  
    

def openfilefastq_adpt():
    fastq_files = askopenfilename(multiple=True)
    print fastq_files
    select_adapter(fastq_files)
        
    
    
B = Tkinter.Button(root, text ="Open fasta file", command = openfilefasta)
Bsra = Tkinter.Button(root, text ="Open sra file", command = openfilesra)
adadp_fastq = Tkinter.Button(root, text ="Open FASTQ file", command = openfilefastq_adpt)

var  = Tkinter.StringVar(root)
var.set('Single-end')
choices  = ['Single-end', 'Paired-end']
option = Tkinter.OptionMenu(root, var, *choices)


progbarlabel = Tkinter.Label(root, text="Completion bar")
progbarlabel.pack(side="bottom")

progbar = ttk.Progressbar(root,orient ="horizontal",length = 200, mode ="determinate")
progbar.pack( side="bottom")
progbar["maximum"] = 100
progbarval = 0


def getadapter(fastq_files, adapter):
    command = ''
    progbarlabel.config(text = "Removing adapter content...")
    for each in fastq_files:
        command+='grep '+adapter+' -c '+ each
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if out != 0 :
            newfile = each.split('.')
            newfile = newfile[0]
            newfile+='_trimmed.fastq'
            command1 = 'cutadapt -b '+ adapter+ ' '+ each+ ' '+' -o '+ newfile
            print command1
            proc = subprocess.Popen(command1, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = proc.communicate()
    B.pack()
    #3
    global progbarval
    progbarval+=3
    progbar["value"] = progbarval
    adapter_root.destroy()
    adadp_fastq.destroy()
    progbarlabel.config(text = "Adapter content successfully removed..")

            
Bsra.pack()
root.mainloop()


# In[ ]:




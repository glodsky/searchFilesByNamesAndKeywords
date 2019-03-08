import os, sys
import glob
from os import listdir
from os.path import isfile, join ,splitext , basename
import datetime
import shutil
    
def get_Allfiles(rootdir,extendname,KeyWords):
    vfs = []
    for KeyWord in KeyWords:
        for fpathe,dirs,fs in os.walk(rootdir):
          for f in fs:
            if f.find(KeyWord)>=0 and (os.path.splitext(f)[1] in extendname) : # filename include KeyWord
                vfs.append (os.path.join(fpathe,f))            
    return vfs
                            
def search_keys_in_Sources(path,filename_parts,KeyWords,extendname):
    save_path = ""
    founds = []
    line_num = 0
    #### filter out including filename_parts of files
    files = get_Allfiles(path,extendname,filename_parts)
    
    #### find KeyWord in each file's content 
    for item in files:
        print('item = %s' % item)
        #print('Now search %s in %s'%(KeyWord,item))
        ff = open(item,'r',encoding='utf-8')
        line_num =0
        for line in ff:
            line_num += 1
            shortname = ""
            for keyword in KeyWords :
                at_s = line.find(keyword)
                if at_s >=0 :
                    print("Found at : %s"%line)
                    shortname = item.split("\\")[-1] 
                    line_f = "在【%s】发现【%s】 第【%s】行 第【%s字】始：\n%s\n"%(shortname,keyword,line_num,at_s,line)
                    founds.append(line_f) #只匹配成功任意一个 就跳出该行查找 继续下一行匹配
                    continue
        ff.close()
        
    #### Copy to current dir
    for item in files:
        shortname = item.split("\\")[-1]
        new_f = os.path.join(os.curdir,shortname)
        if os.path.exists(new_f) :
            os.unlink(new_f)
        shutil.copyfile(item,new_f)
        print("Copy File %s is Over"%shortname)
        
    #### Generate report and To save local
    cur_date = datetime.datetime.now().strftime('%Y%m%d')
    report_f = "%s_%s.txt"%("#".join(KeyWords),cur_date)
    if os.path.exists(report_f):
        os.unlink(report_f)
    fn = open(report_f,'w+',encoding='utf-8') 
    fn.write("Search KeyWord : 【%s】 \n"% " # ".join(KeyWords))
    fn.write("\n".join(files))
    fn.write("\n===================\n")
    if founds != []:
        fn.write("\n".join(founds))
    fn.close()
    print("\nGenerate report is over!")

def main(): 
    cur_dir = r'D:\canDel\殆知阁古代文献藏书2.0版（全TXT版）\殆知阁古代文献藏书2.0版（全TXT版）'
    if !os.path.exists(cur_dir) :
        print("Not Exists %s"%cur_dir)
        exit(0)
    extendname = ['.txt','.pdf']
    fname_parts = ['文始','通玄']  #'文始真经'
    key_words = ['造化','阴阳']
    print("cur_dir = %s  key_word=%s\n"%(cur_dir," # ".join(key_words)))

    search_keys_in_Sources(cur_dir,fname_parts,key_words,extendname)


    
if __name__=="__main__":
    main()

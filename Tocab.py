import os
import sys
import datetime

def fprintf(stream, format_spec, *args): 
    #print("="*80)
    stream.write(format_spec % args) 
def checkInf(path):
    idx = path.rfind("inf")
    if  idx == -1:
        return None
    print("Found INF: ", path)
    if os.path.exists(".\htm"): #清理之前遗留下来的旧档
        #os.rmdir(".\htm")
        for root, dirs, files in os.walk(".\htm", topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    chkinf = "D:\\WinDDK\\7600.16385.0\\tools\\Chkinf\\chkinf.bat"
    os.system('%s \"%s\"' % (chkinf, path));
    
def addheader(filename):
    str = ''';*** Echo.ddf example
;
.OPTION EXPLICIT     ; Generate errors
.Set CabinetFileCountThreshold=0
.Set FolderFileCountThreshold=0
.Set FolderSizeThreshold=0
.Set MaxCabinetSize=0
.Set MaxDiskFileCount=0
.Set MaxDiskSize=0
.Set CompressionType=MSZIP
.Set Cabinet=on
.Set Compress=on
;Specify file name for new cab file
.Set CabinetNameTemplate=%s.cab
; Specify the subdirectory for the files.  
; Your cab file should not have files at the root level,
; and each driver package must be in a separate subfolder.
.Set DestinationDir=%s
;Specify files to be included in cab file
'''
    with open('test.ddf', 'w') as fp:
        fp.write(str % (filename,filename))
    
    
# 遍历文件夹
def walkFile(file):
    
    print("walkFile ==>", file)    
    with open('test.ddf', 'a+') as fp:
        for root, dirs, files in os.walk(file):
    
            # root 表示当前正在访问的文件夹路径
            # dirs 表示该文件夹下的子目录名list
            # files 表示该文件夹下的文件list
    
            # 遍历文件
            for f in files:
                path = os.path.join(root, f);
                #print(path)
                checkInf(path)
                fprintf(fp, "\"%s\"\n",path)
            # 遍历所有的文件夹
            for d in dirs:
                print(os.path.join(root, d))
            
def Tocab(adir, filename):
    argc = len(sys.argv)
    a=adir.rfind("\\")
    suffix_date = datetime.datetime.now().date()
    suffix =suffix_date.__format__('%Y%m%d')
    if(filename ==""):
        filename = adir[a+1:]
    else:
        filename = filename + "_" + suffix
    filename = filename 
    print(filename)
    #return
    addheader(filename)
    walkFile(adir)
    os.system('Makecab /f test.ddf')
    print("output: " + os.path.dirname(os.path.realpath(__file__))+"\\disk1\\" +filename +".cab")

if __name__ == '__main__':
    '''
    usage : Tocab.py   [dir]   
    for example Tocab.py G:\\xv\\MP_branch\\8723F\\8723F 
    '''
    
    ic = "RTL8822C"
    #adir = sys.argv[1]
    #a = adir.rfind("\\")
    #ic = adir[a+1:]
    #adir="G:\\xv\\MP_branch\\8723F\\8723F"
    adir = "G:\\xv\\MP_branch\\8822c\\8822c"
    s = "EUS"
    if (str.__contains__(s, 'E')):
        Tocab(adir + "\\RTLWlanE_WindowsDriver_\\Win7\\X64", ic  + "E_Win7x64")
        Tocab(adir + "\\RTLWlanE_WindowsDriver_\\Win7\\X86", ic  + "E_Win7x86")
    if (str.__contains__(s, 'S')):
        Tocab(adir + "\\RTLWlanS_WindowsDriver_\\Win7\\X64", ic  + "S_Win7x64")
        Tocab(adir + "\\RTLWlanS_WindowsDriver_\\Win7\\X86", ic  + "S_Win7x86")
    if (str.__contains__(s, 'U')):
        Tocab(adir + "\\RTLWlanU_WindowsDriver_\\Win7\\X64", ic  + "U_Win7x64")
        Tocab(adir + "\\RTLWlanU_WindowsDriver_\\Win7\\X86", ic  + "U_Win7x86")
        

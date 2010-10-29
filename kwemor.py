import sys,os

class Kwemore:
    
    def __init__(self): # constructor
        print "Kwemore, the website monitor"
        
    # print how to use kwemor from the commandline
    def Usage(self):
        print 'Usage: Kwemore \n\tpython kwemore.py --<arguments>\n\n\tArguments'
        print '\t\t--adduser:\n\t\tuse this option to a new user.'
        print '\n\t\te.g: python kwemore.py --adduser <twitter_username>\n\n' 
        
    
    def StrippedLine(self, line):
        array = line.split("=>")
        line = array[1].strip().strip("',").strip()
        
        if line.endswith(":"): line = line.rstrip(":")
        if line.endswith("."): line = line.rstrip(".")
        if '\\' in line: line = line.replace("\\", "")
        
        return line
    
    # Read content of a file
    def ReadLines(self, path):
        f = open(path, 'r')
        content = f.readlines()
        
        f.close()
        
        return content
    
    #write content to a file
    def WriteLines(self, path, content):
        # by default we delete the file before we write anything to it
        if os.path.exists(path): 
            os.remove(path)
            
        # recreate a new file and append the content to it
        f = open(path, 'w')
        f.writelines(content)
        f.close()
    
        
    def Unlisted(self, list = [], line = ""):
        result = False
        line = line.lower()
        if line != "" and not line in list:
            list.append(line)
            result = True
        
        return result
    
    
    def GeneratePot(self, dir, pfile):
        temp = [ ]
        list = [ ]
        
        for root, dirs, files in os.walk(dir):
            for file in [f for f in files if f.endswith(".php")]:
                lines = self.ReadLines(os.path.join(root, file))
                
                for line in [l for l in lines if "=>" in l and not l.strip().endswith('array')]:
                    
                    line = self.StrippedLine(line)

                    if self.Unlisted(temp, line):
                        list.append(line)
        count = 0
        list.sort() # just the default list sorting algorithm 
        
        if os.path.exists(pfile): os.remove(pfile)
        f = open(pfile, 'w')
        for msgid in list:
            f.write(' Key:\n')
            f.write('msgid "%s"\n'%msgid)
            f.write('msgstr ""\n\n')
            count += 1
        f.close()
        
        return count


    def GeneratePHP(self, pfile, dir):
        temp = [ ]
        for line in self.ReadLines(pfile):
            if not line == "":
                temp.append(line)
        count = 0
        for root, dirs, files in os.walk(dir):
            for file in [f for f in files if f.endswith(".php")]:
                fn = os.path.join(root, file) # filename
                list = [ ]
                
                for line in self.ReadLines(fn):
                    if "=>" in line and not line.strip().endswith('array'):
                        item = self.StrippedLine(line)
                        msgid = ""
                        msgstr = ""
                        found = False
                        
                        for i in range(0, len(temp) - 1):
                            if temp[i].startswith("msgid"):
                                msgid  = temp[i].replace("msgid", "").strip().strip('"').strip()
                                msgstr = msgid # just incase the translation isnt available, retain original string
                                
                                if msgid.lower() == item.lower():
                                    found = True
                                    msgstr = temp[i+1].replace("msgstr", "").strip().strip('"').strip()
                                    break
                        
                        if found and msgid != "" and msgid != msgstr and msgid in line:
                            if msgid.lower() in line.lower():
                                if msgid.isupper(): # retain the original case
                                    msgstr = msgstr.upper()
                                line = line.replace(msgid, msgstr)
                                list.append(line)
                            count += 1
                    else:
                        list.append(line)
                        
                self.WriteLines(fn, list)       
        return count

    
    def SyncFiles(self, oldfile, newfile):
        list = [ ]
        ol = self.ReadLines(oldfile) # old list
        nl = self.ReadLines(newfile) # new list
        
        count = 0
        for i in range(len(nl) - 1):
            l = nl[i]
            if l.startswith("msgid"):
                msgid  = nl[i]
                msgstr = nl[i+1]

                for j in range(len(ol) - 1):
                    if ol[j] == msgid:
                        msgstr = ol[j+1]
                        count += 1
                        break
                msgstr += '\n\n'
                list.append(msgid)
                list.append(msgstr)
        
        self.WriteLines(newfile, list)
        return count
 

if __name__ == '__main__':
    i18n = Ushahidi18nParser()
    
    x = len(sys.argv)
    
    if x < 3:
        i18n.Usage()
    
    else:
        if sys.argv[1] == '--genpot': # --genpot path potfile
            print '\tGenerated a pot file with %s strings\n'%i18n.GeneratePot(sys.argv[2], sys.argv[3]) 
   
        elif sys.argv[1] == '--genphp': # --genphp potfile path
            print '\tRegenerated the php files with %s translated strings\n'%i18n.GeneratePHP(sys.argv[2], sys.argv[3])
          
        elif sys.argv[1] == '--sync': # --sync oldfile newfile
            print '\tSynced %s strings\n'%i18n.SyncFiles(sys.argv[2], sys.argv[3])

        elif sys.argv[1] == '--usage': # --usage available options
            i18n.Usage()

        else:
            print "Error: Unknown argument\n"
            i18n.Usage()

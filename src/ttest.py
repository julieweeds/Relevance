__author__ = 'Julie'

import os,math

def loadtotals(filename):

    print "Reading "+filename
    mydict={}
    gt=0
    with open(filename,'r') as instream:
        for line in instream:
            fields=line.rstrip().split('\t')
            mydict[fields[0]]=float(fields[1])
            gt+=float(fields[1])

    mydict['__GT__']=gt
    return mydict

def compute_tscore(joint,ent,feat,gt):
    ind = ent*feat
    tscore=(joint*gt-ind)/math.pow(ind,0.5)
    return tscore

def compute_score(joint,ent,feat,gt,score):
    if score=='ts':
        return compute_tscore(joint,ent,feat,gt)
    else:
        print "Unknown association score "+score
        exit()

def processfile(filename,entdict,featdict):
    print "Reading "+filename

    gt1 = entdict.get('__GT__',0)
    gt2 = featdict.get('__GT__',0)
    if gt1 != gt2:
        print "Grandtotals do not match",str(gt1),str(gt2)
        exit()
    linesread=0
    with open(filename,'r') as instream:
        with open(filename+'_tt','w') as outstream:


            for line in instream:
                outputlist=[]
                linesread+=1
                if linesread%1000==0: print "Processed "+str(linesread)+" lines"
                fields=line.rstrip().split('\t')
                entry=fields[0]
                entryfreq=entdict.get(entry,0)
                while(len(fields[1:])>0):
                    joint = float(fields.pop())
                    feat = fields.pop()
                    featfreq=featdict.get(feat,0)
                    score = compute_score(joint,entryfreq,featfreq,gt1,'ts')
                    if score>0:
                        outputlist.append((score,feat))
                if len(outputlist)>0:
                    #outputlist.sort(reverse=True)
                    outstream.write(entry)
                    for(sc,f) in outputlist:
                        outstream.write('\t'+f+'\t'+str(sc))
                    outstream.write('\n')
if __name__=="__main__":

    parentdir="/Volumes/LocalScratchHD/juliewe/Documents/workspace/ThesEval/data/wiki_t100f100_nouns_deps"
    filename="events.strings"
    featext="_depcol"
    entext="_deprow"

    featdict=loadtotals(os.path.join(parentdir,filename+featext))
    entdict=loadtotals(os.path.join(parentdir,filename+entext))

    processfile(os.path.join(parentdir,filename),entdict,featdict)
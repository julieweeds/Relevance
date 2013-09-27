__author__ = 'juliewe'

import sys,os
from conf import configure


class Vector():

    def __init__(self,name,featurelist,params):

        self.name=name
        self.params=params
        self.makefeatures(featurelist)
        self.sorted=False

    def makefeatures(self,featurelist):

        self.featurelist=[]
        while(len(featurelist)>0):
            score = float(featurelist.pop())
            feat = featurelist.pop()
            self.featurelist.append((score,feat))
        self.origwidth=len(self.featurelist)
        if self.params["testing"]:
            print self.origwidth, self.featurelist

    def filterfeatures(self,n_feats,featuredict):

        if self.params["testing"]:
            print self.featurelist
        if not self.sorted:
            self.featurelist.sort(reverse=False)
        else:
            self.featurelist.reverse()

        newlist=[]
        self.filteredtotal=0
        while len(newlist)<n_feats and len(self.featurelist) > 0:
            newlist.append(self.featurelist.pop())
        for(sc,feat) in newlist:
            self.filteredtotal+=sc
            featuredict[feat] = featuredict.get(feat,0)+sc
        self.sorted=True
        self.featurelist=newlist
        self.filteredwidth=len(self.featurelist)
        return featuredict

    def writewidths(self,outstream1,outstream2,outstream3):

        outstream1.write(self.name+"\t")
        outstream2.write(self.name+"\t")
        outstream1.write(str(self.origwidth)+"\n")
        outstream2.write(str(self.filteredwidth)+"\n")
        outstream3.write(self.name+"\t")
        outstream3.write(str(self.filteredtotal)+"\n")


    def writevector(self,outstream):
        outstream.write(self.name)
        for (score,feat) in self.featurelist:
            outstream.write("\t"+feat+"\t"+str(score))
        outstream.write("\n")

class VectorSpace():

    def __init__(self, params):

        self.params=params
        self.datapath=os.path.join(params['datadir'],params['datafile'])
        self.widthfile=os.path.join(params['datadir'],params['datafile']+'.widths')
        self.relevantvectorsfile=os.path.join(params['datadir'],params['datafile']+"_rel"+str(self.params.get("n_feat",10)))
        self.relevantwidthfile=self.relevantvectorsfile+'.widths'
        self.relevantentries=self.relevantvectorsfile+"_entries.strings"
        self.relevantfeatures=self.relevantvectorsfile+"_features.strings"
        self.featuredict={}
        if self.params["testing"]:
            self.check=10
        else:
            self.check=1000


    def processfile(self):
        with open(self.datapath) as instream:
            with open(self.widthfile,'w') as outstream1:
                with open(self.relevantwidthfile,'w') as outstream2:
                    with open(self.relevantvectorsfile,'w') as outstream3:
                        with open(self.relevantentries,'w') as outstream4:
                            print "Reading "+self.datapath
                            linesread=0
                            for line in instream:
                                line=line.rstrip()
                                fields=line.split('\t')
                                vectorname=fields[0]
                                avector=Vector(vectorname,fields[1:],self.params)
                                self.featuredict=avector.filterfeatures(self.params.get("n_feat",10),self.featuredict)
                                avector.writewidths(outstream1,outstream2,outstream4)
                                avector.writevector(outstream3)
                                linesread+=1
                                if linesread%self.check==0:
                                    print "Processed "+str(linesread)+" lines"
                                    if self.params["testing"]: break

                print "Finished processing file: "+str(linesread)+" lines"

        print "Writing feature file"
        with open(self.relevantfeatures,'w') as outstream:
            for (feat,sc) in self.featuredict.items():
                outstream.write(feat+"\t"+str(sc)+"\n")




if __name__=="__main__":

    params = configure(sys.argv)
    myVectors = VectorSpace(params)

    if params.get("filter",False):
        myVectors.processfile()


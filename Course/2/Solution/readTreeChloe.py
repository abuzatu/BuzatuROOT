#!/usr/bin/python

# python
import os,sys
# PyROOT
from ROOT import gROOT, TFile, TTree, TLorentzVector, TH1F
gROOT.SetBatch(True)

total = len(sys.argv)
# number of arguments plus 1
if total!=2:
    print "You need some arguments, will ABORT!"
    print "Ex: ./readTree.py NrEntries"
    print "Ex: ./readTree.py 100"
    print "Ex: ./readTree.py -1"
    assert(False)
# done if

NrEntries=sys.argv[1]
desiredNrEntries=int(NrEntries)

debug=False
fileName="./input/tree_llbb.root"
treeName="perevent"
outputfileName="./output/histo_llbb.root"


if debug:
    print "We want to run over",desiredNrEntries,"entries."

def getTLV( particle , derivation , entry ):

    prefix=particle+"_"+derivation
    
    attnamePt=prefix+"_Pt"
    b_Pt=getattr(entry,attnamePt)
    
    attnameEta=prefix+"_Eta"
    b_Eta=getattr(entry,attnameEta)
    
    attnamePhi=prefix+"_Phi"
    b_Phi=getattr(entry,attnamePhi)
    
    attnameE=prefix+"_E"
    b_E=getattr(entry,attnameE)
    
    if debug:
        print "b_Pt",b_Pt
        print "b_Eta",b_Eta
        print "b_Phi",b_Phi
        print "b_E",b_E
        
    #define TLorentzvec 
    b_tlv=TLorentzVector()
    b_tlv.SetPtEtaPhiE(b_Pt,b_Eta,b_Phi,b_E)
        
    return b_tlv;

        
def readTree( derivation ):
    
    # open file
    file=TFile(fileName,"READ")
    if not file.IsOpen():
        print "File",fileName,"does not exist. WILL ABORT!!!"
        assert(False)
        
    # open tree
    tree=file.Get(treeName)
    if tree==None:
        print "tree",treeName,"doesn't exist in file",fileName,". WILL ABORT!!!"
        assert(False)
        
    # determine how many entries to run on 
    nrEntries=tree.GetEntries()
    if desiredNrEntries<0 or desiredNrEntries>nrEntries:
        actualNrEntries=nrEntries
    else:
        actualNrEntries=desiredNrEntries
    if debug:
        print "We will run over",actualNrEntries,"entries."
        
    # we create a file to store histograms
    outputfile=TFile(outputfileName,"UPDATE")

    #Make higgs mass histogram
    histname = "Higgs_" + derivation + "_M"
    hist_Higgs_M=TH1F(histname,histname,40,48.5,168.5)

    # run over the entries of the tree
    for i, entry in enumerate(tree):
        if i>=actualNrEntries:
            continue
        if debug or i%1000==0:
            print "******* new entry",i," **********"

        b1_tlv=getTLV("b1",derivation,entry)
        b2_tlv=getTLV("b2",derivation,entry)


        b1_M=b1_tlv.M()
        b2_M=b2_tlv.M()
        if debug:
            print "b1_M",b1_M
            print "b2_M",b2_M
            
        # Higgs boson candidate decaying to b1 and b2 
        # TLorentzVector is the sum of the two TLorentzVectors
        Higgs_tlv=b1_tlv+b2_tlv
        Higgs_Pt=Higgs_tlv.Pt()
        Higgs_Eta=Higgs_tlv.Eta()
        Higgs_Phi=Higgs_tlv.Phi()
        Higgs_E=Higgs_tlv.E()
        if debug:
            print "Higgs_Pt",Higgs_Pt
            print "Higgs_Eta",Higgs_Eta
            print "Higgs_Phi",Higgs_Phi
            print "Higgs_E",Higgs_E
            
        Higgs_M=Higgs_tlv.M()
        
        if debug:
            print "Higgs_M",Higgs_M

        #fill histo
        hist_Higgs_M.Fill(Higgs_M)
        
    # done loop over all the entries in the tree
    outputfile.Write()
    outputfile.Close()
# done function


# execute
readTree("Nominal")
readTree("OneMu")
readTree("OneMuNu")
readTree("AllMu")
readTree("AllMuNu")
readTree("PtRecoBukin")
readTree("PtRecoGauss")
readTree("Regression")
readTree("Parton")
 

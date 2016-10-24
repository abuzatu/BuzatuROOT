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


if debug:
    print "We want to run run over",desiredNrEntries,"entries."

def Jets(jet, calib, entry):
	
	name = jet + "_" + calib + "_"
	Ptname = name + "Pt"
	Etaname =  name + "Eta"
	Phiname = name +"Phi"
	Ename = name + "E"
	
	b_Pt = getattr(entry,Ptname)
        b_Eta = getattr(entry,Etaname)
        b_Phi = getattr(entry,Phiname)
        b_E = getattr(entry,Ename)
        
	b_tlv = TLorentzVector() 
        b_tlv.SetPtEtaPhiE(b_Pt,b_Eta,b_Phi,b_E)
        b_M = b_tlv.M()  

	return b_tlv
        
def ChooseCalibration(calib,tree,actualNrEntries,outputfile):

    Histoname = "Higgs_" + calib + "_M"
    #outputfileName = "./output/histo_llbb" + calib + ".root"
    # we create a file to store histograms

    #outputfile=TFile(outputfileName,"RECREATE")
    hist_Higgs_M=TH1F(Histoname,Histoname,40,48.5,168.5)
    # run over the entries of the tree
    # unlike in C++, no need to define the branches in advance
    for i, entry in enumerate(tree):
        if i>=actualNrEntries:
            continue
        if debug or i%1000==0:
            print "******* new entry",i," **********"

        # jet 1
        b1_tlv = Jets("b1",calib, entry) 
        # jet 2
        b2_tlv = Jets("b2", calib, entry) 
        
        # Higgs boson candidate decaying to b1 and b2 
        # TLorentzVector is the sum of the two TLorentzVectors
        Higgs_tlv = b1_tlv + b2_tlv
        Higgs_Pt = Higgs_tlv.Pt()
        Higgs_Eta = Higgs_tlv.Eta()
        Higgs_Phi = Higgs_tlv.Phi()
        Higgs_E = Higgs_tlv.E()
       
        Higgs_M = Higgs_tlv.M()
       
        # the mass should be 125, but when measured we get a distribution around 125
        # we store that in a histogram
        hist_Higgs_M.Fill(Higgs_M)
    # done loop over all the entries in the tree
    outputfile.Write()
    #outputfile.Close()


def readTree():
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
    
    outputfileName = "./output/histo_llbbtest.root"
    outputfile=TFile(outputfileName,"RECREATE")
    #there are nine options
    ChooseCalibration("Nominal", tree, actualNrEntries,outputfile)
    ChooseCalibration("OneMu", tree, actualNrEntries,outputfile)
    ChooseCalibration("PtRecoBukin", tree, actualNrEntries,outputfile)
    ChooseCalibration("PtRecoGauss", tree, actualNrEntries,outputfile)
    ChooseCalibration("Regression", tree, actualNrEntries,outputfile)
    ChooseCalibration("OneMuNu", tree, actualNrEntries,outputfile)
    ChooseCalibration("AllMu", tree, actualNrEntries,outputfile)
    ChooseCalibration("AllMuNu", tree, actualNrEntries,outputfile)
    ChooseCalibration("Parton", tree, actualNrEntries,outputfile)
    outputfile.Close()

    
# execute
readTree()

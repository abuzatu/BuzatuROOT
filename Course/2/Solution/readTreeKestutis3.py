#!/usr/bin/python

# Kestutis Kanisauskas @ University of Glasgow

# python
import os,sys,re
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
    print "We want to run run over",desiredNrEntries,"entries."

def getCorrList(tree):
    corrList = []
    branchNameList = []
    branchList = tree.GetListOfBranches() # obtaining list of branches from the tree in order to extract their names
    for i in range(branchList.GetEntries()):
        branchNameList.append(branchList.At(i).GetName())
    # Building List of Corrections
    for j in branchNameList:
        found = re.search('b1_(.+?)_Pt', j) # Assuming _Eta, _Phi, _E parts exist as well
        if found:
            label = found.group(1)
            corrList.append(label)
    return corrList
    
def getSpecificData(entry, tName='Nominal', bVal='b1', debug=True):
    b_Opt_Pt_Arg = bVal + "_" + tName +"_Pt"
    b_Opt_Eta_Arg = bVal + "_" + tName +"_Eta"
    b_Opt_Phi_Arg = bVal + "_" + tName +"_Phi"
    b_Opt_E_Arg = bVal + "_" + tName +"_E"
    
    b_Opt_Pt=getattr(entry,b_Opt_Pt_Arg)
    b_Opt_Eta=getattr(entry,b_Opt_Eta_Arg)
    b_Opt_Phi=getattr(entry,b_Opt_Phi_Arg)
    b_Opt_E=getattr(entry,b_Opt_E_Arg)
    
    if debug:
        print b_Opt_Pt_Arg,b_Opt_Pt
        print b_Opt_Eta_Arg,b_Opt_Eta
        print b_Opt_Phi_Arg,b_Opt_Phi
        print b_Opt_E_Arg,b_Opt_E
    
    return (b_Opt_Pt, b_Opt_Eta, b_Opt_Phi, b_Opt_E)

def getHiggsMass(entry,tName,debug):
    # we are looping over jets, each has the information of Pt, Eta, Phi, E
    # they are available at different calibration stages:
    # Nominal, OneMu, PtRecoBukin, PtRecoGauss, Regression
    # we also know what is the correct simulated information: Parton
    # we want to compare the different calibrations and see which one 
    # models better the Higgs boson mass
    # all Pt, E, M are in GeV
    # Higgs -> bb, meaning the b1 and b2 in this tree
    # let's see how we get a variable from the tree
    
    # jet 1 
    # >>> b1 <<<
    b1_Opt_Pt,b1_Opt_Eta,b1_Opt_Phi,b1_Opt_E = getSpecificData(entry=entry, tName=tName, bVal="b1",debug=debug)    
    b1_Opt_tlv=TLorentzVector()
    b1_Opt_tlv.SetPtEtaPhiE(b1_Opt_Pt,b1_Opt_Eta,b1_Opt_Phi,b1_Opt_E)
    b1_Opt_M=b1_Opt_tlv.M()
    if debug:
        print "b1_%s_M"%(tName),b1_Opt_M
        
    # jet 2
    # >>> b2 <<<
    b2_Opt_Pt,b2_Opt_Eta,b2_Opt_Phi,b2_Opt_E = getSpecificData(entry=entry, tName=tName, bVal="b2",debug=debug)
    b2_Opt_tlv=TLorentzVector()
    b2_Opt_tlv.SetPtEtaPhiE(b2_Opt_Pt,b2_Opt_Eta,b2_Opt_Phi,b2_Opt_E)
    b2_Opt_M=b2_Opt_tlv.M()
    if debug:
        print "b2_%s_M"%(tName),b2_Opt_M
        
    # Higgs boson candidate decaying to b1 and b2 
    # TLorentzVector is the sum of the two TLorentzVectors
    Higgs_Opt_tlv=b1_Opt_tlv+b2_Opt_tlv
    Higgs_Opt_Pt=Higgs_Opt_tlv.Pt()
    Higgs_Opt_Eta=Higgs_Opt_tlv.Eta()
    Higgs_Opt_Phi=Higgs_Opt_tlv.Phi()
    Higgs_Opt_E=Higgs_Opt_tlv.E()
    if debug:
        print "Higgs_%s_Pt"%(tName),Higgs_Opt_Pt
        print "Higgs_%s_Eta"%(tName),Higgs_Opt_Eta
        print "Higgs_%s_Phi"%(tName),Higgs_Opt_Phi
        print "Higgs_&s_E"%(tName),Higgs_Opt_E
    Higgs_Opt_M=Higgs_Opt_tlv.M()
    if debug:
        print "Higgs_%s_M"%(tName),Higgs_Opt_M
    # the mass should be 125, but when measured we get a distribution around 125
    
    return Higgs_Opt_M

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
    
    if desiredNrEntries < 0 or desiredNrEntries>nrEntries:
        actualNrEntries=nrEntries
    else:
        actualNrEntries=desiredNrEntries
    if debug:
        print "We will run over",actualNrEntries,"entries."
    # modified -> correction list is obtained autatically
    corrList = getCorrList(tree)
    # we create a file to store histograms
    outputfile=TFile(outputfileName,"RECREATE")
    # Building dictionary of histograms and correction names
    dictHist = {} 
    for tName in corrList:
        titleHist = "Higgs_" + tName + "_M"
        dictHist[tName] = TH1F(titleHist,titleHist,40,48.5,168.5) #tName will serve as a key to a particular histogram

   # titleHist = "Higgs_" + tName + "_M"
   #  hist_Higgs_Opt_M=TH1F(titleHist,titleHist,40,48.5,168.5)
    # run over the entries of the tree
    # unlike in C++, no need to define the branches in advance
    for i, entry in enumerate(tree):
        if i>=actualNrEntries:
            continue
        if debug or i%1000==0:
            print "******* new entry",i," **********"
        # Obtaining Higgs mass and filling all the histograms in the dictionary
        for key in dictHist:
            Higgs_Opt_M = getHiggsMass(entry=entry, tName=key, debug=debug)
            dictHist[key].Fill(Higgs_Opt_M)
        # we store that in a histogram
        
    # done loop over all the entries in the tree
    outputfile.Write()
    
    outputfile.Close()
# done function
# execute
readTree()

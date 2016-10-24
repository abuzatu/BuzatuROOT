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
    print "We want to run run over",desiredNrEntries,"entries."

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
    # we create a file to store histograms
    outputfile=TFile(outputfileName,"RECREATE")
    hist_Higgs_Nominal_M=TH1F("Higgs_Nominal_M","Higgs_Nominal_M",40,48.5,168.5)
    # run over the entries of the tree
    # unlike in C++, no need to define the branches in advance
    for i, entry in enumerate(tree):
        if i>=actualNrEntries:
            continue
        if debug or i%1000==0:
            print "******* new entry",i," **********"
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
        b1_Nominal_Pt=getattr(entry,"b1_Nominal_Pt")
        b1_Nominal_Eta=getattr(entry,"b1_Nominal_Eta")
        b1_Nominal_Phi=getattr(entry,"b1_Nominal_Phi")
        b1_Nominal_E=getattr(entry,"b1_Nominal_E")
        if debug:
            print "b1_Nominal_Pt",b1_Nominal_Pt
            print "b1_Nominal_Eta",b1_Nominal_Eta
            print "b1_Nominal_Phi",b1_Nominal_Phi
            print "b1_Nominal_E",b1_Nominal_E
        b1_Nominal_tlv=TLorentzVector()
        b1_Nominal_tlv.SetPtEtaPhiE(b1_Nominal_Pt,b1_Nominal_Eta,b1_Nominal_Phi,b1_Nominal_E)
        b1_Nominal_M=b1_Nominal_tlv.M()
        if debug:
            print "b1_Nominal_M",b1_Nominal_M
        # jet 2
        b2_Nominal_Pt=getattr(entry,"b2_Nominal_Pt")
        b2_Nominal_Eta=getattr(entry,"b2_Nominal_Eta")
        b2_Nominal_Phi=getattr(entry,"b2_Nominal_Phi")
        b2_Nominal_E=getattr(entry,"b2_Nominal_E")
        if debug:
            print "b2_Nominal_Pt",b2_Nominal_Pt
            print "b2_Nominal_Eta",b2_Nominal_Eta
            print "b2_Nominal_Phi",b2_Nominal_Phi
            print "b2_Nominal_E",b2_Nominal_E
        b2_Nominal_tlv=TLorentzVector()
        b2_Nominal_tlv.SetPtEtaPhiE(b2_Nominal_Pt,b2_Nominal_Eta,b2_Nominal_Phi,b2_Nominal_E)
        b2_Nominal_M=b2_Nominal_tlv.M()
        if debug:
            print "b2_Nominal_M",b2_Nominal_M
        # Higgs boson candidate decaying to b1 and b2 
        # TLorentzVector is the sum of the two TLorentzVectors
        Higgs_Nominal_tlv=b1_Nominal_tlv+b2_Nominal_tlv
        Higgs_Nominal_Pt=Higgs_Nominal_tlv.Pt()
        Higgs_Nominal_Eta=Higgs_Nominal_tlv.Eta()
        Higgs_Nominal_Phi=Higgs_Nominal_tlv.Phi()
        Higgs_Nominal_E=Higgs_Nominal_tlv.E()
        if debug:
            print "Higgs_Nominal_Pt",Higgs_Nominal_Pt
            print "Higgs_Nominal_Eta",Higgs_Nominal_Eta
            print "Higgs_Nominal_Phi",Higgs_Nominal_Phi
            print "Higgs_Nominal_E",Higgs_Nominal_E
        Higgs_Nominal_M=Higgs_Nominal_tlv.M()
        if debug:
            print "Higgs_Nominal_M",Higgs_Nominal_M
        # the mass should be 125, but when measured we get a distribution around 125
        # we store that in a histogram
        hist_Higgs_Nominal_M.Fill(Higgs_Nominal_M)
    # done loop over all the entries in the tree
    outputfile.Write()
    outputfile.Close()
# done function


# execute
readTree()

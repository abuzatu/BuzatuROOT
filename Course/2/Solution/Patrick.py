#!/usr/bin/python

# python
import os,sys
import Bukin
# PyROOT
from ROOT import gROOT, TFile, TTree, TLorentzVector, TH1F, TCanvas, TList
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

def FillHisto(name,entry,histogram):
    #name Nominal 
        b1_tlv=GetTlv("b1_"+name,entry)
        b1_M=b1_tlv.M()
        if debug:
            print "b1_"+name+"_M",b1_M
        # jet 2
        b2_tlv=GetTlv("b2_"+name,entry)
        b2__M=b2_tlv.M()
        if debug:
            print "b2_"+name+"_M",b2_M
        # Higgs boson candidate decaying to b1 and b2 
        # TLorentzVector is the sum of the two TLorentzVectors
        Higgs_tlv=b1_tlv+b2_tlv
        Higgs_Pt=Higgs_tlv.Pt()
        Higgs_Eta=Higgs_tlv.Eta()
        Higgs_Phi=Higgs_tlv.Phi()
        Higgs_E=Higgs_tlv.E()
        if debug:
            print "Higgs_"+name+"_Pt",Higgs_Pt
            print "Higgs_"+name+"_Eta",Higgs_Eta
            print "Higgs_"+name+"_Phi",Higgs_Phi
            print "Higgs_"+name+"_E",Higgs_E
        Higgs_M=Higgs_tlv.M()
        if debug:
            print "Higgs_"+name+"_M",Higgs_M
        # the mass should be 125, but when measured we get a distribution around 125
        # we store that in a histogram
        #hist_Higgs_Nominal_M.Fill(Higgs_Nominal_M)
        histogram.Fill(Higgs_M)

def GetTlv(name,entry):
    #like "OneMu", "PtRecoBukin", "PtRecoGauss", "PtRecoAverageBukinAndGauss", "Parton". 
    #name b1_Nominal   
    Pt=getattr(entry,name+"_Pt")
    Eta=getattr(entry,name+"_Eta")
    Phi=getattr(entry,name+"_Phi")
    E=getattr(entry,name+"_E")
    if debug:
        print name+"_Pt",Pt
        print name+"_Eta",Eta
        print name+"_Phi",Phi
        print name+"_E",E
    tlv=TLorentzVector()
    tlv.SetPtEtaPhiE(Pt,Eta,Phi,E)
    return tlv

def readTree(histoMap,hList):
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
        for key, value in histoMap.iteritems():
            FillHisto(key,entry,value)

    # done loop over all the entries in the tree
    hList.Write()  
    #outputfile.Write()
    outputfile.Close()
# done function

# execute
hList = TList();
histoMap = {}
hist_Higgs_Nominal_M=TH1F("Higgs_Nominal_M","Higgs_Nominal_M",40,48.5,168.5)
histoMap['Nominal'] = hist_Higgs_Nominal_M
hList.Add(hist_Higgs_Nominal_M)
hist_Higgs_OneMu_M=TH1F("Higgs_OneMu_M","Higgs_OneMu_M",40,48.5,168.5)
histoMap['OneMu'] = hist_Higgs_OneMu_M
hList.Add(hist_Higgs_OneMu_M)
hist_Higgs_PtRecoBukin_M=TH1F("Higgs_PtRecoBukin_M","Higgs_PtRecoBukin_M",40,48.5,168.5)
histoMap['PtRecoBukin'] = hist_Higgs_PtRecoBukin_M
hList.Add(hist_Higgs_PtRecoBukin_M)
hist_Higgs_PtRecoGauss_M=TH1F("Higgs_PtRecoGauss_M","Higgs_PtRecoGauss_M",40,48.5,168.5)
histoMap['PtRecoGauss'] = hist_Higgs_PtRecoGauss_M
hList.Add(hist_Higgs_PtRecoGauss_M)
hist_Higgs_Regression_M=TH1F("Higgs_Regression_M","Higgs_Regression_M",40,48.5,168.5)
histoMap['Regression'] = hist_Higgs_Regression_M
hList.Add(hist_Higgs_Regression_M)
hist_Higgs_Parton_M=TH1F("Higgs_Parton_M","Higgs_Parton_M",40,48.5,168.5)
histoMap['Parton'] = hist_Higgs_Parton_M
hList.Add(hist_Higgs_Parton_M)

readTree(histoMap,hList)


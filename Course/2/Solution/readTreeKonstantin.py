#!/usr/bin/python

# python
import os,sys
# PyROOT
from ROOT import gROOT, TFile, TTree, TLorentzVector, TH1F
gROOT.SetBatch(True)

total = len(sys.argv)
# print(total)
# number of arguments plus 1
if total!=2:
    print("You need some arguments, will ABORT!")
    print("Ex: ./readTree.py NrEntries")
    print("Ex: ./readTree.py 100")
    print("Ex: ./readTree.py -1")
    assert(False)
# done if

NrEntries=sys.argv[1]
desiredNrEntries=int(NrEntries)

debug=False
fileName="./input/tree_llbb.root"
treeName="perevent"
outputfileName="./output/histo_llbb.root"


if debug:
    print("We want to run run over",desiredNrEntries,"entries.")

def readTree(fileName, outputfileName):
    # open file
    file=TFile(fileName,"READ")
    if not file.IsOpen():
        print("File",fileName,"does not exist. WILL ABORT!!!")
        assert(False)
    # open tree
    tree=file.Get(treeName)
    if tree==None:
        print ("tree",treeName,"doesn't exist in file",fileName,". WILL ABORT!!!")
        assert(False)
    # determine how many entries to run on
    nrEntries=tree.GetEntries()
    print("Number of Entries",nrEntries)
    if desiredNrEntries<0 or desiredNrEntries>nrEntries:
        actualNrEntries=nrEntries
    else:
        actualNrEntries=desiredNrEntries
    if debug:
        print("We will run over",actualNrEntries,"entries.")

    # we create a file to store histograms
    outputfile=TFile(outputfileName,"RECREATE")

    hist_Higgs_Nominal_M=TH1F("Higgs_Nominal_M","Higgs_Nominal_M",40,48.5,168.5)
    hist_Higgs_OneMu_M=TH1F("Higgs_OneMu_M","Higgs_OneMu_M",40,48.5,168.5)
    hist_Higgs_PtRecoGauss_M=TH1F("Higgs_PtRecoGauss_M","Higgs_PtRecoGauss_M",40,48.5,168.5)
    hist_Higgs_PtRecoBukin_M=TH1F("Higgs_PtRecoBukin_M","Higgs_PtRecoBukin_M",40,48.5,168.5)
    hist_Higgs_Parton_M=TH1F("Higgs_Parton_M","Higgs_Parton_M",40,48.5,168.5)
    hist_Higgs_AllMuNu_M=TH1F("Higgs_AllMuNu_M","Higgs_AllMuNu_M",40,48.5,168.5)
    hist_Higgs_TruthWZ_M=TH1F("Higgs_TruthWZ_M","Higgs_TruthWZ_M",40,48.5,168.5)
    hist_Higgs_AllMu_M=TH1F("Higgs_AllMu_M","Higgs_AllMu_M",40,48.5,168.5)
    hist_Higgs_Regression_M=TH1F("Higgs_Regression_M","Higgs_Regression_M",40,48.5,168.5)
    hist_Higgs_OneMuNu_M=TH1F("Higgs_OneMuNu_M","Higgs_OneMuNu_M",40,48.5,168.5)

    # run over the entries of the tree
    # unlike in C++, no need to define the branches in advance
    for i, entry in enumerate(tree):
        if i>=actualNrEntries:
            continue
        if debug or i%1000==0:
            print("******* new entry",i," **********")

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

        b1_OneMu_Pt=getattr(entry,"b1_OneMu_Pt")
        b1_OneMu_Eta=getattr(entry,"b1_OneMu_Eta")
        b1_OneMu_Phi=getattr(entry,"b1_OneMu_Phi")
        b1_OneMu_E=getattr(entry,"b1_OneMu_E")

        b1_PtRecoGauss_Pt=getattr(entry,"b1_PtRecoGauss_Pt")
        b1_PtRecoGauss_Eta=getattr(entry,"b1_PtRecoGauss_Eta")
        b1_PtRecoGauss_Phi=getattr(entry,"b1_PtRecoGauss_Phi")
        b1_PtRecoGauss_E=getattr(entry,"b1_PtRecoGauss_E")

        b1_PtRecoBukin_Pt=getattr(entry,"b1_PtRecoBukin_Pt")
        b1_PtRecoBukin_Eta=getattr(entry,"b1_PtRecoBukin_Eta")
        b1_PtRecoBukin_Phi=getattr(entry,"b1_PtRecoBukin_Phi")
        b1_PtRecoBukin_E=getattr(entry,"b1_PtRecoBukin_E")

        b1_Parton_Pt=getattr(entry,"b1_Parton_Pt")
        b1_Parton_Eta=getattr(entry,"b1_Parton_Eta")
        b1_Parton_Phi=getattr(entry,"b1_Parton_Phi")
        b1_Parton_E=getattr(entry,"b1_Parton_E")

        b1_AllMuNu_Pt=getattr(entry,"b1_AllMuNu_Pt")
        b1_AllMuNu_Eta=getattr(entry,"b1_AllMuNu_Eta")
        b1_AllMuNu_Phi=getattr(entry,"b1_AllMuNu_Phi")
        b1_AllMuNu_E=getattr(entry,"b1_AllMuNu_E")

        b1_TruthWZ_Pt=getattr(entry,"b1_TruthWZ_Pt")
        b1_TruthWZ_Eta=getattr(entry,"b1_TruthWZ_Eta")
        b1_TruthWZ_Phi=getattr(entry,"b1_TruthWZ_Phi")
        b1_TruthWZ_E=getattr(entry,"b1_TruthWZ_E")

        b1_AllMu_Pt=getattr(entry,"b1_AllMu_Pt")
        b1_AllMu_Eta=getattr(entry,"b1_AllMu_Eta")
        b1_AllMu_Phi=getattr(entry,"b1_AllMu_Phi")
        b1_AllMu_E=getattr(entry,"b1_AllMu_E")

        b1_Regression_Pt=getattr(entry,"b1_Regression_Pt")
        b1_Regression_Eta=getattr(entry,"b1_Regression_Eta")
        b1_Regression_Phi=getattr(entry,"b1_Regression_Phi")
        b1_Regression_E=getattr(entry,"b1_Regression_E")

        b1_OneMuNu_Pt=getattr(entry,"b1_OneMuNu_Pt")
        b1_OneMuNu_Eta=getattr(entry,"b1_OneMuNu_Eta")
        b1_OneMuNu_Phi=getattr(entry,"b1_OneMuNu_Phi")
        b1_OneMuNu_E=getattr(entry,"b1_OneMuNu_E")

        if debug:
            print("b1_Nominal_Pt",b1_Nominal_Pt)
            print("b1_Nominal_Eta",b1_Nominal_Eta)
            print("b1_Nominal_Phi",b1_Nominal_Phi)
            print("b1_Nominal_E",b1_Nominal_E)

        b1_Nominal_tlv=TLorentzVector()
        b1_Nominal_tlv.SetPtEtaPhiE(b1_Nominal_Pt,b1_Nominal_Eta,b1_Nominal_Phi,b1_Nominal_E)
        b1_Nominal_M=b1_Nominal_tlv.M()

        b1_OneMu_tlv=TLorentzVector()
        b1_OneMu_tlv.SetPtEtaPhiE(b1_OneMu_Pt,b1_OneMu_Eta,b1_OneMu_Phi,b1_OneMu_E)
        b1_OneMu_M=b1_OneMu_tlv.M()

        b1_PtRecoGauss_tlv=TLorentzVector()
        b1_PtRecoGauss_tlv.SetPtEtaPhiE(b1_PtRecoGauss_Pt,b1_PtRecoGauss_Eta,b1_PtRecoGauss_Phi,b1_PtRecoGauss_E)
        b1_PtRecoGauss_M=b1_PtRecoGauss_tlv.M()

        b1_PtRecoBukin_tlv=TLorentzVector()
        b1_PtRecoBukin_tlv.SetPtEtaPhiE(b1_PtRecoBukin_Pt,b1_PtRecoBukin_Eta,b1_PtRecoBukin_Phi,b1_PtRecoBukin_E)
        b1_PtRecoBukin_M=b1_PtRecoBukin_tlv.M()

        b1_Parton_tlv=TLorentzVector()
        b1_Parton_tlv.SetPtEtaPhiE(b1_Parton_Pt,b1_Parton_Eta,b1_Parton_Phi,b1_Parton_E)
        b1_Parton_M=b1_PtRecoGauss_tlv.M()

        b1_AllMuNu_tlv=TLorentzVector()
        b1_AllMuNu_tlv.SetPtEtaPhiE(b1_AllMuNu_Pt,b1_AllMuNu_Eta,b1_AllMuNu_Phi,b1_AllMuNu_E)
        b1_AllMuNu_M=b1_PtRecoGauss_tlv.M()

        b1_TruthWZ_tlv=TLorentzVector()
        b1_TruthWZ_tlv.SetPtEtaPhiE(b1_TruthWZ_Pt,b1_TruthWZ_Eta,b1_TruthWZ_Phi,b1_TruthWZ_E)
        b1_TruthWZ_M=b1_TruthWZ_tlv.M()

        b1_AllMu_tlv=TLorentzVector()
        b1_AllMu_tlv.SetPtEtaPhiE(b1_AllMu_Pt,b1_AllMu_Eta,b1_AllMu_Phi,b1_AllMu_E)
        b1_AllMu_M=b1_PtRecoGauss_tlv.M()

        b1_Regression_tlv=TLorentzVector()
        b1_Regression_tlv.SetPtEtaPhiE(b1_Regression_Pt,b1_Regression_Eta,b1_Regression_Phi,b1_Regression_E)
        b1_Regression_M=b1_PtRecoGauss_tlv.M()

        b1_OneMuNu_tlv=TLorentzVector()
        b1_OneMuNu_tlv.SetPtEtaPhiE(b1_OneMuNu_Pt,b1_OneMuNu_Eta,b1_OneMuNu_Phi,b1_OneMuNu_E)
        b1_OneMuNu_M=b1_PtRecoGauss_tlv.M()

        if debug:
            print("b1_Nominal_M",b1_Nominal_M)

        # jet 2
        b2_Nominal_Pt=getattr(entry,"b2_Nominal_Pt")
        b2_Nominal_Eta=getattr(entry,"b2_Nominal_Eta")
        b2_Nominal_Phi=getattr(entry,"b2_Nominal_Phi")
        b2_Nominal_E=getattr(entry,"b2_Nominal_E")

        b2_OneMu_Pt=getattr(entry,"b2_OneMu_Pt")
        b2_OneMu_Eta=getattr(entry,"b2_OneMu_Eta")
        b2_OneMu_Phi=getattr(entry,"b2_OneMu_Phi")
        b2_OneMu_E=getattr(entry,"b2_OneMu_E")

        b2_PtRecoGauss_Pt=getattr(entry,"b2_PtRecoGauss_Pt")
        b2_PtRecoGauss_Eta=getattr(entry,"b2_PtRecoGauss_Eta")
        b2_PtRecoGauss_Phi=getattr(entry,"b2_PtRecoGauss_Phi")
        b2_PtRecoGauss_E=getattr(entry,"b2_PtRecoGauss_E")

        b2_PtRecoBukin_Pt=getattr(entry,"b2_PtRecoBukin_Pt")
        b2_PtRecoBukin_Eta=getattr(entry,"b2_PtRecoBukin_Eta")
        b2_PtRecoBukin_Phi=getattr(entry,"b2_PtRecoBukin_Phi")
        b2_PtRecoBukin_E=getattr(entry,"b2_PtRecoBukin_E")

        b2_Parton_Pt=getattr(entry,"b2_Parton_Pt")
        b2_Parton_Eta=getattr(entry,"b2_Parton_Eta")
        b2_Parton_Phi=getattr(entry,"b2_Parton_Phi")
        b2_Parton_E=getattr(entry,"b2_Parton_E")

        b2_AllMuNu_Pt=getattr(entry,"b2_AllMuNu_Pt")
        b2_AllMuNu_Eta=getattr(entry,"b2_AllMuNu_Eta")
        b2_AllMuNu_Phi=getattr(entry,"b2_AllMuNu_Phi")
        b2_AllMuNu_E=getattr(entry,"b2_AllMuNu_E")

        b2_TruthWZ_Pt=getattr(entry,"b2_TruthWZ_Pt")
        b2_TruthWZ_Eta=getattr(entry,"b2_TruthWZ_Eta")
        b2_TruthWZ_Phi=getattr(entry,"b2_TruthWZ_Phi")
        b2_TruthWZ_E=getattr(entry,"b2_TruthWZ_E")

        b2_AllMu_Pt=getattr(entry,"b2_AllMu_Pt")
        b2_AllMu_Eta=getattr(entry,"b2_AllMu_Eta")
        b2_AllMu_Phi=getattr(entry,"b2_AllMu_Phi")
        b2_AllMu_E=getattr(entry,"b2_AllMu_E")

        b2_Regression_Pt=getattr(entry,"b2_Regression_Pt")
        b2_Regression_Eta=getattr(entry,"b2_Regression_Eta")
        b2_Regression_Phi=getattr(entry,"b2_Regression_Phi")
        b2_Regression_E=getattr(entry,"b2_Regression_E")

        b2_OneMuNu_Pt=getattr(entry,"b2_OneMuNu_Pt")
        b2_OneMuNu_Eta=getattr(entry,"b2_OneMuNu_Eta")
        b2_OneMuNu_Phi=getattr(entry,"b2_OneMuNu_Phi")
        b2_OneMuNu_E=getattr(entry,"b2_OneMuNu_E")

        if debug:
            print("b2_Nominal_Pt",b2_Nominal_Pt)
            print("b2_Nominal_Eta",b2_Nominal_Eta)
            print("b2_Nominal_Phi",b2_Nominal_Phi)
            print("b2_Nominal_E",b2_Nominal_E)

        b2_Nominal_tlv=TLorentzVector()
        b2_Nominal_tlv.SetPtEtaPhiE(b2_Nominal_Pt,b2_Nominal_Eta,b2_Nominal_Phi,b2_Nominal_E)
        b2_Nominal_M=b2_Nominal_tlv.M()

        b2_OneMu_tlv=TLorentzVector()
        b2_OneMu_tlv.SetPtEtaPhiE(b2_OneMu_Pt,b2_OneMu_Eta,b2_OneMu_Phi,b2_OneMu_E)
        b2_OneMu_M=b2_OneMu_tlv.M()

        b2_PtRecoGauss_tlv=TLorentzVector()
        b2_PtRecoGauss_tlv.SetPtEtaPhiE(b2_PtRecoGauss_Pt,b2_PtRecoGauss_Eta,b2_PtRecoGauss_Phi,b2_PtRecoGauss_E)
        b2_PtRecoGauss_M=b2_PtRecoGauss_tlv.M()

        b2_PtRecoBukin_tlv=TLorentzVector()
        b2_PtRecoBukin_tlv.SetPtEtaPhiE(b2_PtRecoBukin_Pt,b2_PtRecoBukin_Eta,b2_PtRecoBukin_Phi,b2_PtRecoBukin_E)
        b2_PtRecoBukin_M=b2_PtRecoBukin_tlv.M()

        b2_Parton_tlv=TLorentzVector()
        b2_Parton_tlv.SetPtEtaPhiE(b2_Parton_Pt,b2_Parton_Eta,b2_Parton_Phi,b2_Parton_E)
        b2_Parton_M=b2_PtRecoGauss_tlv.M()

        b2_AllMuNu_tlv=TLorentzVector()
        b2_AllMuNu_tlv.SetPtEtaPhiE(b2_AllMuNu_Pt,b2_AllMuNu_Eta,b2_AllMuNu_Phi,b2_AllMuNu_E)
        b2_AllMuNu_M=b2_PtRecoGauss_tlv.M()

        b2_TruthWZ_tlv=TLorentzVector()
        b2_TruthWZ_tlv.SetPtEtaPhiE(b2_TruthWZ_Pt,b2_TruthWZ_Eta,b2_TruthWZ_Phi,b2_TruthWZ_E)
        b2_TruthWZ_M=b2_TruthWZ_tlv.M()

        b2_AllMu_tlv=TLorentzVector()
        b2_AllMu_tlv.SetPtEtaPhiE(b2_AllMu_Pt,b2_AllMu_Eta,b2_AllMu_Phi,b2_AllMu_E)
        b2_AllMu_M=b2_PtRecoGauss_tlv.M()

        b2_Regression_tlv=TLorentzVector()
        b2_Regression_tlv.SetPtEtaPhiE(b2_Regression_Pt,b2_Regression_Eta,b2_Regression_Phi,b2_Regression_E)
        b2_Regression_M=b2_PtRecoGauss_tlv.M()

        b2_OneMuNu_tlv=TLorentzVector()
        b2_OneMuNu_tlv.SetPtEtaPhiE(b2_OneMuNu_Pt,b2_OneMuNu_Eta,b2_OneMuNu_Phi,b2_OneMuNu_E)
        b2_OneMuNu_M=b2_PtRecoGauss_tlv.M()

        if debug:
            print("b2_Nominal_M",b2_Nominal_M)
        # Higgs boson candidate decaying to b1 and b2
        # TLorentzVector is the sum of the two TLorentzVectors
        Higgs_Nominal_tlv=b1_Nominal_tlv+b2_Nominal_tlv
        Higgs_Nominal_Pt=Higgs_Nominal_tlv.Pt()
        Higgs_Nominal_Eta=Higgs_Nominal_tlv.Eta()
        Higgs_Nominal_Phi=Higgs_Nominal_tlv.Phi()
        Higgs_Nominal_E=Higgs_Nominal_tlv.E()
        Higgs_OneMu_tlv=b1_OneMu_tlv+b2_OneMu_tlv
        Higgs_OneMu_Pt=Higgs_OneMu_tlv.Pt()
        Higgs_OneMu_Eta=Higgs_OneMu_tlv.Eta()
        Higgs_OneMu_Phi=Higgs_OneMu_tlv.Phi()
        Higgs_OneMu_E=Higgs_OneMu_tlv.E()

        Higgs_PtRecoGauss_tlv=b1_PtRecoGauss_tlv+b2_PtRecoGauss_tlv
        Higgs_PtRecoBukin_tlv=b1_PtRecoBukin_tlv+b2_PtRecoBukin_tlv
        Higgs_Parton_tlv=b1_Parton_tlv+b2_Parton_tlv
        Higgs_AllMuNu_tlv=b1_AllMuNu_tlv+b2_AllMuNu_tlv
        Higgs_TruthWZ_tlv=b1_TruthWZ_tlv+b2_TruthWZ_tlv
        Higgs_AllMu_tlv=b1_AllMu_tlv+b2_AllMu_tlv
        Higgs_Regression_tlv=b1_Regression_tlv+b2_Regression_tlv
        Higgs_OneMuNu_tlv=b1_OneMuNu_tlv+b2_OneMuNu_tlv

        if debug:
            print("Higgs_Nominal_Pt",Higgs_Nominal_Pt)
            print("Higgs_Nominal_Eta",Higgs_Nominal_Eta)
            print("Higgs_Nominal_Phi",Higgs_Nominal_Phi)
            print("Higgs_Nominal_E",Higgs_Nominal_E)
        Higgs_Nominal_M=Higgs_Nominal_tlv.M()
        Higgs_OneMu_M=Higgs_OneMu_tlv.M()
        Higgs_PtRecoGauss_M=Higgs_PtRecoGauss_tlv.M()
        Higgs_PtRecoBukin_M=Higgs_PtRecoBukin_tlv.M()
        Higgs_Parton_M=Higgs_Parton_tlv.M()
        Higgs_AllMuNu_M=Higgs_AllMuNu_tlv.M()
        Higgs_TruthWZ_M=Higgs_TruthWZ_tlv.M()
        Higgs_AllMu_M=Higgs_AllMu_tlv.M()
        Higgs_Regression_M=Higgs_Regression_tlv.M()
        Higgs_OneMuNu_M=Higgs_OneMuNu_tlv.M()
        if debug:
            print("Higgs_Nominal_M",Higgs_Nominal_M)
        # the mass should be 125, but when measured we get a distribution around 125
        # we store that in a histogram
        hist_Higgs_Nominal_M.Fill(Higgs_Nominal_M)
        hist_Higgs_OneMu_M.Fill(Higgs_OneMu_M)
        hist_Higgs_PtRecoGauss_M.Fill(Higgs_PtRecoGauss_M)
        hist_Higgs_PtRecoBukin_M.Fill(Higgs_PtRecoBukin_M)
        hist_Higgs_Parton_M.Fill(Higgs_Parton_M)
        hist_Higgs_AllMuNu_M.Fill(Higgs_AllMuNu_M)
        hist_Higgs_TruthWZ_M.Fill(Higgs_TruthWZ_M)
        hist_Higgs_AllMu_M.Fill(Higgs_AllMu_M)
        hist_Higgs_Regression_M.Fill(Higgs_Regression_M)
        hist_Higgs_OneMuNu_M.Fill(Higgs_OneMuNu_M)
    # done loop over all the entries in the tree
    outputfile.Write()
    outputfile.Close()
# done function


# execute
readTree(fileName, outputfileName)

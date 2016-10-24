#!/usr/bin/python

# python
import os,sys
# PyROOT
from ROOT import gROOT, TFile, TTree, TLorentzVector, TH1F, TF1, THStack, TLegend

gROOT.SetBatch(True)

from Bukin import Gauss, Bukin

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

scalesstring="Parton,Nominal,OneMu,OneMuNu,AllMu,AllMuNu,PtRecoGauss,PtRecoBukin,Regression"
list_scale=scalesstring.split(",")


if debug:
    print scalesstring
    print list_scale

def get_dict_scale_hist(list_scale,debug):    
    dict_scale_hist={}
    for scale in list_scale:
        print scale, type(scale)
        histname="Higgs_"+scale+"_M"
        dict_scale_hist[scale]=TH1F(histname,histname,40,48.5,168.5)
        dict_scale_hist[scale].GetXaxis().SetTitle("mbb [GeV]")
        dict_scale_hist[scale].GetYaxis().SetTitle("Arbitrary units")
        dict_scale_hist[scale].SetMinimum(0)
        dict_scale_hist[scale].SetMaximum(4000)
        print type(dict_scale_hist[scale])
    if debug:
        print dict_scale_hist
    return dict_scale_hist
# done function


def get_tlv(entry,b,scale,debug):
    if debug:
        print "get_tlv() for b",b," for scale",scale
    # jet 1
    prefix=b+"_"+scale+"_"
    Pt=getattr(entry,prefix+"Pt")
    Eta=getattr(entry,prefix+"Eta")
    Phi=getattr(entry,prefix+"Phi")
    E=getattr(entry,prefix+"E")
    if debug:
        print "Pt",Pt
        print "Eta",Eta
        print "Phi",Phi
        print "E",E
    tlv=TLorentzVector()
    tlv.SetPtEtaPhiE(Pt,Eta,Phi,E)
    M=tlv.M()
    if debug:
        print "M",M
    return tlv

def get_M(entry,scale,debug):
    if debug:
        print "get_M() for scale",scale
    tlv1=get_tlv(entry,"b1",scale,debug)
    tlv2=get_tlv(entry,"b2",scale,debug)
    # Higgs boson candidate decaying to b1 and b2 
    # TLorentzVector is the sum of the two TLorentzVectors
    tlv=tlv1+tlv2
    Pt=tlv.Pt()
    Eta=tlv.Eta()
    Phi=tlv.Phi()
    E=tlv.E()
    if debug:
        print "Pt",Pt
        print "Eta",Eta
        print "Phi",Phi
        print "E",E
    M=tlv.M()
    if debug:
        print "M",M 
    return M
        
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
    dict_scale_hist=get_dict_scale_hist(list_scale,debug)
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
        

        for scale in list_scale:
            M=get_M(entry,scale,debug)
            dict_scale_hist[scale].Fill(M)
            #dict_scale_hist[scale].Fit("gaus")
    
    # done loop over all the entries in the tree
    
    #Gaussian = TF1 ("Gauss",Gauss(),48.5,168.5,3)
    
    Bukins = TF1 ("Bukin",Bukin(),48.5,168.5,6)
    Bukins.SetLineColor(3)

    #Stack = THStack ("Stack", "Stacked Histograms")

    #Leg = TLegend (x1,y1,x2,y2)
    

    for scale in list_scale:
        #Gaussian.SetParameters(80,dict_scale_hist[scale].GetMean(),dict_scale_hist[scale].GetRMS())
        #dict_scale_hist[scale].Fit(Gaussian,"+")

        Bukins.SetParameters(80,dict_scale_hist[scale].GetMean(),dict_scale_hist[scale].GetRMS(),0,0,0)
        dict_scale_hist[scale].Fit(Bukins,"+")
        
        #Stack.Add(dict_scale_hist[scale])

    #Stack.Draw("option")
    
    #Leg.Draw()

        
    outputfile.Write()
    outputfile.Close()
# done function


# execute
readTree()

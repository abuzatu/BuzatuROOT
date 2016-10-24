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

def jet(entry,jetid,calibid):
    Pt=getattr(entry,"%s_%s_Pt" %(jetid,calibid))
    Eta=getattr(entry,"%s_%s_Eta" %(jetid,calibid))
    Phi=getattr(entry,"%s_%s_Phi" %(jetid,calibid))
    E=getattr(entry,"%s_%s_E" %(jetid,calibid))
    if debug:
        print "%s_%s_Pt",Pt %(jetid,calibid)
        print "%s_%s_Eta",Eta %(jetid,calibid)
        print "%s_%s_Phi",Phi %(jetid,calibid)
        print "%s_%s_E",E %(jetid,calibid)
    tlv=TLorentzVector()
    tlv.SetPtEtaPhiE(Pt,Eta,Phi,E)
    M=tlv.M()
    if debug:
       print "%s_%s_M",M %(jetid,calibid)
    return tlv,M
#end jet function

def readTreeSL(entry,calibid,debug): #plot as input

    # run over the entries of the tree
    # unlike in C++, no need to define the branches in advance

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
    b1_tlv,b1_M = jet(entry,"b1",calibid)
    # jet 2
    b2_tlv,b2_M = jet(entry,"b2",calibid)

    # Higgs boson candidate decaying to b1 and b2 
    # TLorentzVector is the sum of the two TLorentzVectors
    Higgs_tlv=b1_tlv+b2_tlv
    Higgs_Pt=Higgs_tlv.Pt()
    Higgs_Eta=Higgs_tlv.Eta()
    Higgs_Phi=Higgs_tlv.Phi()
    Higgs_E=Higgs_tlv.E()
    if debug:
        print "Higgs_%s_Pt" %calibid,Higgs_Pt
        print "Higgs_%s_Eta" %calibid,Higgs_Eta
        print "Higgs_%s_Phi" %calibid,Higgs_Phi
        print "Higgs_%s_E" %calibid,Higgs_E

    Higgs_M=Higgs_tlv.M()
    if debug:
        print "Higgs_%s_M" %calibid,Higgs_M

    # done loop over all the entries in the tree
    return Higgs_M
# done function

def Histograms(scalestring):
   # we create a file to store histograms
   outputfile=TFile(outputfileName,"RECREATE")

   list_scale = scalestring.split(",")

   dict_scale_hist= {}
   for scale in list_scale:
       histname = "Higgs_"+scale+"_M"
       dict_scale_hist[scale] = TH1F(histname,histname,40,48.5,168.5)
       dict_scale_hist[scale].GetXaxis().SetTitle("Energy")
       dict_scale_hist[scale].GetYaxis().SetTitle("Counts")

       if scale=="Parton":
            dict_scale_hist[scale].GetYaxis().SetRangeUser(0,105)
       else:
            dict_scale_hist[scale].GetYaxis().SetRangeUser(0,15)  # Stops Bukin fit making scale very large

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

   M = []
   for i, entry in enumerate(tree):
       if i>=actualNrEntries:
           continue
       if debug or i%1000==0:
          print
          print "******* new entry",i," **********"
       for scale in list_scale:
           if debug or i%1000==0:
               print "****************************************************************"
               print "The current calibration is: ", scale
           M.append(1)
           M[i] = readTreeSL(entry,scale,debug)

  # for i in range(0,desiredNrEntries):
           dict_scale_hist[scale].Fill(M[i])
       #endfill
   #endloops

   outputfile.Write()
   outputfile.Close()
#end function


# execute
scalestring = "Nominal,OneMu,OneMuNu,AllMu,AllMuNu,PtRecoBukin,PtRecoGauss,Regression,Parton"

Histograms(scalestring)

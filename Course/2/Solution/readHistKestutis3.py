#!/usr/bin/python

# Kestutis Kanisauskas @ University of Glasgow

# python
import os,sys
# PyROOT
from ROOT import gROOT, gStyle, TFile, TTree, TH1F, TF1, TCanvas, TPaveText, TLegend, TLatex, THStack
from __builtin__ import True
gROOT.SetBatch(True)
# Fitting functions
from Bukin import Gauss, Bukin
total = len(sys.argv)
#Options: "histo,fit,histo+fit"
if total!=2:
    print "Plotting option(-s) were not chosen. The script will be using the default 'histo' option!"
    print "When calling the script one can select single or any combination of the options 'histo', 'fit', 'histo+fit',"
    print "Ex: ./Hist_Fit.py histo"
    print "Ex: ./Hist_Fit.py histo,histo+fit"
    print "Ex: ./Hist_Fit.py histo,fit,histo+fit"
    options = ["histo"]
else: 
    options = sys.argv[1].split(',')
    print 'Options Received: ', options

fileName="./output/histo_llbb.root"
autoPlot = False #If true all the histograms existing within root file are plotted with the provided option, otherwise only histograms with corrections from the specific list are plotted
corrList = ["Nominal","OneMu","PtRecoBukin","PtRecoGauss", "Regression"]

   
def ratio(s,b,debug=False):
  if debug:
    print "s",s,"b",b
  if -0.0001<b<0.0001:
    result=0
  else:
    result=s/b
  return result
# done function

# the functions above can be replaced by just one function that takes an argument of what the user wants


def getHistNames(r_file):
    histNames = []
    f_list=r_file.GetListOfKeys()
    for i in range(f_list.GetSize()):
        obj = f_list.At(i)
        histNames.append(obj.GetName())
    return histNames

def setBukin(mean,rms,height,xmin,xmax):
    # create a function from a user defined class in a given range with 6 parameters
    # we choose the range to be related to the histogram values
    function=TF1("bukin",Bukin(),xmin,xmax,6)
    # give name to parameters
    function.SetParName(0,"height")
    function.SetParName(1,"mean") # actually the peak, as it may be asymmetric
    function.SetParName(2,"width")
    function.SetParName(3,"asymmetry")
    function.SetParName(4,"size of lower tail")
    function.SetParName(5,"size of higher tail")

    # set initial values to parameters
    # we can set to all of them, but the crucial ones are height, mean and width
    # if your fits fail, you can change the initialisations of these parameters
    function.SetParameter(0,height)
    function.SetParameter(1,mean)
    function.SetParameter(2,rms)
    #function.SetParameter(3,-0.4)
    #function.SetParameter(4,0.01)
    #function.SetParameter(5,0.005)
    
    return function
    

def plot(dictHist,option):
    c=TCanvas("c","c",600,300)
    legend=TLegend(0.12,0.18,0.35,0.85)
    legend.AddEntry(None,"#bf{mean[GeV] / sigma[GeV] / ratio}","")
    color = 1
    hs = THStack("hs","corrections;mbb [GeV];Number of events;")
    drawOption = "" #Draw Option for THStack
    for key in dictHist:
        hist = dictHist[key].Clone()
        hist.SetLineColor(color) # Setting color for the histogram
        print 'Current Hist Title: ',hist.GetTitle()
        print 'Color Option: ',color
        entries=hist.GetEntries()
        height=hist.GetMaximum()
        mean=hist.GetMean()
        rms=hist.GetRMS()
        
        xmin=mean-3*rms
        xmax=mean+3*rms 
        #Getting Bukin Function
        f = setBukin(mean=mean, rms=rms, height=height, xmin=xmin, xmax=xmax)
        
        ########### start code specific to the histo and/or fit choice ##################
        if option=="histo":
            hs.Add(hist)
            result=(height,mean,rms)
            drawOption = "nostack"
        elif option=="histo+fit":
            hist.Fit("bukin","RQ","HISTS",xmin,xmax)
            f=hist.GetFunction("bukin")
            result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2),f.GetParameter(3),f.GetParameter(4),f.GetParameter(5))
            f.SetLineColor(color)
            hs.Add(hist)
            drawOption = "nostack"
        elif option=="fit":
            hist.Fit("bukin","RQ","RO",xmin,xmax)
            f=hist.GetFunction("bukin")
            result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2),f.GetParameter(3),f.GetParameter(4),f.GetParameter(5))
            f.SetLineColor(color)
            hs.Add(hist)
            drawOption = "nostackRO"
        else:
            print "option",option,"not known"
            assert(False)
        ########## end   code specific to the histo and/or fit choice ##################
        # https://root.cern.ch/doc/master/classTLegend.html     
        legend.AddEntry(hist,hist.GetName(),"f")
        legend_text="#bf{%-.3f/%-.3f/%-.3f}" % (result[1],result[2],ratio(result[2],result[1]))
        legend.AddEntry(None,legend_text,"")
        c.Update()
        
        color += 1
        if (color == 10): #10 would not be visible
            color = 11 

    hs.Draw(drawOption)    
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.025)
    legend.SetTextColor(1)
    legend.Draw('Same')
    # https://root.cern.ch/doc/master/classTLatex.html#L3
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(10)
    t.SetTextFont(43)
    t.SetTextAlign(13)
    t.DrawLatex(0.7,0.85,"#it{#bf{ATLAS} Simulation Internal}")
    t.Draw("Same")        
    
    c.Print("Higgs_"+option+".pdf")
    
def Hist_Fit():
    
    file=TFile(fileName,"READ")
    
    histNames = [] #Will be filled depending on the option provided
    if (autoPlot == True):
        histNames = getHistNames(r_file=file) # List of all the histogram names in the file
    else: 
        for corr in corrList:
            histNames.append("Higgs_"+corr+"_M")
            
        
    # Building dictionary of histograms
    dictHist = {}
    for histoName in histNames:     
        dictHist[histoName] = file.Get(histoName)
    # Set up canvas, remove titles and stats boxes
    gStyle.SetOptTitle(0)
    gStyle.SetOptStat(0)
    for option in options:
        print "option",option
        plot(dictHist=dictHist,option=option)    
    return

Hist_Fit()


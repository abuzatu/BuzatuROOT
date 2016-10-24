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
if total!=3:
    print "Plotting parameters were not provided!"
    print "When calling the script one has to provide two parameters i.e. single or any combination of the plotting options 'histo', 'fit', 'histo+fit' and name of the fit function."
    print "The fit function choice can be either 'gauss' or 'bukin'"
    print "Ex: ./Hist_Fit.py histo gauss"
    print "Ex: ./Hist_Fit.py histo,histo+fit bukin"
    print "Ex: ./Hist_Fit.py histo,fit,histo+fit gauss"
    assert(False)
else: 
    options = sys.argv[1].split(',')
    fitFunction = sys.argv[2].strip() #In case of the whitespace after function name 
    print 'Plotting Options Received:', options
    print 'Fit function:', fitFunction

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

def setGauss(mean,rms,height,xmin,xmax):

    function=TF1('gauss',Gauss(),xmin,xmax,3)

    function.SetParName(0,"height")
    function.SetParName(1,"mean")
    function.SetParName(2,"width")

    function.SetParameter(0,height)
    function.SetParameter(1,mean)
    function.SetParameter(2,rms)

    return function
    

def plot(dictHist,option,fitFunction):
    c=TCanvas("c","c",600,300)
    legend=TLegend(0.12,0.18,0.35,0.85)
    fNamePart = "" #Determines name of the output file
    legend.AddEntry(None,"#bf{mean[GeV] / sigma[GeV] / ratio}","")
    color = 1
    hs = THStack("hs","corrections;mbb [GeV];Number of events;")
    drawOption = "" #Draw Option for THStack
    for key in dictHist:
        hist = dictHist[key].Clone()
        hist.SetLineColor(color) # Setting color for the histogram
#         print 'Current Hist Title: ',hist.GetTitle()
#         print 'Color Option: ',color
        entries=hist.GetEntries()
        height=hist.GetMaximum()
        mean=hist.GetMean()
        rms=hist.GetRMS()
        
        xmin=mean-3*rms
        xmax=mean+3*rms 
        #Getting Function of Choice
        if (fitFunction == 'gauss'):
            f = setGauss(mean=mean, rms=rms, height=height, xmin=xmin, xmax=xmax)
        elif (fitFunction == 'bukin'):
            f = setBukin(mean=mean, rms=rms, height=height, xmin=xmin, xmax=xmax)
        else:
            print "Name of the function was not recognized! Selection can be either 'gauss' or 'bukin'."
            assert(False)
                
        ########### start code specific to the histo and/or fit choice ##################
        if option=="histo":
            hs.Add(hist)
            result=(height,mean,rms)
            drawOption = "nostack"
            fNamePart = option
        elif option=="histo+fit":
            hist.Fit(fitFunction,"RQ","HISTS",xmin,xmax)
            f=hist.GetFunction(fitFunction)
            if (fitFunction == 'gauss'):  
                result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2))
            else:
                result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2),f.GetParameter(3),f.GetParameter(4),f.GetParameter(5))
            f.SetLineColor(color)
            hs.Add(hist)
            drawOption = "nostack"
            fNamePart = "histo+" + fitFunction
        elif option=="fit":
            hist.Fit(fitFunction,"RQ","RO",xmin,xmax)
            f=hist.GetFunction(fitFunction)
            if (fitFunction == 'gauss'):  
                result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2))
            else:
                result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2),f.GetParameter(3),f.GetParameter(4),f.GetParameter(5))
            f.SetLineColor(color)
            hs.Add(hist)
            drawOption = "nostackRO"
            fNamePart = fitFunction
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

    c.Print("Higgs_"+fNamePart+".pdf")
    
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
#       print "Current option: ",option
        plot(dictHist=dictHist,option=option,fitFunction=fitFunction)    
    return

Hist_Fit()


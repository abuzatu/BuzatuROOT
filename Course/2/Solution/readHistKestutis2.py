#!/usr/bin/python

# Kestutis Kanisauskas @ University of Glasgow

# python
import os,sys
# PyROOT
from ROOT import gROOT, gStyle, TFile, TTree, TH1F, TF1, TCanvas, TPaveText, TLegend, TLatex
gROOT.SetBatch(True)
# Fitting functions
from Bukin import Gauss, Bukin
total = len(sys.argv)
#Options: "histo,fit,histo+fit"
if total!=2:
    print "Plotting option(-s) were not chosen. The script will be using the default 'histo' option!"
    print "When calling the script one can select single or any combination of the options 'histo', 'fit', 'histo+fit',"
    print "Ex: ./Hist_Fit_Bukin.py histo"
    print "Ex: ./Hist_Fit_Bukin.py histo,histo+fit"
    print "Ex: ./Hist_Fit_Bukin.py histo,fit,histo+fit"
    options = ["histo"]
else: 
    options = sys.argv[1].split(',')
    print 'Options Received: ', options

fileName="./output/histo_llbb.root"
   
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
    

def plot(h,option,histoName):
    
    entries=h.GetEntries()
    height=h.GetMaximum()
    mean=h.GetMean()
    rms=h.GetRMS()
    color=h.GetLineColor()
    xmin=mean-3*rms
    xmax=mean+3*rms 
    #Getting Bukin Function
    f = setBukin(mean=mean, rms=rms, height=height, xmin=xmin, xmax=xmax)
    
    c=TCanvas("c","c",600,300)
    h.SetXTitle("mbb [GeV]")
    h.SetYTitle("Number of events")
    ########### start code specific to the histo and/or fit choice ##################
    if option=="histo":
        h.Draw("HIST")
    elif option=="histo+fit":
        h.Fit("bukin","RQ","HIST",xmin,xmax)
        f=h.GetFunction("bukin")
        result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2),f.GetParameter(3),f.GetParameter(4),f.GetParameter(5))
        f.SetLineColor(color)
        f.Draw("same")
    elif option=="fit":
        h.Fit("bukin","RQ","RO",xmin,xmax)
        f=h.GetFunction("bukin")
        result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2),f.GetParameter(3),f.GetParameter(4),f.GetParameter(5))
        f.SetLineColor(color)
    else:
        print "option",option,"not known"
        assert(False)
    ########## end   code specific to the histo and/or fit choice ##################
    # https://root.cern.ch/doc/master/classTLegend.html
    legend=TLegend(0.15,0.60,0.50,0.80)
    legend.AddEntry(None,"#bf{mean[GeV] / sigma[GeV] / ratio}","")
    legend.AddEntry(h,h.GetName(),"f")
    result=(height,mean,rms)
    legend_text="#bf{%-.3f/%-.3f/%-.3f}" % (result[1],result[2],ratio(result[2],result[1]))
    legend.AddEntry(None,legend_text,"")
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.03)
    legend.SetTextColor(color)
    legend.Draw("SAME")
    # https://root.cern.ch/doc/master/classTLatex.html#L3
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(10)
    t.SetTextFont(43)
    t.SetTextAlign(13)
    t.DrawLatex(0.15,0.40,"#it{#bf{ATLAS} Simulation Internal}")
    t.Draw("same")
    # save the canvas to file
    c.Print(histoName+"_"+option+".pdf")
    
def Hist_Fit_Bukin():
    
    file=TFile(fileName,"READ")
    histNames = getHistNames(r_file=file) # List of all the histogram names in the file
    
    for histoName in histNames:     
        h=file.Get(histoName)
        # Set up canvas, remove titles and stats boxes
        gStyle.SetOptTitle(0)
        gStyle.SetOptStat(0)
        for option in options:
            print "option",option
            plot(h.Clone(),option,histoName)
    return

Hist_Fit_Bukin()


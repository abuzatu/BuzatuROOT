#!/usr/bin/python
import math
# python
import os,sys
# PyROOT
from ROOT import gROOT, gStyle, TFile, TTree, TH1F, TF1, TCanvas, TPaveText, TLegend, TLatex
gROOT.SetBatch(True)
# Fitting functions
from Bukin import Gauss, Bukin



total = len(sys.argv)
# number of arguments plus 1
if total < 4:
    print "You need some arguments, will ABORT!"
    print "Ex: ./file.py plotType fitType Calibration1 Calibration2 ... etc "
    print "Ex: ./readTree.py histo+fit Gauss Regression Nominal"
    print "plotType options =histo, fit, histo+fit; fitType options = Gauss, Bukin; Calibration options: Nominal, OneMu, PtRecoBukin, PtRecoGauss, Regression, OneMuNu, AllMu, AllMuNu "
    assert(False)
# done if

plotType =sys.argv[1]  
fitType =sys.argv[2]  


#the file we will be taking the histograms from to fit 
fileName="./output/histo_llbbtest.root"
file=TFile(fileName,"READ")

#set up array to hold temporary clones as they will go out of scope in functions before we save to file
myListHisto = []
myListFit = []
myListHistoandFit = []
myListLegend = []


# Set up canvas, remove titles and stats boxes
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

 
outputfilename = plotType + "_Higgs_M_" 
c =TCanvas("c","c",600,300)




def CalibChoice(calib,i):

    histoName = "Higgs_" + calib + "_M"
    h=file.Get(histoName)
    entries=h.GetEntries()
    height=h.GetMaximum()
    mean=h.GetMean()
    rms=h.GetRMS()
    color=h.GetLineColor()
    #f=TF1()
    xmin=mean-3*rms
    xmax=mean+3*rms

    if  fitType == "Bukin" :
	function=TF1("bukin",Bukin(),xmin,xmax,6)
    	function.SetParName(0,"height")
    	function.SetParName(1,"mean") # actually the peak, as it may be asymmetric
    	function.SetParName(2,"width")
    	function.SetParName(3,"asymmetry")
    	function.SetParName(4,"size of lower tail")
    	function.SetParName(5,"size of higher tail")

    	function.SetParameter(0,height)
    	function.SetParameter(1,mean)
    	function.SetParameter(2,rms)
    	#function.SetParameter(3,-0.4)
    	#function.SetParameter(4,0.01)
    	#function.SetParameter(5,0.005)
    elif fitType == "Gauss" :
	function = TF1("gauss", Gauss(),xmax,xmin,3) 
	function.SetParName(0,"height") #height of peak
	function.SetParName(1,"mean") #centre of peak position
	function.SetParName(2,"width") # Gaussian Rms width should not be zero
	function.SetParameter(0,height)
    	function.SetParameter(1,mean)
    	function.SetParameter(2,rms)
    else:
	print " You did not enter a correct fit type. A fit Type is required even if you do not want to plot a fit. Please select from Gauss or Bukin. "
    
    if plotType == "histo":
	plot_histo(h.Clone(), height, mean, rms, color, calib,i) 
    elif plotType == "histo+fit":
	plot_histo_and_fit(h.Clone(), xmin, xmax, color, height, mean, rms,calib,i) 
    elif plotType == "fit":
	plot_fit(h.Clone(), xmin, xmax, color, height, mean, rms,calib,i) 
    else:
	print " You entered an incorrect type of plot. Please select from histo, histo+fit and fit. "

   
def ratio(s,b,debug=False):
  if debug:
    print "s",s,"b",b
  if -0.0001<b<0.0001:
    result=0
  else:
    result=s/b
  return result
# done function

def plot_histo(h, height, mean, rms, color, calib,i):
    
    h.SetXTitle("mbb [GeV]")
    h.SetYTitle("Number of events")
    h.Draw("HIST SAME")
    h.SetMaximum(4500)
    h.SetLineColor(i-2);
    # https://root.cern.ch/doc/master/classTLegend.html
    legend.AddEntry(h,h.GetName(),"f")
    result=(height,mean,rms)
    legend_text="#bf{%-.3f/%-.3f/%-.3f}" % (result[1],result[2],ratio(result[2],result[1]))
    legend.AddEntry(None,legend_text,"")
    legend.SetBorderSize(0)
    legend.SetTextFont(22)
    legend.SetTextSize(0.03)
    legend.SetTextColor(color)
    legend.Draw("SAME")
    # https://root.cern.ch/doc/master/classTLatex.html#L3
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(6)
    t.SetTextFont(22)
    t.SetTextAlign(13)
    t.DrawLatex(0.75,0.80,"#it{#bf{ATLAS} Simulation Internal}")
    t.Draw("same")
    myListHisto.append(h)
    
# done

def plot_histo_and_fit(h, xmin, xmax, color, height, mean, rms,calib,i):
    
    h.SetXTitle("mbb [GeV]")
    h.SetYTitle("Number of events")
    h.Draw("HIST SAME")
    if fitType == "Bukin":
	h.Fit("bukin","RQ","HIST SAME",xmin,xmax)     #R is use range specified in function and Q is quiet i.e min printing
	f=h.GetFunction("bukin")
	result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2),f.GetParameter(3),f.GetParameter(4),f.GetParameter(5))
    	f.Draw("HIST SAME")
    elif fitType == "Gauss":
	h.Fit("gauss", "RQ", "HIST SAME", xmin,xmax)
	f = h.GetFunction("gauss")
	result = (f.GetParameter(0),f.GetParameter(1),f.GetParameter(2))
    	f.Draw("same")
	
    else:
	print " You entered an incorrect type of fit. Use either Gauss or Bukin (case sensitive) "
    # https://root.cern.ch/doc/master/classTLegend.html
    h.SetMaximum(4500)
    f.SetLineColor(i-2)
    h.SetLineColor(i-2)
    legend.AddEntry(h,h.GetName(),"f")
    result=(height,mean,rms)
    legend_text="#bf{%-.3f/%-.3f/%-.3f}" % (result[1],result[2],ratio(result[2],result[1]))
    legend.AddEntry(None,legend_text,"")
    legend.SetBorderSize(0)
    legend.SetTextFont(22)
    legend.SetTextSize(0.03)
    legend.SetTextColor(color)
    legend.Draw("SAME")
    # https://root.cern.ch/doc/master/classTLatex.html#L3
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(6)
    t.SetTextFont(22)
    t.SetTextAlign(13)
    t.DrawLatex(0.15,0.40,"#it{#bf{ATLAS} Simulation Internal}")
    t.Draw("same")
    myListHisto.append(h)
    
# done

def plot_fit(h, xmin, xmax, color, height, mean, rms,calib,i):
    
    h.SetXTitle("mbb [GeV]")
    h.SetYTitle("Number of events")
   
    if fitType == "Bukin":
    	h.Fit("bukin","RQ","RO SAME",xmin,xmax)
    	f=h.GetFunction("bukin")
    	result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2),f.GetParameter(3),f.GetParameter(4),f.GetParameter(5))
    	
    elif fitType == "Gauss":
	h.Fit("gauss","RQ","RO SAME",xmin,xmax) 

    	f=h.GetFunction("gauss")
    	result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2))
	
    else:
	print " You entered an incorrect type of fit. Use either Gauss or Bukin (case sensitive) "
    # https://root.cern.ch/doc/master/classTLegend.html
    h.SetMaximum(4500)
    f.SetLineColor(i-2)
    h.SetLineColor(i-2)
    legend.AddEntry(h,h.GetName(),"f")
    result=(height,mean,rms)
    legend_text="#bf{%-.3f/%-.3f/%-.3f}" % (result[1],result[2],ratio(result[2],result[1]))
    legend.AddEntry(None,legend_text,"")
    legend.SetBorderSize(0)
    legend.SetTextFont(22)
    legend.SetTextSize(0.03)
    legend.SetTextColor(color)
    legend.Draw("SAME")
    # https://root.cern.ch/doc/master/classTLatex.html#L3
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(6)
    t.SetTextFont(22)
    t.SetTextAlign(13)
    t.DrawLatex(0.15,0.40,"#it{#bf{ATLAS} Simulation Internal}")
    t.Draw("same")
    myListFit.append(h)	    
# done






legend=TLegend(0.15,0.30,0.30,0.80)
legend.AddEntry(None,"#bf{mean[GeV] / sigma[GeV] / ratio}","")

for i in range(3, total):
	choice = sys.argv[i] 
	CalibChoice(choice,i)
	outputfilename += "_"+choice


outputfilename += "_" + fitType + ".pdf"
c.Print(outputfilename)



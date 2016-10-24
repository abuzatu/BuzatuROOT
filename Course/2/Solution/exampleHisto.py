#!/usr/bin/python

# python
import os,sys
# PyROOT
from ROOT import gROOT, gStyle, TFile, TTree, TH1F, TF1, TCanvas, TPaveText, TLegend, TLatex
gROOT.SetBatch(True)
# Fitting functions
from Bukin import Gauss, Bukin

fileName="./output/histo_llbb.root"
histoName="Higgs_PtRecoBukin_M"
plot_option="HIST"

file=TFile(fileName,"READ")
h=file.Get(histoName)
entries=h.GetEntries()
height=h.GetMaximum()
mean=h.GetMean()
rms=h.GetRMS()
color=h.GetLineColor()
f=TF1()
# create a function from a user defined class in a given range with 6 parameters
# we choose the range to be related to the histogram values
xmin=mean-3*rms
xmax=mean+3*rms
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
#

# Set up canvas, remove titles and stats boxes
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
   
def ratio(s,b,debug=False):
  if debug:
    print "s",s,"b",b
  if -0.0001<b<0.0001:
    result=0
  else:
    result=s/b
  return result
# done function

def plot_histo(h):
    c=TCanvas("c","c",600,300)
    h.SetXTitle("mbb [GeV]")
    h.SetYTitle("Number of events")
    h.Draw("HIST")
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
    c.Print("plot_histo.pdf")
# done

def plot_histo_and_fit(h):
    c=TCanvas("c","c",600,300)
    h.SetXTitle("mbb [GeV]")
    h.SetYTitle("Number of events")
    h.Fit("bukin","RQ","HIST",xmin,xmax)
    f=h.GetFunction("bukin")
    result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2),f.GetParameter(3),f.GetParameter(4),f.GetParameter(5))
    f.SetLineColor(color)
    f.Draw("same")
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
    c.Print("plot_histo_and_fit.pdf")
# done

def plot_fit(h):
    c=TCanvas("c","c",600,300)
    h.SetXTitle("mbb [GeV]")
    h.SetYTitle("Number of events")
    h.Fit("bukin","RQ","RO",xmin,xmax)
    f=h.GetFunction("bukin")
    result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2),f.GetParameter(3),f.GetParameter(4),f.GetParameter(5))
    f.SetLineColor(color)
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
    c.Print("plot_fit.pdf")
# done

def plot(h,option):
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
    c.Print("plot_option_"+option+".pdf")
# 

# to run explicitly
plot_histo(h.Clone())
plot_histo_and_fit(h.Clone())
plot_fit(h.Clone())

# the functions above can be replaced by just one function that takes an argument of what the user wants
for option in "histo,fit,histo+fit".split(","):
    print "option",option
    plot(h.Clone(),option)

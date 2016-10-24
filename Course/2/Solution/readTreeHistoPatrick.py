#!/usr/bin/python

# python
import os,sys, math
import Bukin
# PyROOT
from ROOT import *
gROOT.SetBatch(True)
# Set up canvas, remove titles and stats boxes
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
debug=False
fileName="./output/histo_llbb.root"
outputfileName="./output/handled.root"

def readHisto(histoMap, options):
    # open file
    file=TFile(fileName,"READ")
    if not file.IsOpen():
        print "File",fileName,"does not exist. WILL ABORT!!!"
        assert(False)
    #Get all of the histograms from the .root file
    hist_Higgs_Nominal_M = file.Get("Higgs_Nominal_M")
    histoMap['Nominal'] = hist_Higgs_Nominal_M
    hist_Higgs_OneMu_M=file.Get("Higgs_OneMu_M")
    histoMap['OneMu'] = hist_Higgs_OneMu_M
    hist_Higgs_PtRecoBukin_M=file.Get("Higgs_PtRecoBukin_M")
    histoMap['PtRecoBukin'] = hist_Higgs_PtRecoBukin_M
    hist_Higgs_PtRecoGauss_M=file.Get("Higgs_PtRecoGauss_M")
    histoMap['PtRecoGauss'] = hist_Higgs_PtRecoGauss_M
    hist_Higgs_Regression_M=file.Get("Higgs_Regression_M")
    histoMap['Regression'] = hist_Higgs_Regression_M
    hist_Higgs_Parton_M=file.Get("Higgs_Parton_M")
    histoMap['Parton'] = hist_Higgs_Parton_M

    fitting(histoMap,options)

def ratio(s,b,debug=False):
  if debug:
    print "s",s,"b",b
  if -0.0001<b<0.0001:
    result=0
  else:
    result=s/b
  return result
# done function

# ex: fit_hist(h,"Bukin","",false)
def fit_hist(h,fit,fit_options,plot_option):
    entries=h.GetEntries()
    height=h.GetMaximum()
    mean=h.GetMean()
    rms=h.GetRMS()
    result=(height,mean,rms)
    f=TF1()
    cutnentries=20
    color=h.GetLineColor()
    if fit=="Gauss":
        if entries>cutnentries and rms>0.02:
            xmin=mean-3*rms
            xmax=mean+3*rms
            function=TF1("gauss",Bukin.Gauss(),xmin,xmax,3)
            function.SetParName(0,"height")
            function.SetParName(1,"mean")
            function.SetParName(2,"width")
            function.SetParameter(0,height)
            function.SetParameter(1,mean)
            function.SetParameter(2,rms)
            h.Fit("gauss",fit_options,plot_option+"same",xmin,xmax)
            f=h.GetFunction("gauss")
            result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2))
            f.SetLineColor(color)
            #f.Draw("SAME")
        else:
            None
    elif fit=="Bukin":
        if entries>cutnentries and rms>0.02:
            xmin=mean-3*rms
            xmax=mean+3*rms
            function=TF1("bukin",Bukin.Bukin(),xmin,xmax,6)
            function.SetParName(0,"height")
            function.SetParName(1,"mean") # actually the peak, as it may be asymmetric
            function.SetParName(2,"width")
            function.SetParName(3,"asymmetry")
            function.SetParName(4,"size of lower tail")
            function.SetParName(5,"size of higher tail")
            function.SetParameter(0,height)
            function.SetParameter(1,mean)
            function.SetParameter(2,rms)
            
            h.Fit("bukin",fit_options,plot_option+"same",xmin,xmax)
            f=h.GetFunction("bukin")
            
            result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2),f.GetParameter(3),f.GetParameter(4),f.GetParameter(5))
            f.SetLineColor(color)
            #f.Draw("SAME")
        else:
            None    
    else:
        None
    return f,result


def fitting(histoMap,options):
    #Option, h - histo, hf -histo fit, f fit
    c = TCanvas("c", "c", 1000, 800)
    legend= TLegend(0.1,0.6,0.3,0.90)
    legend.SetTextFont(72)
    legend.SetTextSize(0.02)
    legend.AddEntry(None,"#bf{mean[GeV] / sigma[GeV] / ratio}","")
    first = True
    cnt = 1

    same = ""
    for key, value in histoMap.iteritems():
        fit = "Gauss"
        plot_option="RO"
        fit_options ="RQ0"
        
        if(first):
            first =False
            same = "same"

        f,result=fit_hist(value,fit,fit_options,plot_option)

        if options == "f":
            f.SetLineColor(cnt);
            f.Draw(same)
            legend.AddEntry("f",key+" fit","l")
            legend_text="#bf{%-.3f/%-.3f/%-.3f}" % (result[1],result[2],ratio(result[2],result[1]))
            legend.AddEntry(None,legend_text,"")
        elif options == "f":
            value.SetLineColor(cnt);
            value.Draw(same)
            legend.AddEntry(value,key,"f")
            legend_text="#bf{%-.3f/%-.3f/%-.3f}" % (result[1],result[2],ratio(result[2],result[1]))
            legend.AddEntry(None,legend_text,"")
        elif options == "hf":
            value.SetLineColor(cnt);
            value.Draw(same)
            value.SetXTitle("mbb [GeV]")
            value.SetYTitle("Number of events")
            legend.AddEntry(value,key,"f")
            f.SetLineColor(cnt);
            f.Draw("same")
            legend.AddEntry("f",key+" fit","l")
            legend_text="#bf{%-.3f/%-.3f/%-.3f}" % (result[1],result[2],ratio(result[2],result[1]))
            legend.AddEntry(None,legend_text,"")

        cnt +=1

    legend.Draw();
    c.Print("plot.pdf")
# done function

# execute

histoMap = {}
readHisto(histoMap,"hf")

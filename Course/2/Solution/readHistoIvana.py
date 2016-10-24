#!/usr/bin/python

# python
import os,sys

# PyROOT
from ROOT import gROOT, gStyle, TFile, THStack, TMultiGraph,  TTree, TH1F, TF1, THStack, TCanvas, TPaveText, TLegend, TLatex
gROOT.SetBatch(True)

# Fitting functions
from Bukin import Gauss, Bukin

# Histograms stack
hs = THStack("hs", "1D Histogram Stacking");


fileName="./output/histo_llbb.root"
file=TFile(fileName,"READ")

# Defining lists
Hlist = ["Higgs_Nominal_M", "Higgs_OneMu_M", "Higgs_AllMu_M", "Higgs_AllMuNu_M", "Higgs_PtRecoGauss_M", "Higgs_PtRecoBukin_M", "Higgs_Regression_M"]; h=[0,0,0,0,0,0,0]; entries=[0,0,0,0,0,0,0]; height=[0,0,0,0,0,0,0]; mean=[0,0,0,0,0,0,0];rms=[0,0,0,0,0,0,0]; xmin=[0,0,0,0,0,0,0]; xmax=[0,0,0,0,0,0,0]; legend_text=[0,0,0,0,0,0,0]; result=[0,0,0,0,0,0,0];f=[0,0,0,0,0,0,0];legend=[0,0,0,0,0,0,0]

# This loop does the histograms stacking and evaluates the elements of the fitting lists 
j=0;
while j<7:
    h[j]=file.Get(Hlist[j])
    h[j].SetLineColor(j+1)
    hs.Add(h[j])
    entries[j]=h[j].GetEntries()
    height[j]=h[j].GetMaximum()
    mean[j]=h[j].GetMean()
    rms[j]=h[j].GetRMS()
    xmin[j]=mean[j]-3*rms[j]
    xmax[j]=mean[j]+3*rms[j]
    f[j]=TF1()
    j=j+1
# done loop

# Set up canvas, remove titles and stats boxes
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

# This function returns result that will be used in building Legends
def ratio(s,b,debug=False):
  if debug:
    print "s",s,"b",b
  if -0.0001<b<0.0001:
    result=0
  else:
    result=s/b
  return result
# done function

# This function plots the histograms on the same canvas
def plot_histo(hs):
    l=0;
    c=TCanvas("c","c",1000,600)
    hs.Draw("nostack")
    hs.GetXaxis().SetTitle("mbb [GeV]")
    hs.GetYaxis().SetTitle("Number of events")
    legend=TLegend(0.13,0.41,0.25,0.88)
    legend.AddEntry(None,"#bf{mean[GeV] / sigma[GeV] / ratio}","")
    while l<7:
        legend.AddEntry(h[l],h[l].GetName(),"f[l]")
        result[l]=(height[l],mean[l],rms[l])
        legend_text[l]="#bf{%-.3f/%-.3f/%-.3f}" % (result[l][1],result[l][2],ratio(result[l][2],result[l][1]))
        legend.AddEntry(None,legend_text[l],"")
        l=l+1
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.03)
    legend.SetTextColor(1)    
    legend.Draw("SAME")
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(14)
    t.SetTextFont(43)
    t.SetTextAlign(13)
    t.DrawLatex(0.73,0.85,"#it{#bf{ATLAS} Simulation Internal}")
    t.Draw()   
    c.Print("plot_histo.pdf")
# done function   

# This function plots the Bukin fittings on the same canvas 
def plot_fit(h,xmin,xmax,height,mean,rms):
    k=0; m=0; s=0;
    c1=TCanvas("c1","c1",1000,600)
    while k<7:
        function=TF1("bukin",Bukin(),xmin[k],xmax[k],6)
        function.SetParName(0,"height")
        function.SetParName(1,"mean")
        function.SetParName(2,"width")
        function.SetParName(3,"asymmetry")
        function.SetParName(4,"size of lower tail")
        function.SetParName(5,"size of higher tail")
        function.SetParameter(0,height[k])
        function.SetParameter(1,mean[k])
        function.SetParameter(2,rms[k])
        h[k].Fit("bukin","RQ","RO",xmin[k],xmax[k])
        f[k]=h[k].GetFunction("bukin")
        k=k+1
    while m<7:
        h[m].SetXTitle("mbb [GeV]")
        h[m].SetYTitle("Number of events")
        f[m].SetLineColor(m+1)
        f[m].Draw("SAME")
        m=m+1
    legend=TLegend(0.13,0.41,0.25,0.88)
    legend.AddEntry(None,"#bf{mean[GeV] / sigma[GeV] / ratio}","")
    while s<7:
        legend.AddEntry(h[s],h[s].GetName(),"f[s]")
        result[s]=(height[s],mean[s],rms[s])
        legend_text[s]="#bf{%-.3f/%-.3f/%-.3f}" % (result[s][1],result[s][2],ratio(result[s][2],result[s][1]))
        legend.AddEntry(None,legend_text[s],"")
        s=s+1
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.03)
    legend.SetTextColor(1)    
    legend.Draw("SAME")
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(14)
    t.SetTextFont(43)
    t.SetTextAlign(13)
    t.DrawLatex(0.73,0.85,"#it{#bf{ATLAS} Simulation Internal}")
    t.Draw()   
    c1.Print("plot_fit.pdf")
# done function

# This function plots the histograms and the Bukin fittings on the same canvas
def plot_histo_and_fit(hs,f):
    n=0;r=0;
    c2=TCanvas("c2","c2",1000,600)
    hs.Draw("nostack")
    hs.GetXaxis().SetTitle("mbb [GeV]")
    hs.GetYaxis().SetTitle("Number of events")
    while n<7:
        h[n].SetXTitle("mbb [GeV]")
        h[n].SetYTitle("Number of events")
        f[n].SetLineColor(n+1)
        f[n].Draw("SAME")
        n=n+1
    legend=TLegend(0.13,0.41,0.25,0.88)
    legend.AddEntry(None,"#bf{mean[GeV] / sigma[GeV] / ratio}","")
    while r<7:
        legend.AddEntry(h[r],h[r].GetName(),"f[r]")
        result[r]=(height[r],mean[r],rms[r])
        legend_text[r]="#bf{%-.3f/%-.3f/%-.3f}" % (result[r][1],result[r][2],ratio(result[r][2],result[r][1]))
        legend.AddEntry(None,legend_text[r],"")
        r=r+1
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.03)
    legend.SetTextColor(1)    
    legend.Draw("SAME")
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(14)
    t.SetTextFont(43)
    t.SetTextAlign(13)
    t.DrawLatex(0.73,0.85,"#it{#bf{ATLAS} Simulation Internal}")
    t.Draw()   
    c2.Print("plot_histo_and_fit.pdf")
# done function

# to run explicitly
plot_histo(hs.Clone())
plot_fit(h,xmin,xmax,height,mean,rms)
plot_histo_and_fit(hs,f)


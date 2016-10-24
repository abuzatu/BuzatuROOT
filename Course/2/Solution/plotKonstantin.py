#!/usr/bin/python

# python
import os,sys
# PyROOT
from ROOT import gROOT, gStyle, TFile, TTree, TH1F, TF1, TCanvas, TPaveText, TLegend, TLatex
gROOT.SetBatch(True)
# Fitting functions
from Bukin import Gauss, Bukin

fileName="./output/histo_llbb.root"
histoName = []
# histoName[0]="Higgs_Nominal_M"
# histoName[1]="Higgs_OneMu_M"
# histoName[2]="Higgs_PtRecoGauss_M"
# histoName[3]="Higgs_PtRecoBukin_M"
# histoName[4]="Higgs_Parton_M"
# histoName[5]="Higgs_AllMuNu_M"
# histoName[6]="Higgs_TruthWZ_M"
# histoName[7]="Higgs_AllMu_M"
# histoName[8]="Higgs_Regression_M"
# histoName[9]="Higgs_OneMuNu_M"
histoName.append("Higgs_Nominal_M")
histoName.append("Higgs_OneMu_M")
histoName.append("Higgs_PtRecoGauss_M")
histoName.append("Higgs_PtRecoBukin_M")
histoName.append("Higgs_Parton_M") # zero width makes for division by zero in Bukin
histoName.append("Higgs_AllMuNu_M")
histoName.append("Higgs_TruthWZ_M") # not related to desired output
histoName.append("Higgs_AllMu_M")
histoName.append("Higgs_Regression_M")
histoName.append("Higgs_OneMuNu_M") # very similar to AllMuNu and not shown

file=TFile(fileName,"READ")

h = []
for i in range(0,10):
    h.append(file.Get(histoName[i]))

entries = []
for i in range(0,10):
    entries.append(h[i].GetEntries())

height = []
for i in range(0,10):
    height.append(h[i].GetMaximum())

mean = []
for i in range(0,10):
    mean.append(h[i].GetMean())

rms = []
for i in range(0,10):
    rms.append(h[i].GetRMS())

color = []
for i in range(0,10):
    color.append(h[i].GetLineColor())
# print(color)
# f=TF1()

# create a function from a user defined class in a given range with 6 parameters
# we choose the range to be related to the histogram values
xmin = []
xmax = []
for i in range(0,10):
    xmin.append(mean[i]-3*rms[i])
    xmax.append(mean[0]+3*rms[0])


function=TF1("bukin",Bukin(),xmin[0],xmax[0],6)

# give name to parameters
function.SetParName(0,"height")
function.SetParName(1,"mean") # actually the peak, as it may be asymmetric
function.SetParName(2,"width")
function.SetParName(3,"asymmetry")
function.SetParName(4,"size of lower tail")
function.SetParName(5,"size of higher tail")

# # set initial values to parameters
# # we can set to all of them, but the crucial ones are height, mean and width
# # if your fits fail, you can change the initialisations of these parameters
function.SetParameter(0,height[0])
function.SetParameter(1,mean[0])
function.SetParameter(2,rms[0])
#function.SetParameter(3,-0.4)
#function.SetParameter(4,0.01)
#function.SetParameter(5,0.005)
#

# Set up canvas, remove titles and stats boxes
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

def ratio(s,b,debug=False):
  if debug:
    print("s",s,"b",b)
  if -0.0001<b<0.0001:
    result=0
  else:
    result=s/b
  return result
# done function


def plot_fit(h):
    c=TCanvas("c","c",600*10,300*10)
    legend=TLegend(0.15,0.35,0.20,0.85)
    legend.AddEntry(None,"#bf{mean[GeV] / sigma[GeV] / ratio}","")

    function.SetParameter(0,height[0])
    function.SetParameter(1,mean[0])
    function.SetParameter(2,rms[0])
    h[0].SetXTitle("mbb [GeV]")
    h[0].SetYTitle("Number of events")
    h[0].Fit("bukin","RQ","RO",xmin[0],xmax[0])
    function.SetParameter(0,height[1])
    function.SetParameter(1,mean[1])
    function.SetParameter(2,rms[1])
    h[1].SetXTitle("mbb [GeV]")
    h[1].SetYTitle("Number of events")
    h[1].Fit("bukin","RQ","RO",xmin[1],xmax[1])
    function.SetParameter(0,height[2])
    function.SetParameter(1,mean[2])
    function.SetParameter(2,rms[2])
    h[2].SetXTitle("mbb [GeV]")
    h[2].SetYTitle("Number of events")
    h[2].Fit("bukin","RQ","RO",xmin[2],xmax[2])
    function.SetParameter(0,height[3])
    function.SetParameter(1,mean[3])
    function.SetParameter(2,rms[3])
    h[3].SetXTitle("mbb [GeV]")
    h[3].SetYTitle("Number of events")
    h[3].Fit("bukin","RQ","RO",xmin[3],xmax[3])
    function.SetParameter(0,height[5])
    function.SetParameter(1,mean[5])
    function.SetParameter(2,rms[5])
    h[5].SetXTitle("mbb [GeV]")
    h[5].SetYTitle("Number of events")
    h[5].Fit("bukin","RQ","RO",xmin[5],xmax[5])
    function.SetParameter(0,height[7])
    function.SetParameter(1,mean[7])
    function.SetParameter(2,rms[7])
    h[7].SetXTitle("mbb [GeV]")
    h[7].SetYTitle("Number of events")
    h[7].Fit("bukin","RQ","RO",xmin[7],xmax[7])
    function.SetParameter(0,height[8])
    function.SetParameter(1,mean[8])
    function.SetParameter(2,rms[8])
    h[8].SetXTitle("mbb [GeV]")
    h[8].SetYTitle("Number of events")
    h[8].Fit("bukin","RQ","RO",xmin[8],xmax[8])

    f=h[0].GetFunction("bukin")
    result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2),f.GetParameter(3),f.GetParameter(4),f.GetParameter(5))
    h[0].GetFunction("bukin").SetLineColor(1)
    h[1].GetFunction("bukin").SetLineColor(2)
    h[2].GetFunction("bukin").SetLineColor(3)
    h[3].GetFunction("bukin").SetLineColor(4)
    h[5].GetFunction("bukin").SetLineColor(5)
    h[7].GetFunction("bukin").SetLineColor(6)
    h[8].GetFunction("bukin").SetLineColor(7)


    h[8].GetFunction("bukin").Draw()
    h[0].GetFunction("bukin").Draw("SAME")
    h[1].GetFunction("bukin").Draw("SAME")
    h[2].GetFunction("bukin").Draw("SAME")
    h[3].GetFunction("bukin").Draw("SAME")
    h[5].GetFunction("bukin").Draw("SAME")
    h[7].GetFunction("bukin").Draw("SAME")

    for i in range(0,9):
        if i == 4 or i == 6 :
            continue
        f=h[i].GetFunction("bukin")
        result=(f.GetParameter(0),f.GetParameter(1),f.GetParameter(2),f.GetParameter(3),f.GetParameter(4),f.GetParameter(5))
        legend.AddEntry(f,h[i].GetName(),"f")
        result=(height[i],mean[i],rms[i])
        legend_text="#bf{%-.3f/%-.3f/%-.3f}" % (result[1],result[2],ratio(result[2],result[1]))
        legend.AddEntry(None,legend_text,"")
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.02)
    legend.SetTextColor(color[0])
    legend.Draw("SAME")
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(100)
    t.SetTextFont(43)
    t.SetTextAlign(13)
    t.DrawLatex(0.15,0.30,"#it{#bf{ATLAS} Simulation Internal}")
    t.Draw("SAME")
    # save the canvas to file
    c.Print("plot_fit.pdf")
# done


# PLOT
plot_fit(h)

#!/usr/bin/python
import os,sys,math
# PyROOT
from ROOT import gROOT, TFile, TTree, TLorentzVector, gStyle, TH1F, TF1, TStyle, TCanvas, TLegend, TAxis, TLatex
from Bukin import Gauss, Bukin

gROOT.SetBatch(True)

total = len(sys.argv)
# number of arguments plus 1
if total!=4:
    print "You need some arguments, will ABORT!"
    print "Ex: ./readHisto.py callibration fit plotType"
    print "Ex: ./readHisto.py OneMu Bukin histo"
    print "Ex: ./reaHisto.py Parton Gauss overlayed"
    print "Ex: ./readHisto.py Nominal Gauss fit"
    assert(False)
# done if

callibName=sys.argv[1]
callibration=str(callibName)

fitType=sys.argv[2]
fitName=str(fitType)

plotTypeName=sys.argv[3]
plotType=str(plotTypeName)

debug=True
fileName="./output/histo_llbb.root"
outputfileName="./output/"+callibration+"_"+fitName+"_"+plotType+".pdf"

if debug:
    print "We will be using callibration:", callibration
    print "Plot type will be:", plotType
    
 # open file
file=TFile(fileName,"READ")
if not file.IsOpen():
    print "File",fileName,"does not exist. WILL ABORT!!!"
    assert(False)

#get hist
histname = "Higgs_" + callibration + "_M"
histo = file.Get( histname )


def ratio(s,b,debug=False):
    if debug:
        print "s",s,"b",b
    if -0.0001<b<0.0001:
        result=0
    else:
        result=s/b
        return result
# done function

    
def PlotHisto(hist,fitName,plotType):   

    if debug:
        print "Fitting",fitName,"function"

    #get fitting params
    height=hist.GetMaximum()
    mean=hist.GetMean()
    rms=hist.GetRMS()
    #define fit range variables
    xmin=mean-3*rms
    xmax=mean+3*rms

    #make the required fit
    if fitName=="Gauss" :
        fitfunc = TF1('Gauss', Gauss(), xmin, xmax, 3)
        fitfunc.SetParameters(height, mean, rms)

    elif fitName=="Bukin":
        fitfunc = TF1('Bukin', Bukin(), xmin, xmax, 6)
        fitfunc.SetParameters(height, mean, rms, -0.4, 0.01, 0.005)

    #create and draw legend and canvas
    c = TCanvas( histname , histname ,800, 400 )
    legend=TLegend(0.13,0.7,0.45,0.85)
    #histoStyle()
    gStyle.SetOptTitle(0)
    gStyle.SetOptStat(0)
    
    #fit and plot according to requirements
    if plotType=="hist":
        hist.Fit(fitfunc,"0")
        legend.AddEntry(hist, "Higgs Mass histo", "l")
        hist.Draw()       
        
    elif plotType=="overlay":
        hist.Fit(fitfunc)
        legend.AddEntry(hist, "Higgs Mass histo", "l")
        legend.AddEntry(fitfunc, "Fitted function", "l")
        hist.Draw()

    elif plotType=="fit":
        hist.Fit(fitfunc)
        func = hist.GetFunction(fitName)
        legend.AddEntry(func, "Fitted function", "l")
        hist.Draw("FUNC")     

    func = hist.GetFunction(fitName)
    fitresults = (func.GetParameter(0),func.GetParameter(1),func.GetParameter(2),func.GetParameter(3),func.GetParameter(4),func.GetParameter(5))
    hist.SetXTitle("mbb [GeV]")
    hist.SetYTitle("Number of events")

    
    legend.AddEntry(None,"#bf{mean[GeV] / sigma[GeV] / ratio}","")
    legend_text="#bf{%-.3f/%-.3f/%-.3f}" % (fitresults[1],fitresults[2],ratio(fitresults[2],fitresults[1]))
    legend.AddEntry(None,legend_text,"")
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.03)
    legend.Draw("same")

    t = TLatex()
    t.SetNDC()
    t.SetTextSize(10)
    t.SetTextFont(43)
    t.SetTextAlign(13)
    t.DrawLatex(0.65,0.85,"#it{#bf{SUPAROOT} lab2 }")
    t.Draw("same")
    
    c.Print(outputfileName)

    return ;
#done function

PlotHisto(histo,fitName,plotType)

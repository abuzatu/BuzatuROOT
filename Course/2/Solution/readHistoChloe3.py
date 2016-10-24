#!/usr/bin/python

# python
import os,sys, math

# PyROOT
from ROOT import gROOT, TFile, TTree, TLorentzVector, gStyle, TH1F, TF1, TStyle, TCanvas, TLegend, TAxis, TLatex, TColor, TAttLine
from Bukin import Gauss, Bukin

gROOT.SetBatch(True)

total = len(sys.argv)
# number of arguments plus 1
if total<4:
    print "You need at least 3 arguments, will ABORT!"
    print "python readHistoChloe3.py Gauss fit Nominal,PtRecoGauss,AllMu,OneMu,AllMuNu,PtRecoBukin,Regression"
    print "You can replace Gauss with Bukin, and/or replace fit with overlay or hist."
    assert(False)
# done if

fitType=sys.argv[1]
fitName=str(fitType)

plotTypeName=sys.argv[2]
plotType=str(plotTypeName)

callibStringList=sys.argv[3]
calliblist=callibStringList.split(",")
ncallibs=len(calliblist)

debug=False
fileName="./output/histo_llbb.root"
outputfileName="./output/"+fitName+"_"+plotType+".pdf"

if debug:
    print "Plot type will be:", plotType
    
 # open file
file=TFile(fileName,"READ")
if not file.IsOpen():
    print "File",fileName,"does not exist. WILL ABORT!!!"
    assert(False)

#get list of histograms
histList=[]
for k in range(0,ncallibs):
    histname = "Higgs_" + calliblist[k] + "_M"
    histo=file.Get( histname )
    histList.append(histo)

    
def ratio(s,b,debug=False):
    if debug:
        print "s",s,"b",b
    if -0.0001<b<0.0001:
        result=0
    else:
        result=s/b
        return result
# done function

    
def OverlayHistograms(fitName,plotType,histograms,outputfileName):   
    
    if debug:
        print "Fitting",fit,"function"
        print "PlotType:", plotType

    #create and draw legend and canvas
    c = TCanvas( "canvas" , "canvas" ,1600, 800 )
    legend=TLegend(0.12,0.47,0.40,0.87)
    legend.AddEntry(None,"#bf{mean[GeV] / sigma[GeV] / ratio}","")
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.03)
    
    gStyle.SetOptTitle(0)
    gStyle.SetOptStat(0)

    #make a template histo so that y axis has correct height
    #find max height
    for hist in histograms:
        heights=[]
        height=hist.GetMaximum()
        heights.append(height)

    maxheight=max(heights)+100
    template=histograms[0].Clone()
    template.SetMaximum(maxheight)
    template.Reset()
    template.Draw()
    template.SetXTitle("mbb [GeV]")
    template.SetYTitle("Number of events")  

    col=2
    #loop over histos to overlay
    for hist in histograms:        

        #get fitting params
        height=hist.GetMaximum()
        mean=hist.GetMean()
        rms=hist.GetRMS()

        #set line color
        hist.SetLineColor(col)
        
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


    
        #fit and plot according to requirements
        if plotType=="hist":
            hist.Fit(fitfunc,"0")
            legend.AddEntry(hist, hist.GetName(), "l")
            hist.Draw("same")       
        
        elif plotType=="overlay":
            hist.Fit(fitfunc,"0")
            func = hist.GetFunction(fitName)
            legend.AddEntry(hist,hist.GetName(), "l")
            hist.Draw("same")
            func.SetLineColor(col)
            func.Draw("SAME")

        elif plotType=="fit":
            hist.Fit(fitfunc,"0")
            func = hist.GetFunction(fitName)
            legend.AddEntry(hist,hist.GetName(), "l")
            func.Draw("SAME")
            func.SetLineColor(col)

        #show fit results in the legend
        func = hist.GetFunction(fitName)
        fitresults = (func.GetParameter(0),func.GetParameter(1),func.GetParameter(2),func.GetParameter(3),func.GetParameter(4),func.GetParameter(5))   
        legend_text="#bf{%-.3f/%-.3f/%-.3f}" % (fitresults[1],fitresults[2],ratio(fitresults[2],fitresults[1]))
        legend.AddEntry(None,legend_text,"")

        col+=1
        #end for loop
        
    legend.Draw("same")

    #plot text
    t = TLatex()
    t.SetNDC()
    t.SetTextSize(14)
    t.SetTextFont(43)
    t.SetTextAlign(13)
    t.DrawLatex(0.8,0.85,"#it{#bf{SUPAROOT} lab2 }")
    t.Draw("same")

    c.Print(outputfileName)
    return ;
#done function

OverlayHistograms(fitName,plotType,histList,outputfileName)






#!/usr/bin/python

# python
import os,sys
# PyROOT
from ROOT import gROOT, gStyle, TFile, TTree, TH1F, TF1, TCanvas, TPaveText, TLegend
gROOT.SetBatch(True)
# Fitting functions
from Bukin import Gauss, Bukin

fileName="./output/histo_llbb.root"

total = len(sys.argv)
# number of arguments plus 1
if total!=2:
    print "You need some arguments, will ABORT!"
    print "Ex: ./readTree.py FittingType"
    print "1= Gaussian, 2= Bukin"
    print "Ex: ./readTree.py 1"
    print "Ex: ./readTree.py 2"
    assert(False)
# done if

Fit=sys.argv[1]
Fit_id=int(Fit)

DrawBothHistAndFit = False
DrawJustFit = True



def Overlay(scalestring):
   list_scale = scalestring.split(",")

   # Set up canvas, remove titles and stats boxes
   gStyle.SetOptTitle(0)
   gStyle.SetOptStat(0)
   c = TCanvas("c","c",1600,800)

   # Legend
   mylegend = TLegend(1.0,0.5,0.73,1.0,"Legend")
   mylegend.SetTextSize(0.04)

   maximumValue=0.0
   dict_scale_hist= {}
   for i,scale in enumerate(list_scale):
       histname = "Higgs_"+scale+"_M"
       dict_scale_hist[scale] = file.Get(histname)
       h=dict_scale_hist[scale]
       h.SetLineColor(i+1) 

       h.SetFillColorAlpha(i+1, 0.3)  
       # I believe histograms are clearer with solid fill, now transparent

       if h.GetMaximum()>maximumValue:
           maximumValue = h.GetMaximum()

   # increase maximum by 10% to ensure histos fit canvas
   maximumValue *= 1.10

   for i,scale in enumerate(list_scale):
       h=dict_scale_hist[scale]
       if i==0:
           h.SetMaximum(maximumValue)
           h.Draw()
       else:
           h.Draw("same")

       # Add legend entry
       mylegend.AddEntry(h,h.GetName(),"f")

   #Set Canvas Title
   pave = TPaveText(0.00,0.9,0.3,1.0,"tblrNDC")
   pave.SetTextColor(1)
   pave.SetTextSize(0.05)
   pave.AddText("Overlaid Histograms")
   pave.Draw("same")

   # Draw legend
   mylegend.Draw("same")

   c.Print("output/overlay.pdf")

def Fitting(scalestring,Fit_id):
   list_scale = scalestring.split(",")

   # Set up canvas, remove titles and stats boxes
   gStyle.SetOptTitle(0)
   gStyle.SetOptStat(0)
   c = TCanvas("c","c",1600,800)

   # Legend
   mylegend = TLegend(1.0,0.3,0.75,1.0,"Legend")
   mylegend.SetTextSize(0.04)

   dict_scale_hist= {}
   dict_gaus_fit= {}
   dict_bukin_fit= {}
   colorcounter= 1

   for scale in list_scale:
       histname = "Higgs_"+scale+"_M"
       dict_scale_hist[scale] = file.Get(histname)
       h=dict_scale_hist[scale]

       xmin = h.GetMean()-3*h.GetRMS()
       xmax = h.GetMean()+3*h.GetRMS()

       # If error here, check Bukin.py has: import math
       dict_gaus_fit[scale] = TF1 ("Gauss",Gauss(),xmin,xmax,3) 
       dict_bukin_fit[scale] = TF1 ("Bukin",Bukin(),xmin,xmax,6)

   for scale in list_scale:
       h=dict_scale_hist[scale]
       if Fit_id==1:
          print
          print "The ROOT Gaussian fit produces: "
          h.Fit("gaus","0 +")  # zero option to not draw

          print
          print "The user defined Gaussian fit produces: "
          dict_gaus_fit[scale].SetParName(0,"User_Constant")
          dict_gaus_fit[scale].SetParName(1,"User_Mean")
          dict_gaus_fit[scale].SetParName(2,"User_Sigma")
          dict_gaus_fit[scale].SetLineColor(colorcounter)
          dict_gaus_fit[scale].SetParameters(100, h.GetMean(),h.GetRMS())
 
          # Add legend entry for Gaussian
          mylegend.AddEntry(dict_gaus_fit[scale],scale+"_Gauss","l")

          if DrawBothHistAndFit:
              h.Fit(dict_gaus_fit[scale],"+ R")
              f = h.GetFunction("Gauss")
              f.SetLineColor(colorcounter)

          if DrawJustFit:
              h.Fit(dict_gaus_fit[scale],"RQ","RO SAME",xmin,xmax)
              f = h.GetFunction("Gauss")
              f.SetLineColor(colorcounter)

       elif Fit_id==2:
          print
          print "The Bukin fit produces: "
          dict_bukin_fit[scale].SetParameters(0, h.GetMean(), h.GetRMS(), 0, 0, 0)
          dict_bukin_fit[scale].SetLineColor(colorcounter)


          # Add legend entry
          mylegend.AddEntry(dict_bukin_fit[scale],scale+"_Bukin","l")

          if DrawBothHistAndFit:
              h.Fit(dict_bukin_fit[scale],"+ R")
              f = h.GetFunction("Bukin")
              f.SetLineColor(colorcounter)

          if DrawJustFit:
              h.Fit(dict_bukin_fit[scale],"RQ","RO SAME",xmin,xmax)
              f = h.GetFunction("Bukin")
              f.SetLineColor(colorcounter)

       colorcounter += 1

   for scale in list_scale:
       h=dict_scale_hist[scale]
       if DrawBothHistAndFit:
           h.Draw("same")
       if DrawJustFit:
           h.Draw("func same")

   #Set Canvas Title
   pave = TPaveText(0.00,0.9,0.3,1.0,"tblrNDC")
   pave.SetTextColor(1)
   pave.SetTextSize(0.05)
   pave.AddText("Histogram Fits")
   pave.Draw("same")

   # Draw legend
   mylegend.Draw("same")

   c.Print("output/fitted.pdf")


####### Execute ########

# open file
file=TFile(fileName,"READ")
if not file.IsOpen():
    print "File",fileName,"does not exist. WILL ABORT!!!"
    assert(False)

scalestring = "Nominal,OneMu,OneMuNu,AllMu,AllMuNu,PtRecoBukin,PtRecoGauss,Regression" #Does not include Parton
Overlay(scalestring)
Fitting(scalestring,Fit_id)

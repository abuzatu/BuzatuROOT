#!/usr/bin/python
from ROOT import TH1F, TCanvas, gROOT

gROOT.SetBatch(True)

def change_color(h,color):
    h.SetLineColor(color)
# done function

color=2
h=TH1F("hist","hist",10,0,100);
h.Fill(23,3);
h.Fill(44,6);
h.Fill(67,2);
change_color(h,color)
c=TCanvas("c","c",600,400)
h.Draw("")
c.Print("./histogram_python.pdf");

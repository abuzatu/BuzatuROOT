#!/usr/bin/python
from ROOT import TFile, TGraph, TCanvas, gROOT

gROOT.SetBatch(True)

outputfile=TFile("./output/graph.root","RECREATE")
g=TGraph("./input/Earth.txt");
c=TCanvas("c","c",600,400)
g.Draw("")
c.Print("./output/orbit.pdf");
g.Write();
outputfile.Write()
outputfile.Close()

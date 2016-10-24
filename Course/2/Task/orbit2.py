#!/usr/bin/python
#ftp://root.cern.ch/root/doc/ROOTUsersGuideHTML/ch04.html#d5e4331
from ROOT import TFile, TGraph, TCanvas, gROOT

gROOT.SetBatch(True)

#outputfile=TFile("./output/graph.root","RECREATE")
path="/Users/abuzatu/Work/Code/TutorialCPP/Course/4/Solution/output/"
bodies="Neptune,Uranus,Saturn,Jupiter,Mars,Earth,Venus,Mercury".split(",")
bodies="Jupiter,Mars,Earth,Venus,Mercury".split(",")
#bodies="Mars,Earth,Venus,Mercury".split(",")
dict_body_color={}
dict_body_color["Neptune"]=1
dict_body_color["Uranus"]=2
dict_body_color["Saturn"]=3
dict_body_color["Jupiter"]=4
dict_body_color["Mars"]=5
dict_body_color["Earth"]=6
dict_body_color["Venus"]=7
dict_body_color["Mercury"]=8
#bodies="Neptune,Uranus".split(",")
suffix=".txt"
dict_body_TGraph={}
for body in bodies:
    dict_body_TGraph[body]=TGraph(path+body+suffix)
# done loop over bodies
c=TCanvas("c","c",600,400)
for i,body in enumerate(bodies):
    print i,body
    if i==0:
        option="AC"
    else:
        option="C"
    dict_body_TGraph[body].SetLineColor(dict_body_color[body])
    dict_body_TGraph[body].Draw(option)
# done loop over bodies
#c.Print("./output/orbit.pdf")
c.Print("./output/orbit_Jupiter.gif")
#for body in bodies:
#    dict_body_TGraph[body].Write()
#outputfile.Write()
#outputfile.Close()

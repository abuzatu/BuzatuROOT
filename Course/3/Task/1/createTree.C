//include from C++
#include <iostream>
#include <stdio.h>
#include <sstream> 

//includes from ROOT
#include "TFile.h"
#include "TTree.h"

int main()
{
  TFile* file = TFile::Open("./output/tree.root","RECREATE");
  TTree *tree = new TTree("test","test");
  Int_t integer_value;
  Float_t float_value;
  Double_t double_value;
  Char_t char_value;
  std::string string_value;
  
  tree->Branch("integer_value",&integer_value,"integer_value/I");
  tree->Branch("float_value",&float_value,"float_value/F");
  tree->Branch("double_value",&double_value,"double_value/D");
  tree->Branch("char_value",&char_value,"char_value/C");
  //loop over how entries your tree should have
  for (unsigned i=0; i!=5; i++) {
    integer_value=(Int_t) i;
    float_value=(Float_t) i;
    double_value=(Double_t) i;
    //convert int to char
    std::stringstream ss;
    ss<<i;
    char_value=ss.str().at(0);
    //end convert int to char
    //for each entry update all the values
    tree->Fill();
  }
  //the tree is now filled
  file->Write();
}

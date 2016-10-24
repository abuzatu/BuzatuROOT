//include from C++
#include <iostream>
#include <stdio.h>
#include <sstream> 
#include <fstream>

//includes from ROOT
#include "TFile.h"
#include "TTree.h"

//includes from my code
#include "Vector3D.h" //MY CLASS

int main()
{
  TFile* file = TFile::Open("./output/tree.root","RECREATE");
  TTree *tree = new TTree("test","test");

  //define variables that will be recomputed for every tree entry
  Int_t integer_value;
  Float_t float_value;
  Double_t double_value;
  Char_t char_value;
  Vector3D Vector3D_value;  //MY CLASS
  //set these variables as branches to the tree
  //note the &, the reference to the variables above
  tree->Branch("integer_value",&integer_value,"integer_value/I");
  tree->Branch("float_value",&float_value,"float_value/F");
  tree->Branch("double_value",&double_value,"double_value/D");
  tree->Branch("char_value",&char_value,"char_value/C");
  //the ones above have a third argument telling the C++ type
  //for our own define type, no third argument, as we do the extra
  //rootcint step in the compilation
  //and we make the class inherit from TObject
  //check the elements in Vector3D.h and Vector3D.cxx that are for 
  //saving to a TTree
  tree->Branch("Vector3D_value",&Vector3D_value); //MY CLASS
  //filling the TTree with the values from the text file
  std::string line;
  std::ifstream myfile ("./input/input.txt");
  double x, y, z;
  unsigned counter=0;
  if(myfile.is_open()){
    while(getline(myfile,line)) {
      if (line=="") continue;
      //
      integer_value=(Int_t) counter;
      float_value=(Float_t) counter;
      double_value=(Double_t) counter;
      //convert int to char
      std::stringstream ssc;
      ssc<<counter;
      char_value=ssc.str().at(0);
      //get the Vector3D v from the line
      std::cout<<"line="<<line<<std::endl;
      std::stringstream ss(line);
      ss>>x>>y>>z;
      Vector3D_value=Vector3D(x,y,z); //MY CLASS
      std::cout<<"Vector3D_value="<<Vector3D_value<<std::endl; //MY CLASS
      //done get the Vector3D v from the line
      //fill all of these to the TTree
      tree->Fill();      
      //increase the counter
      counter++;
    }//end while there are lines
  }//end loop over the input file
  //the tree is now filled
  //we save the file and indirectly it saves the tree owned by the file
  file->Write();
}

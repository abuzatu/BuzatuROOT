//include from C++
#include <iostream>
#include <stdio.h>
#include <sstream> 
#include <fstream>
#include <assert.h>

//includes from ROOT
#include "TFile.h"
#include "TTree.h"

//includes from my code
#include "Vector3D.h" //MY CLASS

int main()
{
  std::string input_file_name="./output/tree.root";
  std::string input_tree_name="test";
  //get file
    TFile* input_file = TFile::Open(input_file_name.c_str(),"READ");
  if(! input_file->IsOpen()){
    std::cout << "Unable to find root file "<<input_file_name 
	      << ". Will ABORT!!!"<<std::endl;
    assert(false);
  }
  //get tree
  TTree *input_tree = (TTree*) input_file->Get(input_tree_name.c_str());
  if(!input_tree){
    std::cout << "Unable to find TTree "<<input_tree_name<<" in file " << input_file_name 
	      << ". Will ABORT!!!"<<std::endl;
    assert(false);
  }
  //info
  std::cout<<"TTree "<<input_tree_name<<" has "<<input_tree->GetEntries()
	   <<" entries"<<std::endl;
  //define variables that will be recomputed for every tree entry
  Int_t integer_value;
  Float_t float_value;
  Double_t double_value;
  Char_t char_value;
  Vector3D* Vector3D_pointer=NULL; //MY CLASS
  //set these variables as branches to the tree
  //note the &, the reference to the variables above
  input_tree->SetBranchAddress("integer_value",&integer_value);
  input_tree->SetBranchAddress("float_value",&float_value);
  input_tree->SetBranchAddress("double_value",&double_value);
  input_tree->SetBranchAddress("char_value",&char_value);//MY CLASS
  input_tree->SetBranchAddress("Vector3D_value",&Vector3D_pointer);//MY CLASS
  //loop over all the entries in the tree
  for(unsigned i=0; i!=input_tree->GetEntries(); i++) {
    input_tree->GetEntry(i);
    //now all the variables from above have values for the current entry
    std::cout<<" ***** new entry "<<i<<" *****"<<std::endl;
    std::cout<<"integer_value="<<integer_value<<std::endl;
    std::cout<<"float_value="<<float_value<<std::endl;
    std::cout<<"double_value="<<double_value<<std::endl;
    std::cout<<"char_value="<<char_value<<std::endl;
    std::cout<<"Vector3D_address="<<Vector3D_pointer<<std::endl;//MY CLASS
    std::cout<<"Vector3D_value="<<(*Vector3D_pointer)<<std::endl;//MY CLASS
  }
  //end loop over all the entries in the tree

  return 0;
}

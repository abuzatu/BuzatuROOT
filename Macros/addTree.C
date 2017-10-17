//25 June 2012, Adrian Buzatu
//how to add a TTree to a .root file

#include <iostream>
#include <string>
#include "TFile.h"
#include "TTree.h"
void addTree(){
  unsigned NEvents=10;
  
  std::string file1_name="testnew.root";
  TFile *file1=new TFile((file1_name).c_str(),"update");
  TTree* tree1=new TTree("test1","test1");
  double pT1;
  tree1->Branch("pT1",&pT1,"pT1/D");
  if(tree1==NULL)
    {
      std::cout<<"tree1 creation failed, will abort!!!"<<std::endl;
      return;
    }
  else
    {
      std::cout<<"tree1 creation successful"<<std::endl;
    }
  for(unsigned i=0; i!=NEvents; i++)
    {
      pT1=70.0;
      tree1->Fill();
    }
  tree1->Write();
  //avoid file1->Write() as this would create a second cycle of the tree
  file1->Close();
}

#include <string>
#include "TFile.h"
#include "TTree.h"
#include <iostream>
void thinTree(){

  std::string file_name="test1.root";
  std::string tree_name="test1";
  TFile* file=new TFile((file_name).c_str());
  //then get the tree that we need
  TTree* tree=dynamic_cast<TTree*>(file->Get(tree_name.c_str()));
  if(!tree){
    std::cout << "Unable to find TTree "<<tree_name<<" in file " << file_name 
	      << std::endl;
    return;
  }

  unsigned NEntries=tree->GetEntries();
  std::cout<<"TTree "<<tree_name<<" has "<<NEntries<<" entries."<<std::endl;

  std::string file_out_name="thin_test1.root";
  TFile* file_out = new TFile(file_out_name.c_str(), "recreate");
  TTree* tree_out = tree->CloneTree(0);
  double a;
  tree->SetBranchAddress("a",     &a);


  for(unsigned i=0; i!=NEntries; i++)
    {
      tree->GetEntry(i);
      std::cout<<"a="<<a<<std::endl;
      if(a>0.5 && a < 1.4)
	tree_out->Fill();
    }

  //tree_out->Print();
  tree_out->AutoSave();
  delete file;
  delete file_out;
  
}


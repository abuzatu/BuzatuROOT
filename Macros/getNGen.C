#include <iostream>
#include <string>
#include "TFile.h"
#include "TTree.h"
void getNGen(std::string file_input){

  //open the input .root file
  TFile *fin=new TFile((file_input).c_str());
  
  //the get the tree that we need to read
  //globaldata
  TTree* mytree_globaldata=dynamic_cast<TTree*>(fin->Get("globaldata"));
  if(!mytree_globaldata){
    std::cout << "Unable to find tree -globaldata- in file " << file_input 
	      << std::endl;
    return;
  }



  //the branches in the globaldata tree
  int NGen=0;
  //extra variables
  int summed_NGen=0;
  
  //set the branches I need to read
  mytree_globaldata->SetBranchAddress("NGen",        &NGen);
  
  //this is also the number of how many files we merged
  //as the global for a single file has only one event entry
  int number_entries=mytree_globaldata->GetEntries();
  
  //loop over all the entries 
  for(int i=0;i<number_entries;i++) {
    //get the current entry
    mytree_globaldata->GetEntry(i);
    summed_NGen+=NGen;
    //cout << "NGen="<< NGen << endl;
 
  }//end loop over all the entries in globaldata 
  //to have info for the data tree
  //it is enough to write it outside the event loop, to write it once
  //cout << "summed_NGen="<< summed_NGen << endl;
  cout<<summed_NGen<<endl;
 
}

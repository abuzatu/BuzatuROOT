//26 June 2012, Adrian Buzatu
//how to replace a TTree in a .root file
//first we want to read the TTree
//create a new TTree based on the same information
//store the tree name
//remove the first tree
//copy the new tree
//make sure it has the same name

#include <string>
#include "TFile.h"
void replaceTree(){

  std::string file_name="testnew.root";
  TFile *file=new TFile((file_name).c_str(),"update");
  std::string object_to_remove="test1;*";
  //the object can be a tree, a histogram, etc, in this case "test1" is a TTree
  //notice the ";1" which means cycle 1; to remove all cycles do ";*"
  //if your object is not at the top directory, but in a directory in the .root file, called foo
  // you do first
  //file->cd("foo");
  //then continue with the Delete command which is only applied to the current gDirectory
  gDirectory->Delete(object_to_remove.c_str());
  file->Close();
}

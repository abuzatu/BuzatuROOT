#include <iostream>
#include <string>
#include "TFile.h"
#include "TTree.h"
void createTrees(){

  unsigned NEvents=10;
  
  std::string file1_name="test1.root";
  TFile *file1=new TFile((file1_name).c_str(),"recreate");
  TTree* tree1=new TTree("test1","test1");
  double pT1;
  tree1->Branch("pT1",&pT1,"pT1/D");
  double a, b, c, d, e, f, g, h;
  tree1->Branch("a",&a,"a/D");
  tree1->Branch("b",&b,"b/D");
  tree1->Branch("c",&c,"c/D");
  tree1->Branch("d",&d,"d/D");
  tree1->Branch("e",&e,"e/D");
  tree1->Branch("f",&f,"f/D");
  tree1->Branch("g",&g,"g/D");
  tree1->Branch("h",&h,"h/D");
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
      pT1=50.0;
      if(i%2 == 0)
	a=1.0;
      else
	a=1.5;
      b=2.0;
      c=3.0;
      d=4.0;
      e=5.0;
      f=6.0;
      g=7.0;
      h=8.0;
      tree1->Fill();
    }
  tree1->Write();
  file1->Write();
  file1->Close();

  std::string file2_name="test2.root";
  TFile *file2=new TFile((file2_name).c_str(),"recreate");
  TTree* tree2=new TTree("test2","test2");
  double pT2;
  tree2->Branch("pT2",&pT2,"pT2/D");
  if(tree2==NULL)
    {
      std::cout<<"tree2 creation failed, will abort!!!"<<std::endl;
      return;
    }
  else
    {
      std::cout<<"tree2 creation successful"<<std::endl;
    }
  for(unsigned i=0; i!=NEvents; i++)
    {
      pT2=60.0;
      tree2->Fill();
    }
  tree2->Write();
  file2->Write();
  file2->Close();
  
  

}

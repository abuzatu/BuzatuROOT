#include <iostream>
#include <string>
#include "TFile.h"
#include "TTree.h"
void fixGlobal(std::string file_name, int summed_NGen, bool isData){

  //file_name = name of input .root file
  //NGen_summed is the sum over all the .root files from this process
  //computed in the bash script and then passed to this file
  //isData = 1 if data and 0 if MC

  //open the input .root file
  TFile *f=new TFile((file_name).c_str(),"update");

  //*******************************************************************
  //*******************************************************************
  
  //the get the tree that we need to modify
  //globaldata
  TTree* mytree_globaldata=dynamic_cast<TTree*>(f->Get("globaldata"));
  if(!mytree_globaldata){
    std::cout << "Unable to find TTree \"globaldata\" in file " << file_name 
	      << std::endl;
    return;
  }
  //*******************************************************************
  //*******************************************************************

  //the branches in the globaldata tere

  //defined and initilize the variables
  int Entries=0;
  //int NGen=0;
  double my_xSect=0.0;
  double my_brFrac=0.0;
  double my_filterEff=0.0;
  double my_integral=0.0;
  double my_fraction=0.0;
  double Lumi=0.0;
  Int_t WenuHbb[2];
  Int_t Wenujets[2];
  Int_t Wmujets[2];//notice the missing nu, I add it when writing the new tree
  Int_t WmunuHbb[2];
  Int_t ZeeHbb[2];
  Int_t ZmumuHbb[2];
  Int_t ZnunuHbb[2];
  Int_t ejets[2];
  Int_t mujets[2];
  Int_t ttbareHbb[2];
  Int_t ttbarhadHbb[2];
  Int_t ttbarmuHbb[2];
  //extra: need to sum up all the entries, in globaldata there is one entry for each merged file
  int summed_Entries=0;
  //int summed_NGen=0;

  if(isData)
    {
      //one leaf per branch
      //all are 1 for data so that the magic formula gives the weight of 1.0 for data events
      summed_Entries=1;
      //summed_NGen=1;
      my_xSect=1.0;
      my_brFrac=1.0;
      my_filterEff=1.0;
      my_integral=1.0;
      my_fraction=1.0;
      Lumi=1.0;
      //two leaves per branch, we copy paste the code below from the output when running
      //over a MC sample that has the same cutMast and invertWord as the data, if there is
      //a bug in the data values, they should be the same for MC
      //if you recompute them, simply change here
      WenuHbb[0]=1073692671;
      WenuHbb[1]=1070335984;
      Wenujets[0]=1073692671;
      Wenujets[1]=1070335856;
      Wmujets[0]=1073692671;
      Wmujets[1]=1070335720;
      WmunuHbb[0]=1073692671;
      WmunuHbb[1]=1070335976;
      ZeeHbb[0]=1073700863;
      ZeeHbb[1]=1070335952;
      ZmumuHbb[0]=1073700863;
      ZmumuHbb[1]=1070335912;
      ZnunuHbb[0]=1073713151;
      ZnunuHbb[1]=1070338040;
      ejets[0]=1072644095;
      ejets[1]=788344;
      mujets[0]=1072644095;
      mujets[1]=788216;
      ttbareHbb[0]=1073692671;
      ttbareHbb[1]=1057753072;
      ttbarhadHbb[0]=1073691039;
      ttbarhadHbb[1]=33304984;
      ttbarmuHbb[0]=1073692671;
      ttbarmuHbb[1]=1057753000;
    }//end if data
  else
    {
      //if MC
      //we read the current global tree leaves, keep them the same, except Entries and NGen
      //which we sum up
      //Read the input globaltree information
      
      //set the branches I need to read
      //these have only one leaf per branch, the standard style
      mytree_globaldata->SetBranchAddress("Entries",     &Entries);
      //mytree_globaldata->SetBranchAddress("NGen",        &NGen);
      mytree_globaldata->SetBranchAddress("my_xSect",    &my_xSect);
      mytree_globaldata->SetBranchAddress("my_brFrac",   &my_brFrac);
      mytree_globaldata->SetBranchAddress("my_filterEff",&my_filterEff);
      mytree_globaldata->SetBranchAddress("my_integral", &my_integral);
      mytree_globaldata->SetBranchAddress("my_fraction", &my_fraction);
      mytree_globaldata->SetBranchAddress("Lumi",        &Lumi);
      //these have to leaves per branch and will return an array of values
      mytree_globaldata->SetBranchAddress("WenuHbb",     &WenuHbb);
      mytree_globaldata->SetBranchAddress("WmunuHbb",    &WmunuHbb);
      mytree_globaldata->SetBranchAddress("ZeeHbb",      &ZeeHbb); 
      mytree_globaldata->SetBranchAddress("ZmumuHbb",    &ZmumuHbb);
      mytree_globaldata->SetBranchAddress("ZnunuHbb",    &ZnunuHbb);
      mytree_globaldata->SetBranchAddress("Wmujets",     &Wmujets); 
      mytree_globaldata->SetBranchAddress("Wenujets",    &Wenujets); 
      mytree_globaldata->SetBranchAddress("ejets",       &ejets); 
      mytree_globaldata->SetBranchAddress("mujets",      &mujets); 
      mytree_globaldata->SetBranchAddress("ttbareHbb",   &ttbareHbb); 
      mytree_globaldata->SetBranchAddress("ttbarmuHbb",  &ttbarmuHbb); 
      mytree_globaldata->SetBranchAddress("ttbarhadHbb", &ttbarhadHbb); 
      
      //this is also the number of how many files we merged
      //as the global for a single file has only one event entry
      int number_entries=mytree_globaldata->GetEntries();
      
      //loop over all the entries 
      for(int i=0;i<number_entries;i++) {
	//get the current entry
	mytree_globaldata->GetEntry(i);
	summed_Entries+=Entries;

	//why do I need NGen summed in a different script instead of just here, after all
	//it works for Entries
	//summed_NGen+=NGen;
	//all the variables should now have values for the current entry
	//one leaf per branch
	/*
	  cout << "Entries="<< Entries << endl;
	  cout << "NGen="<< NGen << endl;
	  cout << "my_xSect="<< my_xSect << endl;
	  cout << "my_brFrac="<< my_brFrac << endl;
	  cout << "my_filterEff="<< my_filterEff << endl;
	  cout << "my_integral="<< my_integral << endl;
	  cout << "my_fraction="<< my_fraction << endl;
	  cout << "Lumi="<< Lumi << endl;
	  //two leaves per branch
	  cout << "WenuHbb cutMask="<<WenuHbb[0]<<" invertWord="<<WenuHbb[1]<< endl;
	  cout << "Wenujets cutMask="<<Wenujets[0]<<" invertWord="<<Wenujets[1]<< endl;
	  cout << "Wmujets cutMask="<<Wmujets[0]<<" invertWord="<<Wmujets[1]<< endl;
	  cout << "WmunuHbb cutMask="<<WmunuHbb[0]<<" invertWord="<<WmunuHbb[1]<< endl;
	  cout << "ZeeHbb cutMask="<<ZeeHbb[0]<<" invertWord="<<ZeeHbb[1]<< endl;
	  cout << "ZmumuHbb cutMask="<<ZmumuHbb[0]<<" invertWord="<<ZmumuHbb[1]<< endl;
	  cout << "ZnunuHbb cutMask="<<ZnunuHbb[0]<<" invertWord="<<ZnunuHbb[1]<< endl;
	  cout << "ejets cutMask="<<ejets[0]<<" invertWord="<<ejets[1]<< endl;
	  cout << "mujets cutMask="<<mujets[0]<<" invertWord="<<mujets[1]<< endl;
	  cout << "ttbareHbb cutMask="<< ttbareHbb[0]<<" invertWord="<< ttbareHbb[1]<< endl;
	  cout << "ttbarhadHbb cutMask="<<ttbarhadHbb[0]<<" invertWord="<<ttbarhadHbb[1]<< endl;
	  cout << "ttbarmuHbb cutMask="<<ttbarmuHbb[0]<<" invertWord="<<ttbarmuHbb[1]<< endl;
	  //extra
	  cout << "summed_Entries="<< summed_Entries << endl;
	  cout << "summed_NGen="<< summed_NGen << endl;
	  
	*/
	//ex: cutMask:    1073692671
	//ex: invertWord: 107033598414957047
      }//end loop over all the entries in globaldata 
      //to have info for the data tree
      //it is enough to write it outside the event loop, to write it once
      /*
      cout << "      WenuHbb[0]="<<WenuHbb[0]<<";"<<endl;
      cout << "      WenuHbb[1]="<<WenuHbb[1]<<";"<<endl;
      cout << "      Wenujets[0]="<<Wenujets[0]<<";"<<endl;
      cout << "      Wenujets[1]="<<Wenujets[1]<<";"<<endl;
      cout << "      Wmujets[0]="<<Wmujets[0]<<";"<<endl;
      cout << "      Wmujets[1]="<<Wmujets[1]<<";"<<endl;
      cout << "      WmunuHbb[0]="<<WmunuHbb[0]<<";"<<endl;
      cout << "      WmunuHbb[1]="<<WmunuHbb[1]<<";"<<endl;
      cout << "      ZeeHbb[0]="<<ZeeHbb[0]<<";"<<endl;
      cout << "      ZeeHbb[1]="<<ZeeHbb[1]<<";"<<endl;
      cout << "      ZmumuHbb[0]="<<ZmumuHbb[0]<<";"<<endl;
      cout << "      ZmumuHbb[1]="<<ZmumuHbb[1]<<";"<<endl;
      cout << "      ZnunuHbb[0]="<<ZnunuHbb[0]<<";"<<endl;
      cout << "      ZnunuHbb[1]="<<ZnunuHbb[1]<<";"<<endl;
      cout << "      ejets[0]="<<ejets[0]<<";"<<endl;
      cout << "      ejets[1]="<<ejets[1]<<";"<<endl;
      cout << "      mujets[0]="<<mujets[0]<<";"<<endl;
      cout << "      mujets[1]="<<mujets[1]<<";"<<endl;
      cout << "      ttbareHbb[0]="<< ttbareHbb[0]<<";"<<endl;
      cout << "      ttbareHbb[1]="<< ttbareHbb[1]<<";"<<endl;
      cout << "      ttbarhadHbb[0]="<<ttbarhadHbb[0]<<";"<<endl;
      cout << "      ttbarhadHbb[1]="<<ttbarhadHbb[1]<<";"<<endl;
      cout << "      ttbarmuHbb[0]="<<ttbarmuHbb[0]<<";"<<endl;
      cout << "      ttbarmuHbb[1]="<<ttbarmuHbb[1]<<";"<<endl;
      */

    }//end if MC
  
  //*******************************************************************
  //*******************************************************************

  //now that we have the values we need to fill the new globaltree
  //we can remove all the cycles of the previous tree
  f->Delete("globaldata;*");
  
  //*******************************************************************
  //*******************************************************************

  //
  // Create the global tree and save output
  // this part is the same for data and MC
  //
  TTree* copyg=new TTree("globaldata","globaldata");
  //one leaf per branch
  copyg->Branch("Entries"     ,&summed_Entries, "Entries/I");
  copyg->Branch("NGen"        ,&summed_NGen,    "NGen/I");
  copyg->Branch("my_xSect"    ,&my_xSect,       "my_xSect/D");
  copyg->Branch("my_brFrac"   ,&my_brFrac,      "my_brFrac/D");
  copyg->Branch("my_filterEff",&my_filterEff,   "my_filterEff/D");
  copyg->Branch("my_integral", &my_integral,    "my_integral/D");
  copyg->Branch("my_fraction", &my_fraction,    "my_fraction/D");
  copyg->Branch("Lumi",        &Lumi,           "Lumi/D");
  //two leaves per branch
  copyg->Branch("WenuHbb"     ,&WenuHbb, "cutMask/I:invertWord/I");
  copyg->Branch("Wenujets"    ,&Wenujets, "cutMask/I:invertWord/I");
  copyg->Branch("Wmunujets"   ,&Wmujets, "cutMask/I:invertWord/I");//note changed name from Wmujets to Wmunujets, to be consistent with Wenujets. 
  copyg->Branch("WmunuHbb"    ,&WmunuHbb, "cutMask/I:invertWord/I");
  copyg->Branch("ZeeHbb"      ,&ZeeHbb, "cutMask/I:invertWord/I");
  copyg->Branch("ZmumuHbb"    ,&ZmumuHbb, "cutMask/I:invertWord/I");
  copyg->Branch("ZnunuHbb"    ,&ZnunuHbb, "cutMask/I:invertWord/I");
  copyg->Branch("ejets"       ,&ejets, "cutMask/I:invertWord/I");
  copyg->Branch("mujets"      ,&mujets, "cutMask/I:invertWord/I");
  copyg->Branch("ttbareHbb"   ,&ttbareHbb, "cutMask/I:invertWord/I");
  copyg->Branch("ttbarhadHbb" ,&ttbarhadHbb, "cutMask/I:invertWord/I");
  copyg->Branch("ttbarmuHbb"  ,&ttbarmuHbb, "cutMask/I:invertWord/I");
  //
  if(!copyg){
    std::cout << "Creation of tree globaldata failed" << std::endl;
    return;
  }else{
    std::cout << "Tree \"globaldata\" created" << std::endl;
  }
  copyg->SetDirectory(f);
  copyg->Fill();
  copyg->Write();
  
  //*******************************************************************
  //*******************************************************************

  //everything ready, so we can write and close the file
  //f->Write();//we get more than 1 cycle, for physics we even get three cycles, so maybe this command has to go away
  f->Close();
}

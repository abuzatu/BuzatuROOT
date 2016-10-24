#include "testROOT.h"

int main(int argc, char* argv[]){
  std::cout<<" ***** Start test.exe ***** "<<std::endl;
  //will use these to count the number of seconds it took to run our code
  clock_t t_start, t_end;
  t_start=clock();

  //we decide if we want to print debug comments or not
  bool debug=false;

  //check if the correct number of arguments is given
  //the function usage is defined below
  //what is the corrent number of arguments is defined below
  //in this same file, as the method is defined there
  int u=usage(argc, argv, debug);
  if (u==-1)
    return -1;

  //if you reached here, it means the user provided the correct number
  //of arguments that we desired, so we can proceed to read the arguments
  //example how to read the input arguments of type *char
  //and how to convert them into different types
  //std::string input_file_name(argv[1]);
  //float a=atof(argv[1]);
  //float a=(double)atof(argv[1]);
  //int a=atoi(argv[1]);
  //unsigned a=(unsigned)atoi(argv[1]);
  //bool add_truth=(bool)atoi(argv[1]);

  int colour=atoi(argv[1]);

  std::cout<<"You ran: ";
  for(int i=0; i!=argc; i++)
    {
      std::cout<<" "<<argv[i];
    }
  std::cout<<std::endl; 

  //***************************************************
  //***************************************************

  TH1F* h = new TH1F("hist","hist",10,0,100);
  h->Fill(23,3);
  h->Fill(44,6);
  h->Fill(67,2);
  TCanvas* c = new TCanvas("c","c",600,400);
  change_colour_of_histogram(h,colour);
  h->Draw();
  c->Print("./output/histogram.pdf");
  delete c;
  delete h;


  //***************************************************
  //***************************************************
  
  std::cout<<" "<<std::endl;
  std::cout << "Think I'm finished!" << std::endl;
  
  t_end=clock();
  float seconds=((float)t_end-(float)t_start)/CLOCKS_PER_SEC;
  float minutes=seconds/60.0;
  float hours=seconds/3600.0;
  std::cout<<"Ran for "<<seconds<<" seconds; or "<<minutes<<" minutes, or "
	   <<hours<<" hours."<<std::endl;
  std::cout<<" ***** End test.exe ***** "<<std::endl;
  return 0;
}//end main function

int usage(int argc, char* argv[], bool debug){

  if(debug)
    {
      for(int i=0; i!=argc; i++)
	{
	  std::cout<<"arg["<<i<<"]="<<argv[i]<<std::endl;
	}
    }

  //2 as we want 1 input
  //it should be the number of inputs plus 1
  if(argc!=2)
    {

      std::cout<<"You ran: ";
      for(int i=0; i!=argc; i++)
	{
	  std::cout<<" "<<argv[i];
	}
      std::cout<<std::endl;      
      std::cout<<"Copy an example from below. Now we ABORT!"<<std::endl;
      std::cout<<"Usage: "
	       <<argv[0]
	       <<" 2"
	       <<std::endl;
      
      return -1;
    }//end if argc
  
  return 1;
}//end usage

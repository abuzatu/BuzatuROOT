{
  std::cout<<"Start rootlogon.C"<<std::endl;
  //set maximum tree size at 1TB instead of the default 1GB
  //especially useful for hadd of many files
  //TTree::SetMaxTreeSize( 1000000000000LL ); // 1 TB
  std::cout<<"End   rootlogon.C"<<std::endl;
}

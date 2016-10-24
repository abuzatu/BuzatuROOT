to do everything it is enough to do make
make

What everything means? It compiles readTree.exe, runs readTree.exe to produce the output .root file, then reads this .root file. Note how Makefile is not only used to compile files, but to do the entire project as well.

If you want individually
./createTree.exe
root.exe ./output/tree.root

or in one line:
./createTree.exe && root.exe ./output/tree.root
./createTree.exe && ./readTree.exe

ROOT documentation about trees
writing to a tree:
ftp://root.cern.ch/root/doc/ROOTUsersGuideHTML/ch12s14.html
writing to a tree your own class:
ftp://root.cern.ch/root/doc/ROOTUsersGuideHTML/ch11s03.html

*****
To see where in the code you need to change for your own class instead of Vector3D class, search in the .cxx and .h files for "//MY CLASS"


find . -name "h.cxx" | xargs grep  "MY CLASS" | less

./Vector3D.h:class Vector3D : public TObject // MY CLASS
./Vector3D.h:  ClassDef(Vector3D,1); // MY CLASS

find . -name "*.cxx" | xargs grep  "MY CLASS" | less
./Vector3D.cxx:#include "Vector3DDict.cxx" // MY CLASS
./Vector3D.cxx:ClassImp(Vector3D); // MY CLASS
./createTree.cxx:#include "Vector3D.h" //MY CLASS
./createTree.cxx:  Vector3D Vector3D_value;  //MY CLASS
./createTree.cxx:  tree->Branch("Vector3D_value",&Vector3D_value); //MY CLASS
./createTree.cxx:      Vector3D_value=Vector3D(x,y,z); //MY CLASS
./createTree.cxx:      std::cout<<"Vector3D_value="<<Vector3D_value<<std::endl; //MY CLASS
./readTree.cxx:#include "Vector3D.h" //MY CLASS
./readTree.cxx:  Vector3D* Vector3D_pointer=NULL; //MY CLASS
./readTree.cxx:  input_tree->SetBranchAddress("char_value",&char_value);//MY CLASS
./readTree.cxx:  input_tree->SetBranchAddress("Vector3D_value",&Vector3D_pointer);//MY CLASS
./readTree.cxx:    std::cout<<"Vector3D_address="<<Vector3D_pointer<<std::endl;//MY CLASS
./readTree.cxx:    std::cout<<"Vector3D_value="<<(*Vector3D_pointer)<<std::endl;//MY CLASS
./Vector3DDict.cxx:class __attribute__((annotate(R"ATTRDUMP(MY CLASS)ATTRDUMP"))) __attribute__((annotate(R"ATTRDUMP(MY CLASS)ATTRDUMP"))) __attribute__((annotate("$clingAutoload$Vector3D.h")))  Vector3D;



*****
When running make you get

Start create file Vector3DDict.cxx
End   create file Vector3DDict.cxx
Start create file createTree.exe
End   create file createTree.exe
Start run createTree.exe to create ./output/tree.root
line=0.1 0.2 0.3
v= x=0.1 y=0.2 z=0.3 module=0.374166
line=1.1 1.2 1.3
v= x=1.1 y=1.2 z=1.3 module=2.08327
line=2.1 2.2 2.3
v= x=2.1 y=2.2 z=2.3 module=3.81314
line=3.1 3.2 3.3
v= x=3.1 y=3.2 z=3.3 module=5.54437
line=4.1 4.2 4.3
v= x=4.1 y=4.2 z=4.3 module=7.27599
line=5.1 5.2 5.3 
v= x=5.1 y=5.2 z=5.3 module=9.00777
End   run createTree.exe to create ./output/tree.root
Start create file readTree.exe
End   create file readTree.exe
Start run readTree.exe
TTree test has 6 entries
 ***** new entry 0 *****
integer_value=0
float_value=0
double_value=0
char_value=0
Vector3D_address=0x295fad0
Vector3D_value= x=0.1 y=0.2 z=0.3 module=0.374166
 ***** new entry 1 *****
integer_value=1
float_value=1
double_value=1
char_value=1
Vector3D_address=0x295fad0
Vector3D_value= x=1.1 y=1.2 z=1.3 module=2.08327
 ***** new entry 2 *****
integer_value=2
float_value=2
double_value=2
char_value=2
Vector3D_address=0x295fad0
Vector3D_value= x=2.1 y=2.2 z=2.3 module=3.81314
 ***** new entry 3 *****
integer_value=3
float_value=3
double_value=3
char_value=3
Vector3D_address=0x295fad0
Vector3D_value= x=3.1 y=3.2 z=3.3 module=5.54437
 ***** new entry 4 *****
integer_value=4
float_value=4
double_value=4
char_value=4
Vector3D_address=0x295fad0
Vector3D_value= x=4.1 y=4.2 z=4.3 module=7.27599
 ***** new entry 5 *****
integer_value=5
float_value=5
double_value=5
char_value=5
Vector3D_address=0x295fad0
Vector3D_value= x=5.1 y=5.2 z=5.3 module=9.00777
End   run readTree.exe

******
to look inside the .root file
root.exe ./output/tree.root

[abuzatu@ppepc137 2]$ root.exe ./output/tree.root
   ------------------------------------------------------------
  | Welcome to ROOT 6.02/12                http://root.cern.ch |
  |                               (c) 1995-2014, The ROOT Team |
  | Built for linuxx8664gcc                                    |
  | From tag v6-02-12, 24 June 2015                            |
  | Try '.help', '.demo', '.license', '.credits', '.quit'/'.q' |
   ------------------------------------------------------------

root [0] 
Attaching file ./output/tree.root as _file0...
Warning in <TClass::Init>: no dictionary for class Vector3D is available
(class TFile *) 0x1ef20d0
root [1] test->GetEntries()
(Long64_t) 6
root [2] test->Print()
******************************************************************************
*Tree    :test      : test                                                   *
*Entries :        6 : Total =            7087 bytes  File  Size =       2297 *
*        :          : Tree compression factor =   1.04                       *
******************************************************************************
*Br    0 :integer_value : integer_value/I                                    *
*Entries :        6 : Total  Size=        610 bytes  File Size  =        104 *
*Baskets :        1 : Basket Size=      32000 bytes  Compression=   1.00     *
*............................................................................*
*Br    1 :float_value : float_value/F                                        *
*Entries :        6 : Total  Size=        600 bytes  File Size  =        102 *
*Baskets :        1 : Basket Size=      32000 bytes  Compression=   1.00     *
*............................................................................*
*Br    2 :double_value : double_value/D                                      *
*Entries :        6 : Total  Size=        637 bytes  File Size  =        115 *
*Baskets :        1 : Basket Size=      32000 bytes  Compression=   1.10     *
*............................................................................*
*Br    3 :char_value : char_value/C                                          *
*Entries :        6 : Total  Size=        615 bytes  File Size  =        121 *
*Baskets :        1 : Basket Size=      32000 bytes  Compression=   1.00     *
*............................................................................*
*Branch  :Vector3D_value                                                     *
*Entries :        6 : BranchElement (see below)                              *
*............................................................................*
*Br    4 :fUniqueID : UInt_t                                                 *
*Entries :        6 : Total  Size=        594 bytes  File Size  =         96 *
*Baskets :        1 : Basket Size=      32000 bytes  Compression=   1.04     *
*............................................................................*
*Br    5 :fBits     : UInt_t                                                 *
*Entries :        6 : Total  Size=        606 bytes  File Size  =        116 *
*Baskets :        1 : Basket Size=      32000 bytes  Compression=   1.10     *
*............................................................................*
*Br    6 :x_        : Double_t                                               *
*Entries :        6 : Total  Size=        583 bytes  File Size  =        112 *
*Baskets :        1 : Basket Size=      32000 bytes  Compression=   1.04     *
*............................................................................*
*Br    7 :y_        : Double_t                                               *
*Entries :        6 : Total  Size=        583 bytes  File Size  =        112 *
*Baskets :        1 : Basket Size=      32000 bytes  Compression=   1.04     *
*............................................................................*
*Br    8 :z_        : Double_t                                               *
*Entries :        6 : Total  Size=        583 bytes  File Size  =        111 *
*Baskets :        1 : Basket Size=      32000 bytes  Compression=   1.05     *
*............................................................................*
root [3] test->Show(0)
======> EVENT:0
 integer_value   = 0
 float_value     = 0
 double_value    = 0
 char_value      = 0
 Vector3D_value  = (Vector3D*)0x22ad810
 fUniqueID       = 0
 fBits           = 33554432
 x_              = 0.1
 y_              = 0.2
 z_              = 0.3
root [4] test->Show(1)
======> EVENT:1
 integer_value   = 1
 float_value     = 1
 double_value    = 1
 char_value      = 1
 Vector3D_value  = (Vector3D*)0x22ad810
 fUniqueID       = 0
 fBits           = 33554432
 x_              = 1.1
 y_              = 1.2
 z_              = 1.3
root [5] .q 



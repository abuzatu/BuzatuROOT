to compile:
make

to run:
./createTree.exe

to see output:
root.exe ./output/tree.root

or in one line:
make && ./createTree.exe && root.exe ./output/tree.root

root [2] test->GetEntries()
(Long64_t) 5
root [3] test->Print()
******************************************************************************
*Tree    :test      : test                                                   *
*Entries :        5 : Total =             932 bytes  File  Size =        452 *
*        :          : Tree compression factor =   1.00                       *
******************************************************************************
*Br    0 :integer_value : integer_value/I                                    *
*Entries :        5 : Total  Size=        606 bytes  File Size  =        100 *
*Baskets :        1 : Basket Size=      32000 bytes  Compression=   1.00     *
*............................................................................*
root [4] test->Show()
======> EVENT:-1
 integer_value   = 0
root [5] test->Show(0)
======> EVENT:0
 integer_value   = 0
root [6] test->Show(1)
======> EVENT:1
 integer_value   = 1
root [7] test->Show(2)
======> EVENT:2
 integer_value   = 2

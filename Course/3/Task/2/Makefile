all: readTree.exe
	@echo "Start run readTree.exe"	
	@./readTree.exe	
	@echo "End   run readTree.exe"	

createTree.exe: createTree.cxx Vector3DDict.cxx
	@echo "Start create file createTree.exe"
	@g++ createTree.cxx Vector3D.cxx -o createTree.exe `root-config --cflags` `root-config --libs`
	@echo "End   create file createTree.exe"

Vector3DDict.cxx: Vector3D.h LinkDef.h
	@echo "Start create file Vector3DDict.cxx"
	@rootcint -f Vector3DDict.cxx -c -O2 -Wall -fPIC -p Vector3D.h LinkDef.h
	@echo "End   create file Vector3DDict.cxx"

./output/tree.root: createTree.exe
	@echo "Start run createTree.exe to create ./output/tree.root"
	@./createTree.exe
	@echo "End   run createTree.exe to create ./output/tree.root"

readTree.exe: readTree.cxx ./output/tree.root
	@echo "Start create file readTree.exe"
	@g++ readTree.cxx Vector3D.cxx -o readTree.exe `root-config --cflags` `root-config --libs`
	@echo "End   create file readTree.exe"

clean:
	@echo "Start clean"
	@rm -f *.exe
	@rm -f *~
	@rm -f *Dict*
	@rm -f ./output/*		
	@echo "End   clean"

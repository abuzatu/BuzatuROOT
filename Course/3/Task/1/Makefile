all: createTree.exe

createTree.exe: createTree.C
	@g++ createTree.C -o createTree.exe `root-config --cflags` `root-config --libs`

clean:
	@rm -f *.exe
	@rm -f *~

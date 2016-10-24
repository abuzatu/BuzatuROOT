This is a skeleton of a softare package in C++. This will work out of the box by compiling and running everything. Adding new functionalities will require a minimum effort on your part, as the Make infrastructure is already done for you. This skeleton was developed by Adrian Buzatu (adrian.buzatu@glasgow.ac.uk) in 2012-2014 for his ATLAS Higgs boson research. Comments and suggestions are very welcome. In the document below explanations for the usage and how it works are presented.

make
source util/setup.sh
./bin/testROOT.exe

./bin/test2.exe

That is it! 

How does it work so magically to compile everything with just one command, make? The long document below will explain the structure of the package and of the Make commands we wrote for this package.

Belew is the one from the C++ course, may be updated for CPPROOT.

****
Package goal and structure:

The goal of such a software package is to work out directly and provide the place holders where you can put your own code, compile and run in an easy way. One of the principles of code design is to reuse the code, i.e. to not have the same piece of code in two places, but rather if we need to have the same code in two places, put it in a function, or a class, and then compile that function or class a library of code which can then be shared with any number of executable codes. Then we want to compile such libraries and such executables in an easy way, and also if a library is modified, this change to be picked up in an automatic when trying to compile the executable. The Makefile language will help us do that. 

We put some functions in the Helper folder. The function declarations are located in Helper.h and the function implementations are located in Helper.cxx. We want to be able to use such functions in many executable files or in other shared libraries.

We put a function in the Helper2 folder, which uses a function declared and defined in Helper. This will be compiled as a shared object that uses other shared objects.

We put a class in the Date folder. It is a class that is able to store a calandar date based on the year, month and day. What it knows to do is to print the values in a day and compute the number of days between a date and another date. 

We create an executable (a C++ main function) in the folder test. For test, the include statements and the function declarations we include are in test.h, such as Helper.h, Helper2.h, while the implementation of main function is in test.cxx. 

We also create another executable in the folder test2. We include this time also Helper.h and Helper2.h, but a class as well, Date. We see how we can use the shared objects in more than one exectuble, thus having reusability of our code. 

When we compile the code, we want the libriaries to be saved in a special folder, let's call it lib (from "library"). They will have the suffix ".so", from "shared object", because these libraries can be shared by many executables and thus fulfilling the goal of reusing our code. 

We want that our executable code, also called binary, to be saved in a folder called "bin" (from "binary"). We typically choose a suffix ".exe" for these files. 

If the compilation succeeds, we want to have in the folder "lib" the files "libHelper.so", "libHelper2.so" and "libDate.so", and in the folder "bin" the file "test.exe" and "test2.exe". From the main folder, we would execute by running "./bin/test.exe" or "./bin/test2.exe". These is the local path of executable files from the main folder. If you want to run only "test.exe" and to work, we need to add the "bin" folder from our package to the $PATH environment variable, by doing:
 
export PATH="$PWD/bin:$PATH"

and more details are shown at the end of this file. 

All right. So we know what we want to be the result of our compilation. The question is how to do it efficiently. After about two weeks of tweaking, I came up with a version of a Makefile that works for me. There are other ways and you can find your own. Here I explain my version. I wanted that when I create a new shared library (or executable) I just create a new folder, copy a previous library code (or executable code) and just modify the minimum possible in the Makefile. In other words, some part of the compilation will be the same irrespective of compiling a shared object or an executable, and other parts are different. I want to find the minimum code that is different and put it separately in the Makefile of each folder Date, Helper, Helper2, test, test2, while keeping the other Makefile files in the main package, Makefile.arch, Makefile.common1 and Makefile.common2 and call such folders from the Makefile from each folder. Let's see how we do it. But first let's see the tutorials on Make, as what we do we combine Make commands in our own way.

****
About Make:

A simple Makefile tuturial
http://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/

Another one:
http://www.cs.swarthmore.edu/~newhall/unixhelp/howto_makefiles.html#creating

The Make manual, for example for if statements in Make, used in my makefile in the package as well:
https://www.gnu.org/software/make/manual/html_node/Conditional-Syntax.html

Make can not only be used to automatize the compilation process, but in general in research to automatize the flow of your data analysis, when some data files are produced having other data files as an input. I highly recommand you watch this video tutorial about Make on Software Carpentry:
http://software-carpentry.org/v4/make/basics.html

****
Our Make files, the way we organise our Make commands:

Makefile.arch will define what compiler and linker and suffixes you use for the files depending on your "architecture" (hence ".arch"), or in other words your operating system. For a linux machine you may use the gcc or g++, but for a Mac you may choose "clang++" or "c++". You need to edit this folder to define the environment variable ARCH to be what you have. For the moment it has "macosx64", and it is also defined for "linuxx8664gcc", which is what a typical research computer in the physics department at Glasgow has. Then it has an if statement and for each case it defines the compilator and linker and suffixes. If you need to add something else to match your architecture, you do edit this file. So this file will allow you to compile on any machine you one, either Mac or Linux. 

For a given folder, we have two choices to make:
1. If we want to compile as a shared library, or as an executable. 
2. What shared libraries does it use. Not only an executable can use one more mare shared libraries, but also a shared library can use one or more shared libraries. 

In each folder, besides the .h and .cxx files, there is a Makefile, which looks likes this for Helper.

include ../Makefile.arch
include ../Makefile.common1

#------------------------------------------------------------------------------
COMPILE_AS=lib
WHICH_OTHER_SHARED_LIBRARIES_ARE_NEEDED_TO_COMPILE=-L$(PATH_TO_SHARED_LIBRARIES_FROM_THIS_PACKAGE) # ex: add -lBlah for Blah library
#------------------------------------------------------------------------------

include ../Makefile.common2

As we see, it starts by executing the commands from Makefile.arch, then those from Makefile.common1, then deciding the steps 1 and 2 mentioned above, and then doing Makefile.common2. As you guessed, for another folder, only the steps 1 and 2 will change, and the rest will remain the same. We are here faithful to the programming principle of reusing the code. If these many parts of the Make method are identical between all the folders of our package, we should write them in only one place and include them in all places. That way, if we want to make a change, the change will be propagated to all packages. If we had the same code with copy paste in all folders, sooner or later we will forget to update in one of the folders when the others are updated. 

Helper defines some functions, so they have no "int main function". We want to use the functions everywhere, so that is why we want to compile as a library and not as an executable, which we want to share with other programms, hence the name of "shared libraries". So we want to compile as a shared library, hence "COMPILE_AS=lib". This sets an environment variable "COMPILE_AS" to the value of "lib". This line will of course be the same for the folders Helper2 and Date, as they are also shared libraries. If we wanted an executable, we would have done "COMPILE_AS=exe", such as is done in the Makefiles of the folders test and test2. In Makefile.common2, there will be an if statement and depending of having "lib" or "exe", the compilation is done differently. 

The second element is if we use any shared libraries in our code here. We don't. That is why we have no such thing as "-lBlah" following "-L$(PATH_TO_SHARED_LIBRARIES_FROM_THIS_PACKAGE)", i.e. the -L and the "lib" folder of our package, where the shared libraries are located. However, the Helper2 uses Helper, so in that folder this line would like this:
WHICH_OTHER_SHARED_LIBRARIES_ARE_NEEDED_TO_COMPILE=-L$(PATH_TO_SHARED_LIBRARIES_FROM_THIS_PACKAGE) -lHelper

The class Date doesn't use Helper or Helper2, so for it this line is the same as in Helper:
WHICH_OTHER_SHARED_LIBRARIES_ARE_NEEDED_TO_COMPILE=-L$(PATH_TO_SHARED_LIBRARIES_FROM_THIS_PACKAGE)

The executable test uses Helper and Helper2, so for it the line looks like:
WHICH_OTHER_SHARED_LIBRARIES_ARE_NEEDED_TO_COMPILE=-L$(PATH_TO_SHARED_LIBRARIES_FROM_THIS_PACKAGE) -lHelper -lHelper2

The executable test 2 uses Helper, Helper2 and Date, so for it the line looks like:
WHICH_OTHER_SHARED_LIBRARIES_ARE_NEEDED_TO_COMPILE=-L$(PATH_TO_SHARED_LIBRARIES_FROM_THIS_PACKAGE) -lHelper -lHelper2 -lDate

So now you know the changes in the Makefile of folders you add in order to do what you add (i.e. be shared libraries or executables and include or not either shared libraries). 

We will continue now to explore how the Make commands work in our package.

****
Makefile.arch

When we run "make" in one folder, as seen above, the contents of this file get executed. First it executes the Makefile.arch from the previous folder (hence the "../"), and the compiler, linker and suffixes are defined as as a function of our operating system. 

# Choose between these options or add your own option"Mac", "GlasgowPPE", "GlasgowLab"
# don't put quotes and don't put a space after the variable, to be sure, add a comment when the name ends
WHERE_I_RUN=Mac
ifeq ($(WHERE_I_RUN),Mac)
ARCH=macosx64
MACOSXTARGET=10.9   
else ifeq ($(WHERE_I_RUN),GlagsowPPE)
ARCH=linuxx8664gcc
else ifeq ($(WHERE_I_RUN),GlasgowLab)
ARCH=linuxx8664gcc
endif

# by using this the code runs faster; with latest compilers even -O3 can be used instead
OPT          =-O2

ifeq ($(ARCH),linuxx8664gcc)
# AMD Opteron and Intel EM64T (64 bit mode) Linux with gcc 3.x
CXX           =g++
CXXFLAGS      =$(OPT) -Wall -fPIC
LD            =g++
LDFLAGS       =$(OPT)
SOFLAGS       =-shared
endif

ifeq ($(ARCH),macosx64)
# MacOS X >= 10.4 with gcc 64 bit mode (GNU gcc 4.*)
CXX           =clang++
CXXFLAGS      =$(OPT) -pipe -Wall -W -Woverloaded-virtual
LD            =clang++
LDFLAGS       =$(OPT) -mmacosx-version-min=$(MACOSXTARGET)
SOFLAGS       =-dynamiclib -single_module
endif

I have to edit this file to tell it on what computer I run, as sometimes I can run from home from my Mac, or from the office on a Linux machine, or from the computer Lab on a different type of linux machine. Based on that, there is an if statement that sets the ARCH variable (architecture). Then based on the architecture here is an if statement that sets what compiler do we use (g++ for Linux and clang++ for Mac, for example), what compilation options we use (-O2 makes the code compile slower, but in the end run much faster; newer compilers may even have -O3 available), what options (flags) are used such as -Wall which turns off a lot of the compiler warnings, and SOFLAGS, which are to be added if we want to compile as a shared library (if not present, the compiler will compile as an executable). 

All this has done is set up enviroment variables based on my computer operating system, such that in the end I can use the same compilation code for all situations.

****

Then "Makefile.common1" from the previous folder is executed, which is common for all folders in our package, be it shared objects or executables. Then come some things that ar specific for this folder (as shared library). Then comes again something that is common for all folders, be it either shared objects or executables. 

PATH_TO_OBJECTS_FROM_THIS_PACKAGE=$(shell cd ../obj; echo `pwd`)
PATH_TO_SHARED_LIBRARIES_FROM_THIS_PACKAGE=$(shell cd ../lib; echo `pwd`)
PATH_TO_BINARIES_FROM_THIS_PACKAGE=$(shell cd ../bin; echo `pwd`)
NAME_OF_CURRENT_FOLDER=$(shell basename `pwd`)

Again we define some environment variables whose long names speak for themselves to the folders of objects (obj), shared libraries (lib), executables (bin), as well as of the current folder that we compile. The "shell" work means that the follwoing commands are just simple bash shell commands from Linux but ran inside the Makefile environment. The ";" allows to run one command after the other, written on the same line. The result of the operation is put into the variable name on the left. "pwd" gives the full path to the current folder, and "basename" removes the path gives you just the name of the current folder.

*****
Then we have the bit specific for each folder, which we have explained above, which looks like this

#------------------------------------------------------------------------------
COMPILE_AS=lib
WHICH_OTHER_SHARED_LIBRARIES_ARE_NEEDED_TO_COMPILE=-L$(PATH_TO_SHARED_LIBRARIES_FROM_THIS_PACKAGE) # ex: add -lBlah for Blah library
#------------------------------------------------------------------------------

*****

Then we have Makefile.common2, where we continue to define some environment variables and then based on those names, do the compilation in an unified way. Let's show and discuss the pieces one at a time.

# define the default suffixes that we assume in our package
HeaderSuffix=h
SourceSuffix=cxx
ObjectPath=$(PATH_TO_OBJECTS_FROM_THIS_PACKAGE)
ObjectSuffix=o
# the suffix and prefix for the output file are defined in the Makefile
# specific for each folder, as it will vary 
# depending if shared library or executable

In this package we assume the convention that all headers end in .h and all implementations in .cxx. But you can choose other conventions. You can use ".H" or ".hh" for the headers, and ".C", ".cc" or ".cpp" for the implementations. The path and suffix of the object file is independent of if I want a shared library or an executable, so we can also define it here. The compilation usually goes in two steps. The first step is called compilation and produces an object .o file. The second step is liking and takes the .o and produces a ../bin/Blah.exe file if we want an executable or ../lib/libBlah.so if we want a shared library. Another difference between shared object and executable is that we use SOFLAGS for a shard object and not use them for the executable. For this reason we create our own variable MY_SHARED_OBJECT_FLAGS that is filled with SOFLAGS for a shared object and is empty for an executable. I can then use it in the compilation below and this name will cover both cases.

# separate between shared library (lib) and executable (exe)
ifeq ($(COMPILE_AS),lib)
     # full path to ../lib
     OutputPath=$(PATH_TO_SHARED_LIBRARIES_FROM_THIS_PACKAGE)
     # convention says that we put lib in front, so libTest.so
     OutputPrefix=lib
     # convention says that the suffix is so
     OutputSuffix=so
     # if use SOFLAGS, compile as a shared library
     MY_SHARED_OBJECT_FLAGS=$(SOFLAGS)
else ifeq ($(COMPILE_AS),exe)
     # full path to ../exe
     OutputPath=$(PATH_TO_BINARIES_FROM_THIS_PACKAGE)
     # convention says there is no prefix, so Test.exe
     OutputPrefix=
     # convention says that the suffix is exe
     OutputSuffix=exe
     # if not use SOFLAGS, compile as an executable
     MY_SHARED_OBJECT_FLAGS=
endif

So there are two flags that I use that are specific to each folder: one piece if the object is a shared library or not (MY_SHARED_OBJECT_FLAGS) and one that tells us what shared libraries are used in the folder (WHICH_OTHER_SHARED_LIBRARIES_ARE_NEEDED_TO_COMPILE). I could enumerate both of them in my compilation code below, but it makes for a long name. So let's put them both in a new variable with a shorter name:

# combine these two flags with long names into one flat with shorter name
MY_FLAGS=$(MY_SHARED_OBJECT_FLAGS) $(WHICH_OTHER_SHARED_LIBRARIES_ARE_NEEDED_TO_COMPILE)

The next piece of code will build the names of the headar, source, object and output files, based on the varaiables defined before with the if statements. They will work therefore for all cases:

# test.h, the header file
NAME_HEA = $(NAME_OF_CURRENT_FOLDER).$(HeaderSuffix)
# test.cxx, the source file
NAME_SRC = $(NAME_OF_CURRENT_FOLDER).$(SourceSuffix)
# test.o, the object file
NAME_OBJ = $(ObjectPath)/$(NAME_OF_CURRENT_FOLDER).$(ObjectSuffix)
# ../lib/libtest.so if shared library or ../bin/test.exe if executable
NAME_OUT = $(OutputPath)/$(OutputPrefix)$(NAME_OF_CURRENT_FOLDER).$(OutputSuffix)

The mark for the output file is "-o", so we define that as well:

# this is the mark of the output file in the make command, typically -o
OutputMark=-o

Now we are ready to finally use the Make commands, as you can see them in the tutorial. A refresher ...

****

So we start from source (Date.cxx) and header (Date.h) and we want to first compile to create the object (Date.o) and then link the object to the final output file (Date.so). We can do in two steps, or we can skip the .o file and create the .so in only one step. In the commented lines you have the example of how to produce the .o, and in the code actually used you have how to skip the .o stage. 

The syntax of makefile is 

target_file: input_file1 input_file2
	     my command to create target_file

Which means that I tell the code that I want to produce an output file called "target_file" by running ny command for action, but only if my target_file doesn't exist, or if it exists, if it's older than input_file1 and input_file2. It is this feature that is the power of automatisation of Makefile. As if you already compiled the code and you run it again, the makefile will not do it again. Thus saving time. But if input_file1 was changed, running make again will compile again target_file. That way, you don't have to manually keep track of what has been changed and what not, Makefile checks it for you and updates the compilation only when needed!

But that is not all! What if input_file1 doesn't exist? The command above will act only if input_file1 exists! If it doesn't, then it will look inside the same file for another rule to create input_file1, for example:

input_file1: input_file3 input_file4
	     my command to create input_file1

Now if you have changed input_file3, then Makefile will know it must recreate input_file1, and since input_file1 has been recreated, then it recreates target_file, without you having had to check which has changed and which not! That is the power of an automatised code flow, another ideal feature in software.

Now we are ready to understand our commented out code:

****

all:$(NAME_OUT)

This is a dummy target, saying that a file called "all" will be produced, but only if a file called NAME_OUT is produced first, but when we go to the rule on how to create "all", there is nothing there, which means "all" is not produced. Basically this is a way to tell Make what files you want to be created. Now Make neads a rule to crate NAME_OUT. We have two ways this can be done. It can be done in two steps (by producing the intermediate .o object files), or in one step (by skipping the intermediate .o object files). 

COMPILE_IN_HOW_MANY_STEPS=2

The user will decide 1 and 2, and then there is an if statement.

COMPILE_IN_HOW_MANY_STEPS=1
# compile in 1 step or 2 steps (producing the .o files as well)
ifeq ($(COMPILE_IN_HOW_MANY_STEPS),1)
     $(NAME_OUT):$(NAME_SRC) $(NAME_HEA)
        @echo "start compiling and linking in one step: $@"
        $(LD) $(NAME_SRC) $(CXXFLAGS) $(MY_FLAGS) $(OutputMark) $@
        @echo "end compiling and linking in one step: $@"
else ifeq ($(COMPILE_IN_HOW_MANY_STEPS),2)
     $(NAME_OUT):$(NAME_OBJ)
        @echo "start linking: $@."
        $(LD) $^ $(MY_FLAGS) $(OutputMark) $@
        @echo "end linking: $@."
     $(NAME_OBJ):$(NAME_SRC) $(NAME_HEA)
        @echo "start compiling: $@."
        $(LD) -c $< $(CXXFLAGS) $(OutputMark) $@
        @echo "end compiling: $@."
endif

If there is only one step, let's look at the code:
     $(NAME_OUT):$(NAME_SRC) $(NAME_HEA)
        @echo "start compiling and linking in one step: $@"
        $(LD) $(NAME_SRC) $(CXXFLAGS) $(MY_FLAGS) $(OutputMark) $@
        @echo "end compiling and linking in one step: $@"

What we read here is that we will recreate a file (target) called $(NAME_OUT) every time the files $(NAME_SRC) and $(NAME_HEA) have been modified. Of course, we want to recompile every time the source file or the header have been modified. We then put a tab on the next line and the rules of what we want to do. First we print some statements that we start and end to compile and link in one step. Notice we print with "echo" and we need to put "@" in front of it. This is make syntax. Notice also "$@", which is just a shortcut to the target file, i.e. the file to the left of ":", i.e. $(NAME_OUT). Now the real rule is the one in the middle.

$(LD) $(NAME_SRC) $(CXXFLAGS) $(MY_FLAGS) $(OutputMark) $@

LD=clang++
NAME_SRC=Helper.cxx
CXXFLAGS=-O2 -pipe -Wall -W -Woverloaded-virtual
MY_FLAGS=-dynamiclib -single_module -L/Users/abuzatu/Work/Code/PackageC++/lib
OutputMark=-o
$@=$(NAME_OUT)=/Users/abuzatu/Work/Code/PackageC++/lib/libHelper.so

In other words, this was just the generic way to write 
clang++ Helper.cxx -O2 -pipe -Wall -W -Woverloaded-virtual -dynamiclib -single_module -L/Users/abuzatu/Work/Code/PackageC++/lib -o /Users/abuzatu/Work/Code/PackageC++/lib/libHelper.so

The same generic way when run on Helper2 will be the same, except it will have the extra -lHelper after the -L bit, so 
clang++ Helper2.cxx -O2 -pipe -Wall -W -Woverloaded-virtual -dynamiclib -single_module -L/Users/abuzatu/Work/Code/PackageC++/lib -lHelper  -o /Users/abuzatu/Work/Code/PackageC++/lib/libHelper2.so

If you compiled test, you will have to remove "-dynamiclib -single_module" as we want an executable and this is used only for a shared object, and we want to include both the -lHelper and -lHelper2, so it would look like this:
clang++ test.cxx -O2 -pipe -Wall -W -Woverloaded-virtual  -L/Users/abuzatu/Work/Code/PackageC++/lib -lHelper -lHelper2 -lDate  -o /Users/abuzatu/Work/Code/PackageC++/bin/test.exe

****

But it can also be done in two steps:
     $(NAME_OUT):$(NAME_OBJ)
	@echo "start linking: $@."
	$(LD) $^ $(MY_FLAGS) $(OutputMark) $@
	@echo "end linking: $@."

First we have a target to $(NAME_OUT) and a prerequisite of $(NAME_OBJ) and we run 

$(LD) $^ $(MY_FLAGS) $(OutputMark) $@

where "$^" is a shortcut for all the elements on the right, which in this case is only "$(NAME_OBJ)". For the linking we need to link to the shared libraries we need and tell it if it's shared object or not, so we need both elements in $(MY_FLAGS). So for Helper it will look like this:

clang++ /Users/abuzatu/Work/Code/PackageC++/obj/Helper.o -dynamiclib -single_module -L/Users/abuzatu/Work/Code/PackageC++/lib  -o /Users/abuzatu/Work/Code/PackageC++/lib/libHelper.so

But of course, this is run only after the .o file is produced, so we need a new rule if this file is not present.

     $(NAME_OBJ):$(NAME_SRC) $(NAME_HEA)
        @echo "start compiling: $@."
        $(LD) -c $< $(CXXFLAGS) $(OutputMark) $@
        @echo "end compiling: $@."

This step is called compilation and is done before the linking. The target is the .o file and the prerequisites are the source and header files. The rule looks like this 

$(LD) -c $< $(CXXFLAGS) $(OutputMark) $@

Where "$<" means just the first element from the list of prerequisites, which means just $(NAME_SRC). Sure, we want to recompile also when just $(NAME_HEA) is changed, that is why we put it in the list of prerequisites. But to compile we only need $(NAME_SRC), as $(NAME_HEA) is called inside $(NAME_SRC) anyway. For Helper this would look like this:

clang++ -c Helper.cxx -O2 -pipe -Wall -W -Woverloaded-virtual -o /Users/abuzatu/Work/Code/PackageC++/obj/Helper.o

*****
The way the comamnds look like are printed on the screen when you do the compilation anyway. In two steps for Helper it looks like this:

start compiling: /Users/abuzatu/Work/Code/PackageC++/obj/Helper.o.
clang++ -c Helper.cxx -O2 -pipe -Wall -W -Woverloaded-virtual -o /Users/abuzatu/Work/Code/PackageC++/obj/Helper.o
end compiling: /Users/abuzatu/Work/Code/PackageC++/obj/Helper.o.
start linking: /Users/abuzatu/Work/Code/PackageC++/lib/libHelper.so.
clang++ /Users/abuzatu/Work/Code/PackageC++/obj/Helper.o -dynamiclib -single_module -L/Users/abuzatu/Work/Code/PackageC++/lib  -o /Users/abuzatu/Work/Code/PackageC++/lib/libHelper.so
end linking: /Users/abuzatu/Work/Code/PackageC++/lib/libHelper.so.

And in one step for Helper it looks like this.

start compiling and linking in one step: /Users/abuzatu/Work/Code/PackageC++/lib/libHelper.so
clang++ Helper.cxx -O2 -pipe -Wall -W -Woverloaded-virtual -dynamiclib -single_module -L/Users/abuzatu/Work/Code/PackageC++/lib  -o /Users/abuzatu/Work/Code/PackageC++/lib/libHelper.so
end compiling and linking in one step: /Users/abuzatu/Work/Code/PackageC++/lib/libHelper.so

*****
If the code is compiled and we run make again, nothing happens. That is the whole point. You run it but it compiles only when it's necessary. Sometimes yo may want to remove the old compilations (the .o and .exe or .so files) so that it will be forced to recompile. You do that with 

make clean

That means that you define a new rule having as target clean, that has no dependencies, i.e. it's always done when called upon, and the rules are removing the files. Of course, we can put several commands in the rule.

clean:
	@rm -f ${NAME_OBJ}
	@rm -f ${NAME_OUT}
	@rm -f ynamiclib
	@rm -f *~
	@rm -f *.pcm
	@rm -f \#*
	@echo "done: cleaning for $(NAME_OF_CURRENT_FOLDER)."

I run "make clean" so that I recompile in 2 steps after having compiled in 1 step, to see the different effects. But sometimes it is necessary in a complex package when some folder does not compile, when it depends on other folders, to just uncompile everything and start again. 

*****
If the compilation does not work, we may want to read the explict values of the abtract terms we have in our compilation. We can do that by creating a new rule info that will use "@echo" to print the values of these variables. Then we run "make info"

info:
	@echo "WHERE_I_RUN=$(WHERE_I_RUN)"
	@echo "ARCH=$(ARCH)"
	@echo "MACOSXTARGET=$(MACOSXTARGET)"
	@echo "OPT=$(OPT)"
	@echo "CXX=$(CXX)"
	@echo "CXXFLAGS=$(CXXFLAGS)"
	@echo "LD=$(LD)"
	@echo "LDFLAGS=$(LDFLAGS)"
	@echo "SOFLAGS=$(SOFLAGS)"
	@echo "PATH_TO_SHARED_LIBRARIES_FROM_THIS_PACKAGE=$(PATH_TO_SHARED_LIBRARIES_FROM_THIS_PACKAGE)"
	@echo "PATH_TO_BINARIES_FROM_THIS_PACKAGE=$(PATH_TO_BINARIES_FROM_THIS_PACKAGE)"
	@echo "NAME_OF_CURRENT_FOLDER=$(NAME_OF_CURRENT_FOLDER)"
	@echo "COMPILE_AS=$(COMPILE_AS)"
	@echo "COMPILE_IN_HOW_MANY_STEPS=$(COMPILE_IN_HOW_MANY_STEPS)"
	@echo "MY_SHARED_OBJECT_FLAGS=$(MY_SHARED_OBJECT_FLAGS)"
	@echo "WHICH_OTHER_SHARED_LIBRARIES_ARE_NEEDED_TO_COMPILE=$(WHICH_OTHER_SHARED_LIBRARIES_ARE_NEEDED_TO_COMPILE)"
	@echo "MY_FLAGS=$(MY_FLAGS)"
	@echo "NAME_HEA=$(NAME_HEA)"
	@echo "NAME_SRC=$(NAME_SRC)"
	@echo "NAME_OBJ=$(NAME_OBJ)"
	@echo "NAME_OUT=$(NAME_OUT)"



****
So now we are ready to compile all our files one by one


cd Helper 
make
cd ..
cd Helper2 
make
cd ..
cd Date
make
cd ..
cd test
make 
cd ..
cd test2
make 
cd ..

But we can have a shorter way. I can compile a folder from outside the folder by providing the path to the folder, either relative or absolute with "-C".

Macintosh-4:PackageWithoutROOT abuzatu$ pwd
/Users/abuzatu/Work/Code/PackageWithoutROOT

make -C Helper
make -C Helper2
make -C Date
make -C test
make -C test2

The order of course matters. Since test needs the shared library Date, Date should be compiled before test. Same for Helper before test.

If we want to uncompile all of them (remove all the .so and .exe files) we do

make clean -C Helper
make clean -C Helper2
make clean -C Date
make clean -C test
make clean -C test2

Now we want to automatize this even more, so we create a file Makefile in the main folder. We want it to run for us, so based on what we learn above we put a rule:

all:
        @make -C Helper
        @make -C Helper2
        @make -C Date
        @make -C test
        @make -C test2
        @echo "done: make for all."

this means it takes no input, but when you run simply make it runs all these commands.

and another rule 

clean:
        @make clean -C Helper
        @make clean -C Helper2
        @make clean -C Date
        @make clean -C test
        @make clean -C test2
        @rm -f *~
        @rm -f \#*
        @echo "done: make clean for all."

****
Now can simply run from the main folder:

Macintosh-4:PackageC++ abuzatu$ make clean
Macintosh-4:PackageC++ abuzatu$ make
Macintosh-4:PackageC++ abuzatu$ ls lib
libDate.so    libHelper.so  libHelper2.so
Macintosh-4:PackageC++ abuzatu$ ls bin
test.exe  test2.exe

Now we can try to run 
./bin/test.exe

But it is crashes, though the file exists. 
[abuzatu@ppepc137 PackageC++]$ ./bin/test.exe 
./bin/test.exe: error while loading shared libraries: libHelper.so: cannot open shared object file: No such file or directory

If you run on a Mac, it will work, but on Linux there is a need of an extra step. At compile time, the libraries were taken from $(LIBS_MINE) and the compilation worked. But at run time, the computer doesn't remember where our libraries are. For this reason we need to add $(LIBS_MINE) to the $(LD_LIBRARY_PATH), which we have to do every time you start a new terminal from the main folder as

Macintosh-4:PackageWithoutROOT abuzatu$ pwd
/Users/abuzatu/Work/Code/PackageWithoutROOT

echo ${LD_LIBRARY_PATH}
export LD_LIBRARY_PATH="${PWD}/lib:${LD_LIBRARY_PATH}"
echo ${LD_LIBRARY_PATH}

As you see, this adds the full path of the lib folder, assuming we are running from the current folder to the LD_LIBRARY_PATH. We also print the path before and after to see the change.

Since this is something we need to run anytime, we put that in a script in the util folder of the package.

Macintosh-4:PackageC++ abuzatu$ pwd
/Users/abuzatu/Work/Code/PackageC++

source util/setup.sh

Now running will work
./bin/test.exe

Now we run again and it works. We obtain:

***** Start test.exe ***** 
You ran:  ./bin/test.exe
 
a=3 b=4 sum in quadrature=5
a=3 a*a=9
square of a=3 is 9 
Think I'm finished!
Ran for 0.00014 seconds; or 2.33333e-06 minutes, or 3.88889e-08 hours.
 ***** End test.exe ***** 

Notice the output of add_in_quadrature(a,b) and squre(a) defined in Helper.
a=3 b=4 sum in quadrature=5
a=3 a*a=9

Notice the output of the print_square(a) function defined in Helper2.
square of a=3 is 9 

Then run ./bin/test2.exe

 ***** Start test2.exe ***** 
You ran:  ./bin/test2.exe
 
a=3 b=4 sum in quadrature=5
a=3 a*a=9
square of a=3 is 9 
Year=2014 Month=3 Day=8
Year=2014 Month=3 Day=30
days_date1_date2=22
 
Year=2012 Month=2 Day=23
Year=2014 Month=3 Day=14
days_date1_date2=750
 
Think I'm finished!
Ran for 0.000291 seconds; or 4.85e-06 minutes, or 8.08333e-08 hours.
 ***** End test2.exe ***** 

Notice the extra example with Date objects, defined in the class date. We got two dates and it computed the number of days between them. Play with it by changing the dates, put also date2 before date1 and see what happens.

****

In summary, when you start a new terminal and the code is not compiled, you do:

cd /Users/abuzatu/Work/Code/PackageC++
make
source ./util/setup.sh
./bin/test.exe
./bin/test2.exe

cd /Users/abuzatu/Work/Code/PackageC++
source ./util/setup.sh
./bin/test.exe
./bin/test2.exe

No ned for make, but you need to do the setup every time you open a new terminal.

****

Finally, your package will evolve in time, so it is a good practice to "tag" versions with some name in a code repository as SVN or Git, so that when you produce some results on a certain date for a certain conference or paper, you know exactly with what version of code you prepared it. In science results should be reproducible, and since we obtained our results with programming and the results would be different with different versions of the code, we save certain versions of our code to SVN or Git and we document in the file called ChangeLog what changes we brought from one version to the next. 

Now you are equipped to add your own shared libraries and executables to this package. So in the next lesson when we create our own class, we will add it and compile it as a shared library, and then we will call it from another executable, for example in the project with the solar system. 

****
If we were to try to execute without given the path to the executable, we would type in the terminal simply "test.exe", and we would get an error that the command does not exist. 

Macintosh-4:PackageC++ abuzatu$ test.exe
-bash: test.exe: command not found

If we run a command, the computer will have to know in what folder it is located. For this it will look at the environment variable called PATH. 

Macintosh-4:PackageC++ abuzatu$ echo $PATH
/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/X11/bin:/usr/texbin

We see different folders separated by ":". The computer will search for our command in the first folder from the left. If found there, it will be executed. If not found there, it will search for it in the next folder. If found, it will be executed. If not, it will search in the third folder and so on. If not found in any of the folders, it will give an error that the command is not found, like in our case above. If the command is present in two folders, the one from the folder most to the left will be used. We can of course modify the value of PATH to add our bin folder, such that then we can run our executable from any folder we are in our computer, without typing the full path to it. We will add our folder to the beginning of the PATH.

export PATH="$PWD/bin:$PATH"

The environment variable $PWD means the current folder, so $PWD/bin will be the full path to our bin folder, after which we write ":" and the current value of "$PATH", and the result we write into PATH. That way PATH gets updatd. Now the environment variable PATH looks like 

Macintosh-4:PackageC++PackageWithoutROOT abuzatu$ echo $PATH
/Users/abuzatu/Work/Code/PackageC++/bin:/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/opt/X11/bin:/usr/texbin
Macintosh-4:PackageC++PackageWithoutROOT abuzatu$ 

Now we can run test and it will be found.

****
That is it! You can now add new code and compile it to your package! But there is more about Make than just compiling code!  It is very commonly used for compiling C++ code, but it is more powerful than that! In fact, it could be used to streamline the flow of your analysis automatically. 

Imagine you start with a file data1.txt which you then process with code1 to produce data2.txt, which is then processed by code2 to produce data3.txt, which is then processed by code3 to produce a latex document document.tex which is then compiled by latex to produce document.pdf. You can run one step at a time:

code1 data1.txt data2.txt
code2 data2.txt data3.txt
code3 data3.txt document.tex
pdflatex document.tex document.pdf

Now what if data1.txt changes? You have to run all these files at a time. You can put all of them in a shell script and run them all at once, sure. But what if only data2.txt changed? You can still run all at once, but you run run the first step though yuo don't need it. What if it takes too long? You can then edit manually your shell script. What if the code2 canged? You have to check again. All these steps are called book keeping and are error prone and time consuming. Why not let Makefile do it all for us? Our Makefile would like that that:

document.pdf: document.tex
document.tex: data3.txt code3
data3.txt: data2.txt code2
data2.txt: data1.txt code1

Running make will update only the files that need to be updated in ALL situations, either that we modified the data files or the code associated to them!

You can read more about how you can use Makefile in your analysis flow, including video tutorials, on the Software Carpentery website: http://software-carpentry.org/v4/make/basics.html

echo "At first, LD_LIBRARY_PATH=${LD_LIBRARY_PATH}"
echo "We add the lib folder of our package in front of it then add :, as folders are separated by :"
export LD_LIBRARY_PATH="${PWD}/lib:${LD_LIBRARY_PATH}"
echo "At end, LD_LIBRARY_PATH=${LD_LIBRARY_PATH}"


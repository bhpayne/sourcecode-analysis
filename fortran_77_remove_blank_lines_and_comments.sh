# 20120523
# Ben Payne
# remove blank lines and commented lines from Fortran 77

if [ "$#" -ne 1 ]; then
  echo "number of arguments is $#"
  echo "this script requires one argument, the name of the file"  
fi

# remove lines which start with "c" or "C" or "*"

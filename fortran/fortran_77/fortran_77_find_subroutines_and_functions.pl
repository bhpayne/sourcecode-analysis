#!/usr/bin/perl

# 20120523
# Ben Payne
# find subroutines in Fortran 77

#print "usage:   perl find.pl \< source_input.f\n\n";

# number of arguments should be zero
#$argcnt = $#ARGV + 1;
#print "number of arguments is $argcnt\n\n";

# http://stackoverflow.com/questions/2460065/how-can-i-create-a-new-file-using-a-variable-value-as-the-name-in-perl
open (SOURCEFILE, '>>main.f');
open (LISTOFSUBROUTINES, '>>list_of_subroutines.log');
open (LISTOFFUNCTIONS, '>>list_of_functions.log');

while(<STDIN>) { # read each line from input 
  my($line) = $_; # assign input to new variable "line"
  chomp($line); # removes new line character from input 
  
  # assuming commented lines and comments have been removed, detect the presence of the string "subroutine"
  if (/^subroutine/i) {
    close (SOURCEFILE);
    while ($line =~/^subroutine[ ]+([a-zA-Z0-9_]+)[ ]*\(.*/g) { # figure out what the name of the subroutine is
      print LISTOFSUBROUTINES "$1\n";
      open (SOURCEFILE, ">>subroutine_$1.f"); 
    }
  }
  if (/^function/i) {
    close (SOURCEFILE);
    while ($line =~/^function[ ]+([a-zA-Z0-9_]+)[ ]*\(.*/g) { # figure out what the name of the function is
      print LISTOFFUNCTIONS "$1\n";
      open (SOURCEFILE, ">>function_$1.f"); 
    }
  }
  print SOURCEFILE "$line\n";
}
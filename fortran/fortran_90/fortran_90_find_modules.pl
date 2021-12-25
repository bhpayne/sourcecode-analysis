#!/usr/bin/perl

use strict;
use warnings;

# 20120523
# Ben Payne
# find moduless in Fortran 90

# Grab all the content between
# MODULE nameofmodule
# and
# END MODULE


#print "usage:   perl find.pl \< source_input.f\n\n";

# number of arguments should be zero
#$argcnt = $#ARGV + 1;
#print "number of arguments is $argcnt\n\n";

open (LISTOFMODULES, '>>list_of_modules.log');

open (MODULE, ">> no_modules.f");  
while(<STDIN>) { # read each line from input 
  my($line) = $_; # assign input to new variable "line"
  chomp($line); # removes new line character from input 

  # assuming commented lines and comments have been removed, detect the presence of the string "module"
  if ( $line =~ m/^module(.*)/i) {
#     print "found $line\n";
    my($moduleName) = $line;
    $moduleName =~ s/^module[ ]+([a-zA-Z0-9_]+)/$1/i;
#     print "name of module is $moduleName";
    close(MODULE);
    open (MODULE, ">> module_$moduleName.f");
    print LISTOFMODULES "$moduleName\n";
  }
  print MODULE "$line\n";
  if ( $line =~ m/^end module(.*)/i) {
    close MODULE;
    open (MODULE, ">> no_modules.f");  
  }
}
close MODULE;
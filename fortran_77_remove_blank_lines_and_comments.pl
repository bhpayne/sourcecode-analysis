#!/usr/local/bin/perl

# 20120523
# Ben Payne
# remove blank lines and commented lines from Fortran 77
# Note: this might be simpler in a shell script using sed
# see http://www.troubleshooters.com/codecorn/littperl/perlreg.htm#StringSelections
# and http://www.regular-expressions.info/perl.html

#print "Useage:   perl remove.pl \< commented_source_input.f \> cleaned_source_output.f\n\n";

# number of arguments should be zero
#$argcnt = $#ARGV + 1;
#print "number of arguments is $argcnt\n\n";

while(<STDIN>) { # read each line from input 
  my($line) = $_; # assign input to new variable "line"
  chomp($line); # removes new line character from input 

  # remove proceeding tabs and spaces
  $line =~ s/^[ \t]*//ig; # http://sed.sourceforge.net/sed1line.txt

  # remove trailing tabs and spaces
  $line =~ s/[ \t]*$//ig; # http://sed.sourceforge.net/sed1line.txt

  # remove lines which start with c, C, *, or a new line
  if (/^[!cC\*].*/) {
    next;# skips to the next line, so won't print
  }
 
  # remove trailing comments on remaining lines
  $line =~ s/(!.*)//ig;

  # doesn't seem to be working
  if (/^$/) { # blank line
    next;# skips to the next line, so won't print
  }

  # after completing search/replace, output result
  print "$line\n";
}

# EOF
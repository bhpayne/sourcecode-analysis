#!/usr/bin/perl
# use strict;
# use warnings;

# perl fortran_77_subroutine_and_functiondependendencies.pl > graphme.dot
# neato -Tpng graphme.dot > subroutine_and_function_graph.png

# this script assumes 
#   bash fortran_77_create_list_of_common_sub_and_func.sh
# has already been run. This generates a folder containing
# list_of_subroutines.log
# list_of_functions.log
# main.f
# function_*
# subroutine_*

$foldr="Allison_transfer_double_capture.mpi";
#foldr=Esam_molecule_4dw.mpi

# for file in $foldr/function_*; do
#   #echo $file
#   for line in $(cat "./$file"); do
#     printf "${line}\n"
#   done
# #   look for "call " and capture the string after that
# #   make a new file with GraphViz syntax
# done

print "digraph F77Dependencies {\n";
print "label=\"$foldr\"; \n";
# http://stackoverflow.com/questions/3428448/reducing-graph-size-in-graphviz
print "ranksep=1.25; \n";
print "nodes[nodesep=0.75]; \n";

print "main [fillcolor=red, style=\"filled\", shape=circle]";

open ALL_SUBROUTINES, "<$foldr/list_of_subroutines.log" or die $!;
while (my $each_subrtn = <ALL_SUBROUTINES>) {
  chomp($each_subrtn);
  print "$each_subrtn [shape=box]\n"; # http://www.graphviz.org/doc/info/shapes.html
}
close ALL_SUBROUTINES;

open ALL_FUNCTIONS, "<$foldr/list_of_functions.log" or die $!;
while (my $each_func = <ALL_FUNCTIONS>) {
  chomp($each_func);
  print "$each_func [fillcolor=yellow, style=\"rounded,filled\", shape=diamond]\n";
}
close ALL_FUNCTIONS;

# main calls subroutine
open MAIN_FILE, "<$foldr/main.f" or die $!;
while (my $main_line = <MAIN_FILE>) {
  chomp($main_line);
  #print "$main_line\n";
  if ($main_line =~ /call/i) {
    $this_line=$main_line;
    # figure out the name of the subroutine on that line
    $this_line =~ s/[ ]*call[ ]*(.*)\((.*)/\1/ig;
    # after completing search/replace, output result
    #print "subroutine contains a call to $this_line\n";

    # http://www.perlmonks.org/?node_id=887141
    # You have to reset the second file-handle so it starts reading from the very beginning for each step of outer loop
    open LIST_OF_SUBROUTINES, "<$foldr/list_of_subroutines.log" or die $!;
    while (my $subrtn_list = <LIST_OF_SUBROUTINES>) {
      chomp($subrtn_list);
      #print "list of subroutines contains $subrtn_list and\n";
      if ($subrtn_list eq $this_line) {
        print "main -> $subrtn_list\n";
#       } else {
#         print "$subrtn_list is not the same as $this_line\n";
      }
    }
    close LIST_OF_SUBROUTINES;
  }
}
close MAIN_FILE;

# subroutine calls subroutine
open ALL_SUBROUTINES, "<$foldr/list_of_subroutines.log" or die $!;
while (my $each_subrtn = <ALL_SUBROUTINES>) {
  chomp($each_subrtn);
  #print "$each_subrtn asdf\n";
  open SUBROUTINE_FILE, "<$foldr/subroutine_$each_subrtn.f" or die $!;
  while (my $subrtn_line = <SUBROUTINE_FILE>) {
    chomp($subrtn_line);
    #print "$subrtn_line\n";
    if ($subrtn_line =~ /call/i) {
      $this_line=$subrtn_line;
      # figure out the name of the subroutine on that line
      $this_line =~ s/[ ]*call[ ]*(.*)\((.*)/\1/ig;
      # after completing search/replace, output result
      #print "subroutine contains a call to $this_line\n";

      # http://www.perlmonks.org/?node_id=887141
      # You have to reset the second file-handle so it starts reading from the very beginning for each step of outer loop
      open LIST_OF_SUBROUTINES, "<$foldr/list_of_subroutines.log" or die $!;
      while (my $subrtn_list = <LIST_OF_SUBROUTINES>) {
        chomp($subrtn_list);
        #print "list of subroutines contains $subrtn_list and\n";
        if ($subrtn_list eq $this_line) {
          print "$each_subrtn -> $subrtn_list\n";
  #       } else {
  #         print "$subrtn_list is not the same as $this_line\n";
        }
      }
      close LIST_OF_SUBROUTINES;
    }
  }
  close SUBROUTINE_FILE;
}
close ALL_SUBROUTINES;

# function calls subroutine
open ALL_FUNCTIONS, "<$foldr/list_of_functions.log" or die $!;
while (my $each_func = <ALL_FUNCTIONS>) {
  chomp($each_func);
  #print "$each_func asdf\n";
  open FUNCTION_FILE, "<$foldr/function_$each_func.f" or die $!;
  while (my $func_line = <FUNCTION_FILE>) {
    chomp($func_line);
    #print "$func_line\n";
    if ($func_line =~ /call/i) {
      $this_line=$func_line;
      # figure out the name of the subroutine on that line
      $this_line =~ s/[ ]*call[ ]*(.*)\((.*)/\1/ig;
      # after completing search/replace, output result
      #print "subroutine contains a call to $this_line\n";

      # http://www.perlmonks.org/?node_id=887141
      # You have to reset the second file-handle so it starts reading from the very beginning for each step of outer loop
      open LIST_OF_SUBROUTINES, "<$foldr/list_of_subroutines.log" or die $!;
      while (my $subrtn_list = <LIST_OF_SUBROUTINES>) {
        chomp($subrtn_list);
        #print "list of subroutines contains $subrtn_list and\n";
        if ($subrtn_list eq $this_line) {
          print "$each_func -> $subrtn_list\n";
  #       } else {
  #         print "$subrtn_list is not the same as $this_line\n";
        }
      }
      close LIST_OF_SUBROUTINES;
    }
  }
  close FUNCTION_FILE;
}
close ALL_FUNCTIONS;

# subroutine -> function
open ALL_SUBROUTINES, "<$foldr/list_of_subroutines.log" or die $!;
while (my $each_subrtn = <ALL_SUBROUTINES>) {
  chomp($each_subrtn);
  #print "$each_subrtn asdf\n";
  open SUBROUTINE_FILE, "<$foldr/subroutine_$each_subrtn.f" or die $!;
  while (my $subrtn_line = <SUBROUTINE_FILE>) {
    chomp($subrtn_line);
    #print "$subrtn_line\n";

    open ALL_FUNCTIONS, "<$foldr/list_of_functions.log" or die $!;
    while (my $this_func = <ALL_FUNCTIONS>) {
      chomp($this_func);

      if ($subrtn_line =~ /(.*)[= ]*$this_func\(/i) {
            print "$each_subrtn -> $this_func\n";
      }
    }
    close ALL_FUNCTIONS;
  }
  close SUBROUTINE_FILE;
}
close ALL_SUBROUTINES;

# function -> function
open ALL_FUNCTIONS, "<$foldr/list_of_functions.log" or die $!;
while (my $each_func = <ALL_FUNCTIONS>) {
  chomp($each_func);
  #print "$each_func asdf\n";
  open FUNCTION_FILE, "<$foldr/function_$each_func.f" or die $!;
  while (my $func_line = <FUNCTION_FILE>) {
    chomp($func_line);
    #print "$func_line\n";

    open THESE_FUNCTIONS, "<$foldr/list_of_functions.log" or die $!;
    while (my $this_func = <THESE_FUNCTIONS>) {
      chomp($this_func);

      if ($func_line =~ /(.*)[= ]*$this_func\(/i) {
            print "$each_func -> $this_func\n";
      }
    }
    close ALL_FUNCTIONS;
  }
  close SUBROUTINE_FILE;
}
close ALL_FUNCTIONS;


print "overlap=false\nfontsize=12;\n}\n";
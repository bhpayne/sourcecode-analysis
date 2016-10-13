#!/bin/bash
#20120529
#Ben Payne

# Comparison of two fortran codes:


foldr1_fortran=double_capture/transfer_double_capture.mpi.f 
foldr1=transfer_double_capture.mpi
foldr2_fortran=single_capture_and_transfer_excitation/transfer.ranger.8sections.checking.cm.pert.redo.7.18.f
foldr2=transfer_single_capture.mpi
# foldr_fortran=Uttam_Chowdhury/project_transfer_excitation/plane_wave_hyllerass_plane_wave/transfer.mpi.f

mkdir $foldr1
perl fortran_remove_blank_lines_and_comments.pl < ../../${foldr1_fortran} > no_comments.f
perl fortran_90_find_modules.pl < no_comments.f # output is no_modules.f
perl fortran_find_subroutines_and_functions.pl < no_modules.f
mv function_* ${foldr1}/
mv subroutine_* ${foldr1}/
mv main.f ${foldr1}/
mv list_of_subroutines.log ${foldr1}/
mv list_of_functions.log ${foldr1}/
mv list_of_modules.log ${foldr1}/
# perl fortran_find_subroutines_and_functions.pl < module_MyMath.f
# mmv 'subroutine_*.f' 'module_MyMath_subroutine_#1.f'
# mmv 'function_*.f' 'module_MyMath_function_#1.f'
# perl fortran_find_subroutines_and_functions.pl < module_MyBasisSet.f
# mmv 'subroutine_*.f' 'module_MyBasisSet_subroutine_#1.f'
# mmv 'function_*.f' 'module_MyBasisSet_function_#1.f'
sort ${foldr1}/list_of_subroutines.log > ${foldr1}/list_of_subroutines_sorted.log 
sort ${foldr1}/list_of_functions.log > ${foldr1}/list_of_functions_sorted.log 



mkdir $foldr2
perl fortran_remove_blank_lines_and_comments.pl < ../../${foldr2_fortran} > no_comments.f
perl fortran_90_find_modules.pl < no_comments.f # output is no_modules.f
perl fortran_find_subroutines_and_functions.pl < no_modules.f
mv function_* ${foldr2}/
mv subroutine_* ${foldr2}/
mv main.f ${foldr2}/
mv list_of_subroutines.log ${foldr2}/
mv list_of_functions.log ${foldr2}/
mv list_of_modules.log ${foldr1}/
sort ${foldr2}/list_of_subroutines.log > ${foldr2}/list_of_subroutines_sorted.log 
sort ${foldr2}/list_of_functions.log > ${foldr2}/list_of_functions_sorted.log 

comm -1 -2 ${foldr1}/list_of_functions_sorted.log ${foldr2}/list_of_functions_sorted.log > list_of_functions_with_same_name.log
comm -3 ${foldr1}/list_of_functions_sorted.log ${foldr2}/list_of_functions_sorted.log > list_of_functions_with_unique_name.log

comm -1 -2 ${foldr1}/list_of_subroutines_sorted.log ${foldr2}/list_of_subroutines_sorted.log > list_of_subroutines_with_same_name.log
comm -3 ${foldr1}/list_of_subroutines_sorted.log ${foldr2}/list_of_subroutines_sorted.log > list_of_subroutines_with_unique_name.log



#Note: for three files, use 
#comm -12 file1 file2 | comm -12 - file3

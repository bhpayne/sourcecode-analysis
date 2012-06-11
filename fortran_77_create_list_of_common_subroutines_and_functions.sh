#!/bin/bash
#20120529
#Ben Payne

# Comparison of two fortran codes:


# foldr_fortran=Esam_Ali/old_working_code/thetafast_25/molecule4dw.mpi.f
# foldr2=Esam_molecule_4dw.mpi
# foldr_fortran=Adam_Upshaw/Single_orientation/oriented.madison.f
foldr1_fortran=Allison_Harris/double_capture/transfer_double_capture.mpi.f 
foldr1=Allison_transfer_double_capture.mpi
# foldr_fortran=Allison_Harris/excitation_ionization/4dw.f90
foldr2_fortran=Allison_Harris/single_capture_and_transfer_excitation/transfer.ranger.8sections.checking.cm.pert.redo.7.18.f
foldr2=Allison_transfer_single_capture.mpi
# foldr_fortran=Hari_Chaluvadi/wavefunction_integration/asymmetric_coplane.mpi.f
# foldr_fortran=Hari_Chaluvadi/wavefunction_integration/asymmetric_perpendicular_plane.mpi.f
# foldr_fortran=Hari_Chaluvadi/wavefunction_integration/symmetric_coplane.mpi.f
# foldr_fortran=Hari_Chaluvadi/wavefunction_integration/symmetric_perpendicular_plane.mpi.f
# foldr_fortran=Uttam_Chowdhury/project_double_capture/double_var_capture.mpi.f
# foldr_fortran=Uttam_Chowdhury/project_molecular_three_body_distorted_wave_eikonal/eis_molecule.mpi.f
# foldr_fortran=Uttam_Chowdhury/project_single_capture/u_transfer_final_per.mpi.f
# foldr_fortran=Uttam_Chowdhury/project_transfer_excitation/eikonal/transfer_eikonal.mpi.f
# foldr_fortran=Uttam_Chowdhury/project_transfer_excitation/four_body_model_transfer_excitation/u_transfer_final_per.mpi.f
# foldr_fortran=Uttam_Chowdhury/project_transfer_excitation/plane_wave_hylleraas_coulomb_wave/transfer.mpi.f
# foldr_fortran=Uttam_Chowdhury/project_transfer_excitation/plane_wave_hyllerass_plane_wave/transfer.mpi.f

mkdir $foldr1
perl fortran_77_remove_blank_lines_and_comments.pl < ../../${foldr1_fortran} > out.f

perl fortran_77_find_subroutines_and_functions.pl < out.f
mv function_* ${foldr1}/
mv subroutine_* ${foldr1}/
mv main.f ${foldr1}/
mv list_of_subroutines.log ${foldr1}/
mv list_of_functions.log ${foldr1}/
rm out.f  
sort ${foldr1}/list_of_subroutines.log > ${foldr1}/list_of_subroutines_sorted.log 
sort ${foldr1}/list_of_functions.log > ${foldr1}/list_of_functions_sorted.log 

mkdir $foldr2
perl fortran_77_remove_blank_lines_and_comments.pl < ../../${foldr2_fortran} > out.f
perl fortran_77_find_subroutines_and_functions.pl < out.f
mv function_* ${foldr2}/
mv subroutine_* ${foldr2}/
mv main.f ${foldr2}/
mv list_of_subroutines.log ${foldr2}/
mv list_of_functions.log ${foldr2}/
rm out.f 
sort ${foldr2}/list_of_subroutines.log > ${foldr2}/list_of_subroutines_sorted.log 
sort ${foldr2}/list_of_functions.log > ${foldr2}/list_of_functions_sorted.log 

comm -1 -2 ${foldr1}/list_of_functions_sorted.log ${foldr2}/list_of_functions_sorted.log > list_of_functions_with_same_name.log
comm -3 ${foldr1}/list_of_functions_sorted.log ${foldr2}/list_of_functions_sorted.log > list_of_functions_with_unique_name.log

comm -1 -2 ${foldr1}/list_of_subroutines_sorted.log ${foldr2}/list_of_subroutines_sorted.log > list_of_subroutines_with_same_name.log
comm -3 ${foldr1}/list_of_subroutines_sorted.log ${foldr2}/list_of_subroutines_sorted.log > list_of_subroutines_with_unique_name.log



#Note: for three files, use 
#comm -12 file1 file2 | comm -12 - file3

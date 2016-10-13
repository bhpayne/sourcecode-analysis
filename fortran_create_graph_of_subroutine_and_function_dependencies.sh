#!/bin/bash
#20120529
#Ben Payne

# Comparison of two fortran codes:


# foldr1_fortran=old_working_code/thetafast_25/molecule4dw.mpi.f
# foldr1=molecule_4dw.mpi
# foldr1_fortran=Single_orientation/single_orientation.mpi.f
# foldr1=asymmetric_coplane.mpi
foldr1_fortran=Ola_Al-Hagan/ola_orient_phi.mpi.f
foldr1=Ola_orient.mpi
# foldr_fortran=wavefunction_integration/asymmetric_perpendicular_plane.mpi.f
# foldr_fortran=project_transfer_excitation/four_body_model_transfer_excitation/u_transfer_final_per.mpi.f
# foldr_fortran=project_transfer_excitation/plane_wave_hylleraas_coulomb_wave/transfer.mpi.f
# foldr_fortran=project_transfer_excitation/plane_wave_hyllerass_plane_wave/transfer.mpi.f

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

# need to be able to pass argument to perl: name of folder

perl fortran_77_subroutine_and_function_dependendencies.pl ${foldr1} > subroutine_and_function_graph.dot
#neato -Tpng subroutine_and_function_graph.dot > subroutine_and_function_graph_neato.png
dot -Gconcentrate=true -Tpng subroutine_and_function_graph.dot > subroutine_and_function_graph_dot.png
#twopi -Tpng subroutine_and_function_graph.dot > subroutine_and_function_graph_twopi.png
#circo -Tpng subroutine_and_function_graph.dot > subroutine_and_function_graph_circo.png
#fdp -Tpng subroutine_and_function_graph.dot > subroutine_and_function_graph_fdp.png




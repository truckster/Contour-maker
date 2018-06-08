import statusAlert, recoPreparation, contour_analyze, IO

import cPickle as pickle
from os import chdir, remove, path, getcwd
from glob import glob
import gc
import numpy as np

# input_path = "/home/gpu/Simulation/mult/new/"
input_path = "/home/gpu/Simulation/processed_sim/lala2/"
# input_path = "/home/gpu/Simulation/mult/test/"
# input_path = "/home/gpu/Simulation/test/"
# input_path = "/home/gpu/Simulation/test_short/"
# input_path = "/home/gpu/Simulation/single/"

# output_path = "/home/gpu/Simulation/Contours/"
# output_path = "/home/gpu/Analysis/muReconstruction/Output/LPMT/"

# input_path = "/home/gpu/Simulation/presentation/y/"
# output_path = "/home/gpu/Analysis/muReconstruction/Output/presentation/y/"

qreco_accuracy = []

chdir(input_path)
for folder in glob("*/"):
    '''Control, which events are useful for the analysis'''
    new_output_path = recoPreparation.create_output_path(input_path, folder, "/Contours/", input_path)

    chdir(input_path + folder)
    # TODO start new process for each file. This might solve the memory problem.
    statusAlert.processStatus("Reading file: " + str(folder))

    '''calculate PMT positions for this file'''
    PmtPositions = pickle.load(open("PMT_positions.pkl", 'rb'))

    '''collect entry and exit points of all muons in event'''
    intersec_radius = 17600
    time_resolution = 1*10**-9
    # muon_points = pickle.load(open("muon_truth.pkl", 'rb'))

    '''collect information of all photons within certain time snippet and save the separately'''
    photons_in_time_window = pickle.load(open("framed_photons.pkl", 'rb'))
    photons_of_entire_event = pickle.load(open("total_event_photons.pkl", 'rb'))

    # frame_time_cut = 10
    number_contour_level = 8

    event_photons, event_photons_diff = contour_analyze.collect_contour_data(photons_of_entire_event,
                                                                             PmtPositions,
                                                                             number_contour_level,
                                                                             axis=None)

    event_photons_dPhi, event_photons_diff_dPhi = contour_analyze.collect_contour_data(photons_of_entire_event,
                                                                                       PmtPositions,
                                                                                       number_contour_level,
                                                                                       axis="Phi")

    event_photons_dTheta, event_photons_diff_dTheta = contour_analyze.collect_contour_data(photons_of_entire_event,
                                                                                           PmtPositions,
                                                                                           number_contour_level,
                                                                                           axis="Theta")

    contour_array_total, contour_array_diff = contour_analyze.collect_contour_data(photons_in_time_window,
                                                                                   PmtPositions,
                                                                                   number_contour_level,
                                                                                   axis=None)

    contour_array_total_dPhi, contour_array_diff_dPhi = contour_analyze.collect_contour_data(photons_in_time_window,
                                                                                             PmtPositions,
                                                                                             number_contour_level,
                                                                                             axis="Phi")

    contour_array_total_dTheta, contour_array_diff_dTheta = contour_analyze.collect_contour_data(photons_in_time_window,
                                                                                                 PmtPositions,
                                                                                                 number_contour_level,
                                                                                                 axis="Theta")

    IO.pickle_safe(event_photons, new_output_path, "event_photons")
    IO.pickle_safe(event_photons_dPhi, new_output_path, "event_photons_dPhi")
    IO.pickle_safe(event_photons_dTheta, new_output_path, "event_photons_dTheta")
    IO.pickle_safe(contour_array_total, new_output_path, "contour_array_total")
    IO.pickle_safe(contour_array_diff, new_output_path, "contour_array_diff")
    # IO.pickle_safe(contour_array_total_dPhi, new_output_path, "contour_array_total_phi_rotate")
    # IO.pickle_safe(contour_array_diff_dPhi, new_output_path, "contour_array_diff_phi_rotate")
    # IO.pickle_safe(contour_array_total_dTheta, new_output_path, "contour_array_total_theta_rotate")
    # IO.pickle_safe(contour_array_diff_dTheta, new_output_path, "contour_array_diff_theta_rotate")


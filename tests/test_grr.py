from src.grr_generator import GRR, generate_grr_savename
import os


grr_path = generate_grr_savename()

if not os.path.isfile(grr_path):
    grr = GRR(grr_path)
    grr.append_log("resources\SN_A00000000002T0_DATE_06-02-2022_TIME_03-08-14.txt")

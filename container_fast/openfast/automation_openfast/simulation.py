import random
import shutil
import subprocess
import os

from automation_openfast.file_modification import modify_simulation_file
from automation_openfast.inflow_wind_types import modify_inflow_wind_binary_bladed_style
from automation_openfast.openfast_helpers import remove_extension
from automation_openfast.turbsim_wind_types import turbsim_binary_bladed_style_full_field
from automation_openfast.openfast_helpers import *
from automation_openfast.progressive_damage import *


class OpenFastSimulation:
    """
    """

    def __init__(self,
                 time_stamp,
                 openfast_model_file_path,
                 turbsim_model_file_path,
                 inflow_wind_file_path,
                 wind_type,
                 wind_speed_range,
                 progressive_mass_imbalance=False,
                 blade_structural_file="",
                 adjusting_blade_mass=0.0,
                 progressive_erosion=False,
                 airfoil_file="",
                 aerodata_file="",
                 adjusting_cl=0.0,
                 adjusting_cd=0.0):
        self.openfast_model_file_path = openfast_model_file_path
        self.turbsim_model_file_path = turbsim_model_file_path
        self.inflow_wind_model_file_path = inflow_wind_file_path
        self.wind_type = wind_type
        self.wind_speed_range = wind_speed_range
        self.simulation_input_file = None
        self.turbsim_simulation_file = None
        self.simulation_time_stamp = int(time_stamp) + random.randint(1, 200)
        self.simulation_input_file_no_extension = None
        self.simulation_directory = None
        self.progressive_mass_imbalance = progressive_mass_imbalance
        self.blade_structural_file = blade_structural_file
        self.adjusting_blade_mass = adjusting_blade_mass
        self.progressive_erosion = progressive_erosion
        self.airfoil_file = airfoil_file
        self.aerodata_file = aerodata_file
        self.adjusting_cl = adjusting_cl
        self.adjusting_cd = adjusting_cd

    def modify_turbsim_file(self):
        """

        :return:
        """
        shutil.copyfile(self.turbsim_model_file_path, self.turbsim_simulation_file)

        wind_speed = round(random.uniform(self.wind_speed_range[0], self.wind_speed_range[1]), 2)
        random_seed1 = random.randint(-2147483648, 2147483648)
        random_seed2 = random.randint(-2147483648, 2147483648)
        if self.wind_type == 4:
            with open(self.turbsim_simulation_file, 'r') as reading_file:
                lines = reading_file.read().splitlines()
                modified_lines = turbsim_binary_bladed_style_full_field(lines, random_seed1, random_seed2, wind_speed)
                with open(self.turbsim_simulation_file, 'w') as writing_lines:
                    writing_lines.write('\n'.join(modified_lines))

    def openfast_input(self):
        """

        :return:
        """
        shutil.copyfile(self.openfast_model_file_path, self.simulation_input_file)
        with open(self.simulation_input_file, "r") as reading_file:
            lines = reading_file.read().splitlines()
            modified_lines = modify_simulation_file(lines)
            with open(self.simulation_input_file, "w") as writing_file:
                writing_file.write('\n'.join(modified_lines))

    def inflow_wind(self):
        """

        :return:
        """
        with open(self.inflow_wind_model_file_path, 'r') as reading_file:
            lines = reading_file.read().splitlines()
            if self.wind_type == 4:
                modified_lines = modify_inflow_wind_binary_bladed_style(lines,
                                                                        self.turbsim_model_file_path,
                                                                        self.simulation_time_stamp)
            with open(self.inflow_wind_model_file_path, 'w') as writing_file:
                writing_file.write('\n'.join(modified_lines))

    def __enter__(self):
        fst_extension = "fst"
        turbsim_input = "inp"
        self.turbsim_simulation_file = f"{os.path.dirname(self.openfast_model_file_path)}/Wind/" \
                                       f"{define_simulation_file_name(self.simulation_time_stamp, self.turbsim_model_file_path, turbsim_input)}"
        self.simulation_input_file = f"{os.path.dirname(self.openfast_model_file_path)}/out/" \
                                     f"{define_simulation_file_name(self.simulation_time_stamp, self.openfast_model_file_path, fst_extension)}"
        self.modify_turbsim_file()
        self.openfast_input()
        self.inflow_wind()
        return self

    def __exit__(self, type, value, traceback):
        self.simulation_input_file_no_extension = remove_extension(self.simulation_input_file)
        delete_files(self.simulation_input_file)
        delete_files(f"{self.simulation_input_file_no_extension}.AD.sum")
        delete_files(f"{self.simulation_input_file_no_extension}.ED.sum")
        delete_files(f"{self.simulation_input_file_no_extension}.sum")
        delete_files(f"{self.simulation_input_file_no_extension}.UA.sum")
        delete_files(f"{self.simulation_input_file_no_extension}.SrvD.sum")
        delete_files(self.turbsim_simulation_file)
        delete_files(f"{remove_extension(self.turbsim_simulation_file)}.wnd")
        delete_files(f"{remove_extension(self.turbsim_simulation_file)}.sum")

    def run(self):
        self.__enter__()
        if self.progressive_mass_imbalance:
            increasing_mass_imbalance(self.blade_structural_file, self.adjusting_blade_mass)
        if self.progressive_erosion:
            increasing_airfoil_erosion(self.airfoil_file, self.adjusting_cl, self.adjusting_cd)
            increasing_aerodata_erosion(self.aerodata_file, self.adjusting_cl, self.adjusting_cd)

        subprocess.run(["turbsim", self.turbsim_simulation_file])
        subprocess.run(["openfast", self.simulation_input_file])
        self.__exit__(None, None, None)

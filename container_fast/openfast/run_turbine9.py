from automation_openfast.simulation import OpenFastSimulation
import sys


def main(simulation_timestamp):
    turbine9_input_file = "turbine9/turbine9.fst"
    turbsim_input_file = "turbine9/Wind/wind_model.inp"
    inflow_wind_file = "turbine9/WP_Baseline_InflowWind_12mps.dat"
    turbine9_airfoil_file = "turbine9/Airfoils/s826_1603_turbine9.dat"
    turbine9_aerodata_file = "turbine9/AeroData/s826_1603_turbine9.dat"
    turbsim_wind_type = 4
    wind_speed_range = (5, 18)

    with OpenFastSimulation(simulation_timestamp,
                            turbine9_input_file,
                            turbsim_input_file,
                            inflow_wind_file,
                            turbsim_wind_type,
                            wind_speed_range,
                            progressive_erosion=True,
                            airfoil_file=turbine9_airfoil_file,
                            aerodata_file=turbine9_aerodata_file,
                            adjusting_cl=0.015,
                            adjusting_cd=0.04) as turbine_simulation:
        turbine_simulation.run()


if __name__ == '__main__':
    timestamp = sys.argv[1]
    main(timestamp)

from automation_openfast.simulation import OpenFastSimulation
import sys


def main(simulation_timestamp):
    turbine2_input_file = "turbine2/turbine2.fst"
    turbsim_input_file = "turbine2/Wind/wind_model.inp"
    inflow_wind_file = "turbine2/WP_Baseline_InflowWind_12mps.dat"
    turbsim_wind_type = 4
    wind_speed_range = (5, 18)

    with OpenFastSimulation(simulation_timestamp,
                            turbine2_input_file,
                            turbsim_input_file,
                            inflow_wind_file,
                            turbsim_wind_type,
                            wind_speed_range) as turbine_simulation:
        turbine_simulation.run()


if __name__ == '__main__':
    timestamp = sys.argv[1]
    main(timestamp)

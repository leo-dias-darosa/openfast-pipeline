from automation_openfast.simulation import OpenFastSimulation
import sys


def main(simulation_timestamp):
    turbine5_input_file = "turbine5/turbine5.fst"
    turbsim_input_file = "turbine5/Wind/wind_model.inp"
    inflow_wind_file = "turbine5/WP_Baseline_InflowWind_12mps.dat"
    turbine5_structural_blade_file = "turbine5/Baseline_Blade_turbine5.dat"
    turbsim_wind_type = 4
    wind_speed_range = (5, 18)

    with OpenFastSimulation(simulation_timestamp,
                            turbine5_input_file,
                            turbsim_input_file,
                            inflow_wind_file,
                            turbsim_wind_type,
                            wind_speed_range,
                            progressive_mass_imbalance=True,
                            blade_structural_file=turbine5_structural_blade_file,
                            adjusting_blade_mass=0.0000083) as turbine_simulation:
        turbine_simulation.run()


if __name__ == '__main__':
    timestamp = sys.argv[1]
    main(timestamp)

from automation_openfast.simulation import OpenFastSimulation
import sys


def main(simulation_timestamp):
    turbine4_input_file = "turbine4/turbine4.fst"
    turbsim_input_file = "turbine4/Wind/wind_model.inp"
    inflow_wind_file = "turbine4/WP_Baseline_InflowWind_12mps.dat"
    turbine4_structural_blade_file = "turbine4/Baseline_Blade_turbine4.dat"
    turbsim_wind_type = 4
    wind_speed_range = (5, 18)

    with OpenFastSimulation(simulation_timestamp,
                            turbine4_input_file,
                            turbsim_input_file,
                            inflow_wind_file,
                            turbsim_wind_type,
                            wind_speed_range,
                            progressive_mass_imbalance=True,
                            blade_structural_file=turbine4_structural_blade_file,
                            adjusting_blade_mass=0.0000125) as turbine_simulation:
        turbine_simulation.run()


if __name__ == '__main__':
    timestamp = sys.argv[1]
    main(timestamp)

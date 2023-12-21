#!/bin/bash
simulation_time=$(date +%s)
landing_bucket="s3://openfast-data/landing-data"

python run_turbine6.py "$simulation_time"
turbine6_result_full_path="$(ls -t /openfast/turbine6/out/*.out | head -1)"
turbine6_file=$(basename "${turbine6_result_full_path}")
echo "copying $turbine6_file to S3 bucket"
aws s3 cp "$turbine6_result_full_path" "$landing_bucket/$turbine6_file"
echo "deleting $turbine6_file"
rm "$turbine6_result_full_path"


simulation_time=$(date +%s)
python run_turbine7.py "$simulation_time"
turbine7_result_full_path="$(ls -t /openfast/turbine7/out/*.out | head -1)"
turbine7_file=$(basename "${turbine7_result_full_path}")
echo "copying $turbine7_file to S3 bucket"
aws s3 cp "$turbine7_result_full_path" "$landing_bucket/$turbine7_file"
echo "deleting $turbine7_file"
rm "$turbine7_result_full_path"


simulation_time=$(date +%s)
python run_turbine10.py "$simulation_time"
turbine10_result_full_path="$(ls -t /openfast/turbine10/out/*.out | head -1)"
turbine10_file=$(basename "${turbine10_result_full_path}")
echo "copying $turbine10_file to S3 bucket"
aws s3 cp "$turbine10_result_full_path" "$landing_bucket/$turbine10_file"
echo "deleting $turbine10_file"
rm "$turbine10_result_full_path"


simulation_time=$(date +%s)
python run_turbine11.py "$simulation_time"
turbine11_result_full_path="$(ls -t /openfast/turbine11/out/*.out | head -1)"
turbine11_file=$(basename "${turbine11_result_full_path}")
echo "copying $turbine11_file to S3 bucket"
aws s3 cp "$turbine11_result_full_path" "$landing_bucket/$turbine11_file"
echo "deleting $turbine11_file"
rm "$turbine11_result_full_path"

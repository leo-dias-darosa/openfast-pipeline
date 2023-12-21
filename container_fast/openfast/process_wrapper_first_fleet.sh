#!/bin/bash
simulation_time=$(date +%s)
landing_bucket="s3://openfast-data/landing-data"

python run_turbine1.py "$simulation_time"
turbine1_result_full_path="$(ls -t /openfast/turbine1/out/*.out | head -1)"
turbine1_file=$(basename "${turbine1_result_full_path}")
echo "copying $turbine1_file to S3 bucket"
aws s3 cp "$turbine1_result_full_path" "$landing_bucket/$turbine1_file"
echo "deleting $turbine1_file"
rm "$turbine1_result_full_path"

simulation_time=$(date +%s)
python run_turbine2.py "$simulation_time"
turbine2_result_full_path="$(ls -t /openfast/turbine2/out/*.out | head -1)"
turbine2_file=$(basename "${turbine2_result_full_path}")
echo "copying $turbine2_file to S3 bucket"
aws s3 cp "$turbine2_result_full_path" "$landing_bucket/$turbine2_file"
echo "deleting $turbine2_file"
rm "$turbine2_result_full_path"


simulation_time=$(date +%s)
python run_turbine3.py "$simulation_time"
turbine3_result_full_path="$(ls -t /openfast/turbine3/out/*.out | head -1)"
turbine3_file=$(basename "${turbine3_result_full_path}")
echo "copying $turbine3_file to S3 bucket"
aws s3 cp "$turbine3_result_full_path" "$landing_bucket/$turbine3_file"
echo "deleting $turbine3_file"
rm "$turbine3_result_full_path"
  
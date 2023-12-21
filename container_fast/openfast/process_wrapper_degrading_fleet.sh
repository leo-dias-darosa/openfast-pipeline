#!/bin/bash
while true
  do
  simulation_time=$(date +%s)
  landing_bucket="s3://openfast-data/landing-data"
  python run_turbine4.py "$simulation_time"
  turbine4_result_full_path="$(ls -t /openfast/turbine4/out/*.out | head -1)"
  turbine4_file=$(basename "${turbine4_result_full_path}")
  echo "copying $turbine4_file to S3 bucket"
  aws s3 cp "$turbine4_result_full_path" "$landing_bucket/$turbine4_file"
  echo "deleting $turbine4_file"
  rm "$turbine4_result_full_path"

  simulation_time=$(date +%s)
  python run_turbine5.py "$simulation_time"
  turbine5_result_full_path="$(ls -t /openfast/turbine5/out/*.out | head -1)"
  turbine5_file=$(basename "${turbine5_result_full_path}")
  echo "copying $turbine5_file to S3 bucket"
  aws s3 cp "$turbine5_result_full_path" "$landing_bucket/$turbine5_file"
  echo "deleting $turbine5_file"
  rm "$turbine5_result_full_path"

  simulation_time=$(date +%s)
  python run_turbine8.py "$simulation_time"
  turbine8_result_full_path="$(ls -t /openfast/turbine8/out/*.out | head -1)"
  turbine8_file=$(basename "${turbine8_result_full_path}")
  echo "copying $turbine8_file to S3 bucket"
  aws s3 cp "$turbine8_result_full_path" "$landing_bucket/$turbine8_file"
  echo "deleting $turbine8_file"
  rm "$turbine8_result_full_path"

  simulation_time=$(date +%s)
  python run_turbine9.py "$simulation_time"
  turbine9_result_full_path="$(ls -t /openfast/turbine9/out/*.out | head -1)"
  turbine9_file=$(basename "${turbine9_result_full_path}")
  echo "copying $turbine9_file to S3 bucket"
  aws s3 cp "$turbine9_result_full_path" "$landing_bucket/$turbine9_file"
  echo "deleting $turbine9_file"
  rm "$turbine9_result_full_path"

  sleep 27m
  done

#!/bin/bash

# Define the folder path
FOLDER_PATH="./problem5-4o/"
VARIABLES="side,points,k"

# Run pipeline with the folder path as the argument
python3 pipeline.py $FOLDER_PATH

# Check if the first script succeeded
if [ $? -ne 0 ]; then
  echo "pipeline.py failed. Aborting."
  exit 1
fi

# Run extractCode with the folder path as the argument
python3 extractCode.py $FOLDER_PATH $VARIABLES

# Check if the second script succeeded
if [ $? -ne 0 ]; then
  echo "extractCode.py failed."
  exit 1
fi

echo "Both scripts ran successfully."

## Run the pipeline 10 times for both folders in sequence
#for i in {1..10}; do
#  echo "Run $i for problem2-4o"
#  FOLDER_PATH="./problem2-4o/"
#  VARIABLES="n,present,future,hierarchy,budget"
#  python3 pipeline.py $FOLDER_PATH
#  if [ $? -ne 0 ]; then
#    echo "pipeline.py failed for problem2-4o on run $i. Aborting."
#    exit 1
#  fi
#  python3 extractCode.py $FOLDER_PATH $VARIABLES
#  if [ $? -ne 0 ]; then
#    echo "extractCode.py failed for problem2-4o on run $i. Aborting."
#    exit 1
#  fi
#
#  echo "Run $i for problem3-4o"
#  FOLDER_PATH="./problem3-4o/"
#  VARIABLES="n,edges,queries"
#  python3 pipeline.py $FOLDER_PATH
#  if [ $? -ne 0 ]; then
#    echo "pipeline.py failed for problem3-4o on run $i. Aborting."
#    exit 1
#  fi
#  python3 extractCode.py $FOLDER_PATH $VARIABLES
#  if [ $? -ne 0 ]; then
#    echo "extractCode.py failed for problem3-4o on run $i. Aborting."
#    exit 1
#  fi
#done
#
#echo "All runs completed successfully."

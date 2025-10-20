#!/bin/bash

for i in {1..10}; do

  # Problem 1
  echo "Run $i for problem1-4o"
  FOLDER_PATH="./problem1-4o/"
  VARIABLES="word"
  python3 pipeline.py $FOLDER_PATH
  if [ $? -ne 0 ]; then
    echo "pipeline.py failed for problem1-4o on run $i. Aborting."
    exit 1
  fi
  python3 extractCode.py $FOLDER_PATH $VARIABLES
  if [ $? -ne 0 ]; then
    echo "extractCode.py failed for problem1-4o on run $i. Aborting."
    exit 1
  fi

#  # Problem 2
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
#  # Problem 3
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

#  # Problem 4
#  echo "Run $i for problem4-4o"
#  FOLDER_PATH="./problem4-4o/"
#  VARIABLES="nums"
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
#

#  # Problem 5
#  echo "Run $i for problem5-4o"
#  FOLDER_PATH="./problem5-4o/"
#  VARIABLES="side,points,k"
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
done

echo "All runs completed successfully."

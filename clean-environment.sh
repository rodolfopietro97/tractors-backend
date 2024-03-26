#!/bin/bash

### This script is used to clean the environment by removing old migrations, pycache files and fixtures.

# 1. Root app directory
rm -rf migrations
find . -type d -name __pycache__ -exec rm -fr {} \;

# 2. Apps folders migrations

# Define an array of directories
declare -a dirs=("users" "brands" "contacts" "customers" "companies" )

# Loop through each directory and perform the operation
for dir in "${dirs[@]}"; do
    # Remove old migrations
    rm -rf ./$dir/migrations
    rm -rf ./$dir/__pycache__

    # Create new migrations folders
    mkdir ./$dir/migrations
    touch ./$dir/migrations/__init__.py
done

echo "Cleanup done!"
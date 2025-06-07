#!/bin/bash

# GitHub Repository Push Script
# Replace YOUR_GITHUB_USERNAME with your actual GitHub username

echo "Setting up GitHub repository..."

# Configure git user (if not already done)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add remote origin (replace with your repository URL)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/Wi-Fi_first_project.git

# Verify remote was added
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main

echo "Repository pushed to GitHub successfully!"
echo "Don't forget to:"
echo "1. Update the remote URL with your actual GitHub username"
echo "2. You may need to authenticate with GitHub (username/password or token)"

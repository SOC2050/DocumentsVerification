
#!/bin/bash

# Ensure you are in the root directory of your git repository
if [ ! -d ".git" ]; then
  echo "This is not a Git repository. Exiting..."
  exit 1
fi

# Check if a remote named 'origin' exists
if ! git remote | grep -q 'origin'; then
  echo "No remote named 'origin' found. Please set it up using:"
  echo "git remote add origin https://github.com/SOC2050/DocumentsVerification.git"

  exit 1
fi

# Prompt the user for a commit message if none is provided
if [ -z "$1" ]; then
  # If no commit message is provided, use the timestamp
  commit_message="Auto-commit at $(date '+%Y-%m-%d %H:%M:%S')"
else
  # If a commit message is provided, append the timestamp
  commit_message="$1 - Auto-commit at $(date '+%Y-%m-%d %H:%M:%S')"
fi

# Add all changes (you can customize this to target specific files)
git add .

# Commit the changes with the provided or auto-generated message
git commit -m "$commit_message"

# Push the changes to the remote repository on the main branch
git push origin main

# Check the status after push
if [ $? -eq 0 ]; then
  echo "Changes have been successfully pushed to the main branch."
else
  echo "There was an error pushing the changes."
fi


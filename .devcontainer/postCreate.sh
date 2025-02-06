#!/bin/bash
set -e

# Add git configuration prompt
if [ -z "$(git config --global user.name)" ]; then
    echo "Git user.name not set. Please enter your name:"
    read -r git_name
    git config --global user.name "$git_name"
fi

if [ -z "$(git config --global user.email)" ]; then
    echo "Git user.email not set. Please enter your email:"
    read -r git_email
    git config --global user.email "$git_email"
fi

echo "Creating virtual environment..."
uv venv

echo "Activating virtual environment..."
. .venv/bin/activate

# Add virtual environment activation to .zshrc
ZSHRC="/home/vscode/.zshrc"
ACTIVATION_COMMAND="[ -f /workspaces/.venv/bin/activate ] && source /workspaces/.venv/bin/activate"

# Create .zshrc if it doesn't exist
touch "$ZSHRC"

# Add activation command if not already present
if ! grep -q "source /workspaces/.venv/bin/activate" "$ZSHRC"; then
    echo "" >> "$ZSHRC"
    echo "# Automatically activate virtual environment" >> "$ZSHRC"
    echo "$ACTIVATION_COMMAND" >> "$ZSHRC"
fi

# Install dependencies
echo "Installing dependencies..."
uv pip install -e ".[dev]"

echo "Initializing MongoDB replica set..."
if command -v mongosh &> /dev/null; then
    max_attempts=30
    attempt=1

    while [ $attempt -le $max_attempts ]; do
        echo "Attempt $attempt of $max_attempts: Checking MongoDB connection..."
        if mongosh --host mongodb:27017 --eval "db.runCommand('ping').ok" --quiet; then
            echo "MongoDB is responsive, initializing replica set..."

            # Try to initialize the replica set with proper JSON syntax
            mongosh --host mongodb:27017 --eval '
                try {
                    rs.status();
                } catch (err) {
                    rs.initiate({
                        _id: "rs0",
                        members: [
                            {
                                _id: 0,
                                host: "mongodb:27017"
                            }
                        ]
                    });
                }
            '

            # Wait for replica set to initialize
            sleep 5

            # Verify replica set status
            if mongosh --host mongodb:27017 --eval "rs.status().ok" --quiet; then
                echo "Replica set initialization completed successfully"
                break
            else
                echo "Replica set initialization failed, retrying..."
            fi
        fi

        echo "Waiting for MongoDB..."
        sleep 2
        attempt=$((attempt + 1))
    done

    if [ $attempt -gt $max_attempts ]; then
        echo "Failed to initialize MongoDB after $max_attempts attempts"
        exit 1
    fi
else
    echo "mongosh not found, please check the installation."
    exit 1
fi

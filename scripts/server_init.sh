#!/bin/bash

# Prompt user for Node.js version
read -p "Enter the Node.js version to install (e.g., 20): " NODE_VERSION

# Prompt user for temporary password for 'ansible_user'
read -sp "Enter a temporary password for 'ansible_user': " ANSIBLE_PASSWORD

# Ensure the password isn't blank
if [ -z "$ANSIBLE_PASSWORD" ]; then
    echo "\nPassword cannot be empty. Please run the script again and set a valid password."
    exit 1
fi

# Update package list and install required dependencies
sudo apt update
sudo apt install -y curl sudo

# Install NVM (Node Version Manager)
echo "\nInstalling NVM..."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash

# Load NVM
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm

# Install specified Node.js version and set it as default
echo "Installing Node.js version $NODE_VERSION..."
nvm install "$NODE_VERSION"
nvm use "$NODE_VERSION"
nvm alias default "$NODE_VERSION"

# Create user 'ansible_user'
echo "\nCreating user 'ansible_user'..."
sudo useradd -m -s /bin/bash ansible_user

# Add 'ansible_user' to the sudo group for admin privileges
echo "Adding 'ansible_user' to the sudo group..."
sudo usermod -aG sudo ansible_user

# Set the user-provided temporary password for 'ansible_user'
echo "\nSetting temporary password for 'ansible_user'..."
echo "ansible_user:$ANSIBLE_PASSWORD" | sudo chpasswd

# Configure passwordless sudo for 'ansible_user'
echo "Configuring passwordless sudo for 'ansible_user'..."
echo "ansible_user ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/ansible_user

# Ensure the user can login using SSH keys
echo "Configuring SSH key login for 'ansible_user'..."

# Create the .ssh directory and authorized_keys file
sudo mkdir -p /home/ansible_user/.ssh
sudo chmod 700 /home/ansible_user/.ssh
sudo touch /home/ansible_user/.ssh/authorized_keys
sudo chmod 600 /home/ansible_user/.ssh/authorized_keys

# Set ownership of the .ssh directory and files to 'ansible_user'
sudo chown -R ansible_user:ansible_user /home/ansible_user/.ssh

# Install Google Chrome
echo "\nInstalling Google Chrome..."

# Download the Google Chrome .deb package
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# Install the package using dpkg
sudo dpkg -i google-chrome-stable_current_amd64.deb

# Fix broken dependencies if necessary
sudo apt --fix-broken install -y

# Remove the .deb file to clean up
echo "Removing Google Chrome installer..."
rm google-chrome-stable_current_amd64.deb

# Print completion message
echo "\nNode.js version $NODE_VERSION installed and set as default."
echo "'ansible_user' has been created with sudo privileges and the specified temporary password."
echo "Passwordless sudo has been enabled for 'ansible_user'."
echo "Google Chrome has been installed successfully."
echo "You can now use 'ssh-copy-id' to copy SSH keys for 'ansible_user'."
echo "Remember to delete or disable the password after setup."

# Finish
echo "\nSetup completed successfully."

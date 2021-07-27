#!/usr/bin/env bash

# Copy SSH private key to file, if set
# This is used for talking to GitHub over an SSH connection
if [ $WAGTAIL_LOCALIZE_PRIVATE_KEY ]; then
    echo "Generating SSH config"
    SSH_DIR=/app/.ssh

    mkdir -p $SSH_DIR
    chmod 700 $SSH_DIR

    echo $WAGTAIL_LOCALIZE_PRIVATE_KEY | base64 --decode > $SSH_DIR/id_rsa

    chmod 400 $SSH_DIR/id_rsa

    cat << EOF > $SSH_DIR/config
StrictHostKeyChecking no
EOF

    chmod 600 $SSH_DIR/config

    echo "Done!"
fi

#!/usr/bin/env bash

# Exit if any individual stage fails
set -e

# Preprocess the CSS
tailwindcss -i ./styles/page.css -o ./static/styles/page.css

# Build the site
zola build

# Yeet it to my VPS
# `dev` is a server on my Tailnet

rsync -avz --delete-after ./public/ dev:~/mosiman.ca

#!/usr/bin/env sh

uid() {
    openssl rand -hex 32
}

touch .env

echo "SECRET_KEY=\"$(uid)\"" >.env
echo "STORAGE_SECRET=\"$(uid)\"" >>.env

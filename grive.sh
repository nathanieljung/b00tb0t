#!/bin/bash
cd /home/discordbot/discord
if output=$(git status --porcelain) && [ -z "$output" ]; then
	git pull --no-commit
else
	echo "ERROR: git not clean. Can't pull."
fi

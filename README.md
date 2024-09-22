# Accounts with Unused 2FA

## Overview
This project processes a Bitwarden vault in JSON format and a TOTP JSON file from https://2fa.directory/api to identify accounts that have not enabled two-factor authentication (2FA) using TOTP.

It outputs a list of supported accounts that are not currently using 2FA.

## Table of Contents

- [Features](#features)
- [Usage](#usage)

## Features

- Reads and validates a Bitwarden vault in JSON format.
- Reads and processes a TOTP JSON file.
- Identifies accounts without TOTP enabled.
- Outputs a JSON file with accounts lacking 2FA and their documentation links if one exists.

## Usage
After cloning the repo or downloading it, run it using:

```bash
python main.py <path_to_bitwarden_vault> <path_to_totp_json> <output_path>
```

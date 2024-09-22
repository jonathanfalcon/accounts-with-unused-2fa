import json
from urllib.parse import urlparse
from typing import Union
from project_types import Type_BitwardenVault, Type_TotpJson, Type_Output

# Basic function to read json files
def read_json(path: str) -> Union[Type_BitwardenVault, Type_TotpJson]:
    try:
        with open(path, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        raise FileNotFoundError(f'File not found: {path}')
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f'Error reading JSON file: {path}. The file may be malformed or empty.',
            e.doc,
            e.pos,
            e.msg
        )
    
# Basic function write json files
def write_json(path: str, output: Type_Output) -> None:
    try:
        with open(path, 'w') as json_file:
            json.dump(output, json_file, indent = 4)
    except Exception as e:
        raise IOError(f'Failed to write JSON to {path}: {e}')

# Validate Bitwarden vault structure
def validate_bitwarden_vault(bitwarden_vault: Type_BitwardenVault) -> None:
    if not isinstance(bitwarden_vault, dict):
        raise ValueError('Bitwarden vault must be a JSON object.')
    if 'items' not in bitwarden_vault:
        raise ValueError('Bitwarden vault must contain an "items" property.')
    if not isinstance(bitwarden_vault['items'], list):
        raise ValueError('The "items" property must be an array of accounts.')
    
    for index, account in enumerate(bitwarden_vault['items']):
        if not isinstance(account, dict):
            raise ValueError(f'Account at index {index} must be a JSON object.')
        if 'login' not in account:
            raise ValueError(f'Account at index {index} must contain a "login" object.')
        if 'uris' not in account['login']:
            raise ValueError(f'Account at index {index} must contain a "login" object with "uris".')
        if not isinstance(account['login']['uris'], list):
            raise ValueError(f'The "uris" property in account at index {index} must be an array.')
        if 'name' not in account:
            raise ValueError(f'Account at index {index} must have a "name" property.')
        if not isinstance(account['name'], str):
            raise ValueError(f'Account at index {index} "name" property must be a string.')

    
# Cleans up urls, returning only the top-level domain, free of subdomains
# Ex: 'https://login.example.com/account' to 'example.com'
def get_top_level_domain(uri: str) -> str:
    parsed_uri = urlparse(uri)
    uri_parts = parsed_uri.hostname.split('.')

    return '.'.join(uri_parts[-2:]) if len(uri_parts) >= 2 else parsed_uri.hostname

def get_accounts_with_unused_2fa(
        bitwarden_vault: Type_BitwardenVault,
        totp_json: Type_TotpJson
) -> Type_Output:
    supported_accounts: Type_Output = []

    for account in bitwarden_vault['items']:

        # Check each URI in the account's login URIs
        for uri_dict in account['login']['uris']:
            uri = uri_dict['uri']
            domain = get_top_level_domain(uri)
            totp_info = totp_json.get(domain)

            # If the site supports 2FA and TOTP is None, add to the result
            if totp_info and account['login']['totp'] is None:
                supported_accounts.append({
                    'name': account['name'],
                    'uri': uri,
                    'documentation': totp_info.get('documentation') or 'No documentation available.'
                })
                break # Only keeps first matching uri, if any

    return supported_accounts

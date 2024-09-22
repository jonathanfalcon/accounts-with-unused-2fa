from utils import read_json, write_json, validate_bitwarden_vault, get_top_level_domain, get_accounts_with_unused_2fa
from project_types import Type_BitwardenVault, Type_TotpJson, Type_Output
import sys

def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <path_to_bitwarden_vault> <path_to_totp_json> <output_path>")
        return

    bitwarden_vault_path = sys.argv[1]
    totp_json_path = sys.argv[2]
    output_path = sys.argv[3]

    try:
        bitwarden_vault: Type_BitwardenVault = read_json(bitwarden_vault_path)
        totp_json: Type_TotpJson = read_json(totp_json_path)

        validate_bitwarden_vault(bitwarden_vault)

        supported_accounts: Type_Output = get_accounts_with_unused_2fa(bitwarden_vault, totp_json)

        write_json(output_path, supported_accounts)

        print(f'Output saved to {output_path}')

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    main()

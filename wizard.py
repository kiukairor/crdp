#!/usr/bin/python3
"""
wizard.py: Interactive or config-driven setup for the Thales CRDP Kustomize demo

This script will:
  - Copy TLS key/cert into gw-api/tls/
  - Write the registration token into crdp/regtoken/value
  - Update crdp-routes/kustomization.yaml with namespace & hostname
  - Update crdp/kustomization.yaml with namespace & CM_HOST

Usage:
  # Interactive prompts:
  ./wizard.py

  # From config file:
  ./wizard.py --config setup.yaml

Config file format (YAML or JSON):
  crdp_namespace: my-namespace
  domain_name: example.com         # optional, for generating hostname
  crdp_hostname: crdp.example.com
  ciphertrust_host: cm.example.com
  tls_key: /path/to/tls.key
  tls_crt: /path/to/tls.crt
  regtoken: "<your-registration-token>"

"""
import argparse
import shutil
from pathlib import Path
import yaml
import subprocess

# Define file locations relative to project root
ROOT = Path(__file__).parent
GW_TLS_DIR = ROOT / 'gw-api' / 'tls'
REGTOKEN_DIR = ROOT / 'crdp' / 'regtoken'
CRDP_ROUTES_K = ROOT / 'crdp-routes' / 'kustomization.yaml'
CRDP_K = ROOT / 'crdp' / 'kustomization.yaml'


def load_config(path):
    with open(path) as f:
        return yaml.safe_load(f)


def prompt_config():
    cfg = {}
    cfg['crdp_namespace'] = input('CRDP namespace: ').strip()
    default_domain = input('Domain name (for TLS CN, optional): ').strip()
    if default_domain:
        cfg['domain_name'] = default_domain
    cfg['crdp_hostname'] = input('CRDP hostname (e.g. crdp.<domain>): ').strip()
    cfg['ciphertrust_host'] = input('CipherTrust Manager host/IP: ').strip()
    cfg['tls_key'] = input('Path to tls.key: ').strip()
    cfg['tls_crt'] = input('Path to tls.crt: ').strip()
    cfg['regtoken'] = input('Registration token: ').strip()
    return cfg


def write_tls(cfg):
    GW_TLS_DIR.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy(cfg['tls_key'], GW_TLS_DIR / 'tls.key')
        shutil.copy(cfg['tls_crt'], GW_TLS_DIR / 'tls.crt')
    except shutil.SameFileError:
        pass  # Skip if source/destination are the same


def write_regtoken(cfg):
    REGTOKEN_DIR.mkdir(parents=True, exist_ok=True)
    with open(REGTOKEN_DIR / 'value', 'w') as f:
        f.write(cfg['regtoken'])
    print(f"Wrote registration token to {REGTOKEN_DIR}/value")


def update_yaml(path, namespace, literal_key, literal_value):
    """
    Update a kustomization.yaml by replacing the namespace: line and a literal entry.
    Preserves original indentation.
    """
    lines = path.read_text().splitlines()
    updated = []
    for line in lines:
        stripped = line.lstrip()
        indent = line[:len(line) - len(stripped)]
        # match namespace
        if stripped.startswith('namespace: '):
            updated.append(f"{indent}namespace: {namespace}")
        # match literal entries like '- key=value'
        elif stripped.startswith(f'- {literal_key}='):
            updated.append(f"{indent}- {literal_key}={literal_value}")
        else:
            updated.append(line)
    path.write_text("\n".join(updated) + "\n")
    print(f"Updated {path.relative_to(ROOT)}: namespace and {literal_key}")

def main():
    parser = argparse.ArgumentParser(description='Setup CRDP Kustomize demo')
    parser.add_argument('--config', help='Path to YAML/JSON config file')
    args = parser.parse_args()

    cfg = load_config(args.config) if args.config else prompt_config()

    # Copy TLS and token
    write_tls(cfg)
    write_regtoken(cfg)

    # Update kustomizations
    update_yaml(CRDP_ROUTES_K, cfg['crdp_namespace'], 'hostname', cfg['crdp_hostname'])
    update_yaml(CRDP_K,       cfg['crdp_namespace'], 'CM_HOST',    cfg['ciphertrust_host'])

    print("\nAll files updated.")
    print("Now creating K8s objects...")

    # Create namespace (ignore if exists)
    print(f"Creating namespace '{cfg['crdp_namespace']}'...")
    subprocess.run(['kubectl', 'create', 'ns', cfg['crdp_namespace']], check=False)

    # Apply kustomize
    print("Applying kustomize overlays...")
    subprocess.run(['kubectl', 'apply', '-k', str(ROOT)], check=True)


if __name__ == '__main__':
    main()

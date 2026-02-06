# Ansible Network Hardening – Load Balancer

An Ansible project that automates network hardening for load balancer (or edge) hosts: firewall checks, port restriction to a gold standard, disabling legacy services, and generating a secure F5-style configuration from variables.

## Contents

- **`group_vars/all.yml`** – Central variables: `gold_standard_ports` (e.g. 80, 443), `min_tls_version` (e.g. 1.2), and list of legacy services to disable.
- **`harden_loadbalancer.yml`** – Playbook that applies hardening and writes the config.
- **`templates/f5_config.conf.j2`** – Jinja2 template used to generate `f5_config.conf` from those variables.
- **`inventory.yml`** (optional) – Example inventory; replace with your own.

## Quick Start

1. **Install Ansible and collections** (if needed):
   ```bash
   pip install ansible
   ansible-galaxy collection install community.general ansible.posix
   ```

2. **Set your inventory**  
   Create an `inventory.yml` (or use `-i` with your inventory) and put your load balancer hosts in a group named `loadbalancers`.

3. **Run the playbook** (use `--check` for dry run):
   ```bash
   ansible-playbook -i inventory.yml harden_loadbalancer.yml
   ```

## What the Playbook Does

1. **Firewall check** – Determines whether UFW or iptables/firewalld is in use and reports status.
2. **Restrict to gold-standard ports** – Configures the host firewall so only the ports in `gold_standard_ports` (e.g. 80, 443) are allowed (UFW on Debian/Ubuntu; firewalld on RHEL when present).
3. **Disable legacy services** – Stops and disables services listed in `legacy_services_to_disable` (e.g. `telnet`, `ftp`).
4. **Generate secure config** – Renders `templates/f5_config.conf.j2` to `/etc/loadbalancer/f5_config.conf` with TLS version, allowed ports, and disabled services reflected (dummy F5-style file for demonstration).

## NIST 800-53 Alignment (Configuration Management & Security)

This project is designed to support **NIST SP 800-53** controls around configuration management and network security.

| Control / Area | How this project supports it |
|----------------|------------------------------|
| **CM-2 (Baseline Configuration)** | A single, version-controlled baseline is defined in `group_vars/all.yml` (ports, TLS version, services to disable). The playbook applies that baseline consistently. |
| **CM-3 (Configuration Change Control)** | Changes are made through Ansible (code), not ad hoc. Playbook and vars can be reviewed and approved before execution; `--check` supports impact review. |
| **CM-6 (Configuration Settings)** | Security-related settings (allowed ports, minimum TLS, disabled services) are explicitly set and documented in YAML and in the generated `f5_config.conf`. |
| **CM-7 (Least Functionality)** | Only `gold_standard_ports` are allowed; legacy/insecure services (e.g. telnet, ftp) are disabled, reducing unnecessary and risky services. |
| **SC-7 (Boundary Protection)** | Firewall is checked and configured so only approved ports (e.g. 80, 443) are permitted, reinforcing access control at the network boundary. |
| **SC-8 (Transmission Confidentiality/Integrity)** | Use of `min_tls_version: 1.2` (and the template’s TLS/SSL settings) supports NIST guidance (e.g. 800-52) for protecting data in transit. |

By keeping the “gold standard” in variables and generating config from a template, the project supports **repeatable, auditable configuration management** in line with NIST 800-53.

## Customization

- **Ports:** Edit `gold_standard_ports` in `group_vars/all.yml`.
- **TLS:** Change `min_tls_version` in `group_vars/all.yml`; the template uses it in `f5_config.conf`.
- **Legacy services:** Add or remove entries in `legacy_services_to_disable` in `group_vars/all.yml`.

## Requirements

- Ansible 2.9+
- For UFW/firewalld tasks: `community.general` and `ansible.posix` collections (see Quick Start).
- Target hosts: Linux with UFW (Debian/Ubuntu) or firewalld (RHEL) for full automation; playbook can be adapted for other firewalls.

## License

Use and modify as needed for your environment and interview demos.

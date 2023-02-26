# CISCO_FTD Ansible Collection

The Ansible collection includes ``ftd`` terminal and cliconf plugins that allow you to use it as ``ansible_network_os`` under ``network_cli`` connection.

This collection has been tested against Cisco FTD version 7.0.1

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10,<2.11**.
<!--end requires_ansible-->

## Requirements

Nothing special.

## Installing this collection

Create a local ansible.cfg and specify the collections_paths configuration to locate the collections. See sample directory structure below
```
[defaults]
collections_paths = ./
```

### Install the latest version from GitHub

```bash
ansible-galaxy collection install git@github.com:alexkross/cisco_ftd_cli.git
```


### Install from Ansible Galaxy

    ansible-galaxy collection install alexkross.cisco_ftd_cli

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: alexkross.cisco_ftd_cli
```

### Using modules from the alexkross.cisco_ftd_cli collection in your playbooks

You can call modules by their Fully Qualified Collection Namespace (FQCN), such as `amotolani.cisco_fmc.network`.
The following example task creates Host fmc objects from a loop and deploys this configuration, using the FQCN:

```yaml
---
  - name: Show running configuration
    cli_command: show running-config
    register: reg
  - debug: var=reg.stdout
```

For obvious reasons ``cli_config`` is unsupported on a FTD gear managed under FMC. You can try other collections instead, [fmc_collections by amotolani](https://github.com/amotolani/fmc_collections) for example.

### See Also:
* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection
We are seeking contributions to help improve this collection. If you find problems, or a way to make it better, please open an issue or create a PR against the [cisco_ftd_cli collection repository](https://github.com/alexkross/cisco_ftd_cli/). 


### Code of Conduct
This collection follows the Ansible project's
[Code of Conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html).
Please read and familiarize yourself with this document.

<!--
## Release notes
Release notes are available [here](https://github.com/alexkross/cisco_ftd_cli/blob/master/CHANGELOG.rst).

## Roadmap
-->

## More information

- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible network resources](https://docs.ansible.com/ansible/latest/network/getting_started/network_resources.html)
- [Ansible Collection overview](https://github.com/fmc_collections/overview)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Developing network plugins](https://docs.ansible.com/ansible/latest/network/dev_guide/developing_plugins_network.html)
- [Cisco Firepower Threat Defence Notes](https://github.com/willrabarber/Networking/wiki/Cisco-Firepower-Threat-Defence-Notes)
- [Ansible code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.

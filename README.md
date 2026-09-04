# Efteling Wait Times

[![GitHub Release](https://img.shields.io/github/v/release/BuurmanG/Efteling-wachttijden?style=flat-square)](https://github.com/BuurmanG/Efteling-wachttijden/releases)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange?style=flat-square)](https://hacs.xyz/)
[![License](https://img.shields.io/github/license/BuurmanG/Efteling-wachttijden?style=flat-square)](https://github.com/BuurmanG/Efteling-wachttijden/blob/main/LICENSE)

A custom [Home Assistant](https://www.home-assistant.io/) integration for **Efteling** that provides current attraction wait times.

The integration retrieves the available Efteling attraction information and exposes it as sensors in Home Assistant.

## Features

* 🎢 Current wait times for Efteling attractions
* 🔄 Automatic updates through Home Assistant
* ⚙️ Configuration through the Home Assistant UI
* 🧩 Compatible with HACS as a custom repository

## Installation

[![Add Integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start?domain=efteling)
### HACS

1. Open **HACS** in Home Assistant.

2. Go to **Integrations**.

3. Open the menu in the top-right corner.

4. Select **Custom repositories**.

5. Add:

   `https://github.com/BuurmanG/Efteling-wachttijden`

6. Select **Integration** as the category.

7. Click **Add**.

8. Search for **Efteling Wait Times** and install it.

9. Restart Home Assistant.

After restarting, continue with the configuration below.

### Manual installation

1. Download or clone this repository.

2. Copy the `efteling` integration folder into:

   `config/custom_components/efteling/`

3. Restart Home Assistant.

4. Add the integration through the Home Assistant UI.

## Configuration

After installation:

1. Open **Settings → Devices & services**.
2. Select **Add Integration**.
3. Search for **Efteling**.
4. Follow the configuration steps.

No Efteling account is required.

## Sensors

The integration creates sensors for the available Efteling attractions.

Each sensor reports the current waiting time for its attraction.

Depending on the attraction and data provided by Efteling, additional information may be available as entity attributes.

## Automation examples

You can use the wait-time sensors in Home Assistant automations.

For example, you could create a notification when the waiting time for an attraction drops below a certain value:

```yaml
automation:
  - alias: "Efteling ride available"
    trigger:
      - platform: numeric_state
        entity_id: sensor.<attraction>
        below: 15
    action:
      - service: notify.notify
        data:
          message: "The waiting time is now below 15 minutes!"
```

Replace `sensor.<attraction>` with the entity created by the integration.

Example with the custom:auto_entities card:
<img width="500" height="925" alt="image" src="https://github.com/user-attachments/assets/106f967f-05e3-4bfc-9f64-9c58051a320c" />

Code:
type: custom:auto-entities
card:
  type: entities
  title: Efteling wachttijden
  show_header_toggle: false
  card_mod:
    style: |
      ha-card {
        --primary-text-color: var(--primary-color);
        --secondary-text-color: var(--primary-color);
        --paper-item-icon-color: var(--primary-color);
      }

      #states > * {
        margin: -12px 0px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
      }
filter:
  include:
    - entity_id: sensor.efteling_*_wachttijd
      options:
        type: custom:template-entity-row
        name: |
          {{ state_attr(config.entity, 'friendly_name')
             | replace(' Wachttijd', '') }}
        state: |
          {{ states(config.entity) }} min
        card_mod:
          style: |
            :host {
              --paper-item-min-height: 28px !important;
              height: 28px !important;
              margin: 0px !important;
              padding: 0px !important;

              {% set status_entity = config.entity
                 | replace('_wachttijd', '_status') %}

              {% if states(status_entity) == 'OPERATING' %}
                --paper-item-icon-color: #003366;
                color: #003366;
              {% else %}
                --paper-item-icon-color: red;
                color: red;
              {% endif %}
            }
sort:
  method: name
  ignore_case: true


## Troubleshooting

If the integration is not updating:

1. Check **Settings → Devices & services → Efteling**.
2. Check the Home Assistant logs for errors.
3. Make sure your Home Assistant installation has internet access.
4. Restart Home Assistant after updating the integration.

If you find a problem, please open an issue with:

* Home Assistant version
* Integration version
* Relevant log messages
* Steps to reproduce the problem

Please remove any personal or sensitive information from logs before posting them.

## Disclaimer

This project is **not affiliated with, endorsed by, or sponsored by Efteling**.

Efteling and its related trademarks are the property of their respective owners.

This integration is provided for personal and informational use.

## Contributing

Contributions and bug reports are welcome.

If you have an improvement or fix:

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test the integration.
5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


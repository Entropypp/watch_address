# Bitcoin Address Balance Monitor

A lightweight Python CLI tool that monitors a specific Bitcoin address for balance changes. It fetches the current balance in Satoshis using either Blockbook (Explorer) or Mempool APIs and triggers an email alert if the balance deviates from your expected amount.

## Features

* **Dual API Support:** Queries balance data using either Blockbook explorer or Mempool API formats.
* **Automated Alerts:** Triggers email notifications immediately when a balance change is detected.
* **Multi-Recipient Support:** Allows sending notifications to multiple emails separated by semicolons.
* **Self-Hosted Friendly:** Disables SSL verification warnings for users querying private or self-hosted API backends.

## API Integration Details

The script parses different JSON payload schemas depending on the `-i` / `--api` flag selection:

### 1. Blockbook API (`-i explorer`)
Queries standard Blockbook nodes using the address history endpoint. It targets the nested `txHistory` block to retrieve the current balance calculation:
```python
# Expected Blockbook JSON Response Path
return int(request.json()['txHistory']['balanceSat'])
```

### 2. Mempool API (`-i mempool`)
Queries Mempool.space or self-hosted Esplora instances. It targets the `chain_stats` block to calculate total received funds:
```python
# Expected Mempool JSON Response Path
return int(request.json()['chain_stats']['funded_txo_sum'])
```

## Prerequisites

* Python 3.x
* `requests` library

Install dependencies via pip:
```bash
pip install requests
```

## Usage

Run the script from the command line by passing the required configuration parameters.

```bash
python monitor.py -x <host> -a <btc_address> -n <nickname> -s <expected_sats> -f <from_email> -t <to_email> --server <smtp_server>
```

### Command-Line Arguments

| Short | Long | Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `-x` | `--host` | String | **Yes** | The API host domain (e.g., `mempool.space`). |
| `-a` | `--address` | String | **Yes** | The Bitcoin address to monitor. |
| `-n` | `--nickname` | String | **Yes** | A friendly name/label for the monitored address. |
| `-s` | `--sats` | Integer | **Yes** | The expected wallet balance in Satoshis. |
| `-f` | `--frm` | String | **Yes** | Sender email address. |
| `-t` | `--to` | String | **Yes** | Recipient email address(es). Separate multiple addresses with `;`. |
| `-e` | `--server` | String | **Yes** | SMTP server address. |
| `-i` | `--api` | String | No | API type schema: `explorer` (default) or `mempool`. |

### Automation Example

To run this script automatically at regular intervals, you can set up a Linux cron job:

```bash
# Open your crontab configurations
crontab -e

# Run the monitoring check every 30 minutes
*/30 * * * * /usr/bin/python3 /path/to/monitor.py -x mempool.space -a 1111111111111111111114oLvT2 -i mempool -n "Savings Wallet" -s 50000 -f alerts@example.com -t user@example.com --server ://example.com
```

## Security Note

This script connects to SMTP servers using standard TLS authentication. Be cautious when executing this via cron or shell scripts to prevent leaking sensitive infrastructure arguments or credentials in plaintext logs.

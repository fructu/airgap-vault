# AirGap Vault

<p align="left">
    <img src="./banner.png" />
</p>

> Self custody made simple and secure. Protect your crypto and store your private keys offline.

[AirGap](https://airgap.it) is a crypto wallet system that lets you secure cypto assets with one secret on an offline device. The AirGap Vault application is installed on a dedicated device that has no connection to any network, thus it is air gapped. The [AirGap Wallet](https://github.com/airgap-it/airgap-wallet) is installed on your everyday smartphone.

## Megatron version

 **Warning:** Only run https_server.py in a TailsOS where chromium is only used for this vault.

Build a web version that can be served locally inside TailOS offline.

** Once you have updated TailsOS DO NOT CONNECT IT ONLINE AGAIN then generate/import the seed **

my files:

```code
git whatchanged --author="fructu" --name-only --oneline | sort | uniq -c

.gitignore
https_server.py
lib/backup.py
lib/__init__.py
Makefile
README.md
```

You need a TailOS USB:

- [TailsOS](https://tails.net/)


So far this is based on:

- [airgap-vault](https://github.com/airgap-it/airgap-vault/)

commit 091fff8707ea5cac8670c143daade542c899bf6f (tag: v3.32.5)

Based in the github runs, because the original Build section of this document, did not work in my machine.

- https://github.com/airgap-it/airgap-vault/actions/runs/11440806117/job/31827459216

Not using netlify-cli to deploy and test
I just run the web version with python server

Developing

make sure of comment these lines in https_server.py

```code
def main():
    print("megatron.thx airgap-vault v1.0")
    #backup_previous()
    server = Process(target=https_server_run)
    server.start()
    #chromium_open()
    #server.terminate()
```

open with the browser you want

Build

you can just do just:

```bash
make clean
make all
```

```bash
$ yarn install --frozen-lockfile
$ yarn run build:no-sapling
```
Create Certificate

The cert.pem and key.pem are created using this command left all questions by default, just press enter:

```bash
$ openssl req -x509 -nodes -days 36500 -newkey rsa:2048 -keyout www/key.pem -out www/cert.pem
```

Install on Tails
- Copy airgap-vault/to_deploy to a usb.
- Once you load Tails in your computer.
- create a Persistent volumen encrypted.
- select + and add administrator password.
- Start Tails

update tails with:

```bash
sudo -s -- <<EOF
apt update
apt upgrade -y
apt full-upgrade -y
apt autoremove -y
apt autoclean -y
EOF
```

- install chromium

In TailsOS Persistent folder copy the content of to_deploy:
- airgap-vault 
- airgap-vault.tar.gz

Run

```bash
$ python3 https_server.py
```

chromium would open automatically if not you can use any other browser:

open firefox https://127.0.0.1:5000/

there will be a warning about the certificate:
Click "Advanced"
click "Accept Risk and Continue"

if you run make and you want to deploy just copy in usb and untar with:

```bash
tar -xf file_name.tar.gz
```

Vault

In TailsOS the cookies and config of chromium are stored in this 2 directories:
~/.cache/chromium
~/.config/chromium

when https_server.py runs it will restored those directories from the vault
and after is finished it does a backup from those directories inside sthe vault
because the chromium directories will be lost once Tails is shutdown.

cd .cache/
 vault/chromium_bk/cache
 vault/chromium_bk/config


## Description

AirGap Vault is responsible for secure key generation. Entropy from audio, video, touch and accelerometer are used together with the output of the hardware random number generator. The generated secret is saved in the secure enclave of the device, only accessible by biometric authentication. Accounts for multiple protcols can be created. Transactions are prepared by the AirGap Wallet and then transferred to the offline device via QR code, where it is signed and sent back to the Wallet using another QR code.

AirGap Vault is a hybrid application (using the same codebase for Android and iOS). Created using AirGap's protocol agnostic `airgap-coin-lib` library to interact with different protocols and our own secure storage implementation.

<p align="left">
    <img src="./devices.png" />
</p>

## Related Projects

- [AirGap Wallet](https://github.com/airgap-it/airgap-wallet)
- [airgap-coin-lib](https://github.com/airgap-it/airgap-coin-lib)

- [AirGap Linux Distribution](https://github.com/airgap-it/airgap-distro)
- [apk-signer](https://github.com/airgap-it/airgap-raspberry-apk-signer)

#
#
#
#

all: deploy

#compile
www/index.html:
	echo "compile"
	yarn install --frozen-lockfile
	yarn run build:no-sapling

www/cert.pem www/key.pem:
	openssl req -x509 -nodes -days 36500 -newkey \
		  rsa:2048 -keyout www/key.pem -out www/cert.pem \
		 -subj "/CN=$cn\/emailAddress=admin@$cn/C=US/ST=Ohio/L=Columbus/O=Widgets Inc/OU=Some Unit"

#deploy
deploy: to_deploy/airgap-vault.zip
	echo "creating deploy"

to_deploy/airgap-vault.zip: www/index.html create_deploy_dir www/cert.pem www/key.pem https_server.py README.md
	echo "Preparing deploy directory"
	cp -r www to_deploy/airgap-vault
	cp https_server.py to_deploy/airgap-vault
	cp -r lib to_deploy/airgap-vault
	cp README.md to_deploy/airgap-vault
	cd to_deploy;tar -czvf airgap-vault.tar.gz airgap-vault

create_deploy_dir:
	mkdir -p to_deploy/airgap-vault/vault/chromium_bk/cache/
	mkdir -p to_deploy/airgap-vault/vault/chromium_bk/config/

clean:
	rm -rf to_deploy
	rm -rf www

#
#
#
#

all: to_deploy/airgap-vault.zip

#compile
www/index.html: 
	echo "compile"
	yarn install --frozen-lockfile
	yarn run build:no-sapling

cert.pem key.pem:
	openssl req -x509 -nodes -days 36500 -newkey \
		  rsa:2048 -keyout key.pem -out cert.pem \
		 -subj "/CN=$cn\/emailAddress=admin@$cn/C=US/ST=Ohio/L=Columbus/O=Widgets Inc/OU=Some Unit"

#deploy
to_deploy/airgap-vault.zip: cert.pem key.pem https_server.py README.md www/index.html create_deploy_dir
	echo "Preparing deploy directory"
	cp -r www to_deploy/airgap-vault
	cp https_server.py to_deploy/airgap-vault
	cp README.md to_deploy/airgap-vault
	cp cert.pem to_deploy/airgap-vault
	cp key.pem  to_deploy/airgap-vault
	cd to_deploy;tar -czvf airgap-vault.tar.gz airgap-vault

create_deploy_dir:
	mkdir -p to_deploy/airgap-vault	

clean:
	rm -rf to_deploy
	rm -rf www
	rm cert.pem
	rm key.pem

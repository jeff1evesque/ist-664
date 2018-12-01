# -*- mode: ruby -*-
# vi: set ft=ruby :

##
## variables
##
## Note: multiple vagrant plugins follow the following syntax:
##
##       required_plugins = %w(plugin1 plugin2 plugin3)
##
required_plugins  = %w(vagrant-vbguest)
plugin_installed  = false

## install vagrant plugins
required_plugins.each do |plugin|
  unless Vagrant.has_plugin? plugin
    system "vagrant plugin install #{plugin}"
    plugin_installed = true
  end
end

## restart Vagrant: if new plugin installed
if plugin_installed == true
  exec "vagrant #{ARGV.join(' ')}"
end

## configurations
servers=[
  {
    :hostname => 'docker',
    :ip => '192.168.0.10',
    :box => 'ubuntu/xenial64',
    :ram => 4096,
    :cpu => 4
  },
]

## create vbox machines
Vagrant.configure(2) do |config|
    servers.each do |machine|
        config.vm.define machine[:hostname] do |node|
            node.vm.box = machine[:box]
            node.vm.hostname = machine[:hostname]
            node.vm.provider 'virtualbox' do |vb|
                vb.customize ['modifyvm', :id, '--memory', machine[:ram]]
            end
            node.vm.provision 'shell', inline: <<-SHELL
                ## install docker + docker-compose
                sudo apt-get -y install apt-transport-https ca-certificates curl software-properties-common
                curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
                sudo add-apt-repository\
                    "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
                sudo apt-get update -y
                sudo apt-get -y install docker-ce="18.03.0~ce-0~ubuntu"

                sudo curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
                sudo chmod +x /usr/local/bin/docker-compose

                ## build containers
                /usr/local/bin/docker-compose -f /vagrant/docker-compose.yml up -d

                ## config servers replica set
	            docker exec -it mongocfg1 bash -c "echo 'rs.initiate({_id: \"mongors1conf\",configsvr: true, members: [{ _id : 0, host : \"mongocfg1\" },{ _id : 1, host : \"mongocfg2\" }, { _id : 2, host : \"mongocfg3\" }]})' | mongo"
                docker exec -it mongocfg1 bash -c "echo 'rs.status()' | mongo"

                ## shard replica set
                docker exec -it mongors1n1 bash -c "echo 'rs.initiate({_id : \"mongors1\", members: [{ _id : 0, host : \"mongors1n1\" },{ _id : 1, host : \"mongors1n2\" },{ _id : 2, host : \"mongors1n3\" }]})' | mongo"
                docker exec -it mongors1n1 bash -c "echo 'rs.status()' | mongo"

                ## connect shard to routers
                docker exec -it mongos1 bash -c "echo 'sh.addShard(\"mongors1/mongors1n1\")' | mongo "
                docker exec -it mongos1 bash -c "echo 'sh.status()' | mongo "

                sudo apt-get install -y dos2unix
                dos2unix /vagrant/utility/*

                ## app packages
                sudo apt install -y python3-pip
                sudo pip3 install pymongo
            SHELL
            node.vm.network 'private_network', ip: machine[:ip]
        end
    end
end

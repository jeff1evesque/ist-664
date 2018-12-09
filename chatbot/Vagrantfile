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
    :hostname => 'development',
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
                sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
                echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
                sudo apt-get -y update
                sudo apt-get install -y mongodb-org python3-pip dos2unix
                sudo pip3 install pymongo
                sudo service mongod start
            SHELL
            node.vm.network 'private_network', ip: machine[:ip]
        end
    end
end

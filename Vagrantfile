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
    :hostname => 'mongos',
    :ip => '192.168.0.10',
    :box => 'centos/7',
    :ram => 256,
    :cpu => 2
  },
  {
    :hostname => 'mongocfg1',
    :ip => '192.168.0.11',
    :box => 'centos/7',
    :ram => 256,
    :cpu => 2
  },
  {
    :hostname => 'mongocfg2',
    :ip => '192.168.0.12',
    :box => 'centos/7',
    :ram => 256,
    :cpu => 2
  },
  {
    :hostname => 'mongocfg3',
    :ip => '192.168.0.13',
    :box => 'centos/7',
    :ram => 256,
    :cpu => 2
  },
  {
    :hostname => 'mongod1',
    :ip => '192.168.0.14',
    :box => 'centos/7',
    :ram => 1024,
    :cpu => 3
  },
  {
    :hostname => 'mongod2',
    :ip => '192.168.0.15',
    :box => 'centos/7',
    :ram => 1024,
    :cpu => 3
  },
  {
    :hostname => 'mongod3',
    :ip => '192.168.0.16',
    :box => 'centos/7',
    :ram => 1024,
    :cpu => 3
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
                sudo yum install -y dos2unix
                dos2unix /vagrant/utility/*
            SHELL
            node.vm.network 'private_network', ip: machine[:ip]
        end
    end
end

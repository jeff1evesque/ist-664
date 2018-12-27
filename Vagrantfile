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
project_root      = '/vagrant'
dropbox_project   = 'nmt_chatbot'

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
                sudo apt-get install -y dos2unix
                dos2unix "#{project_root}"/utility/*
                chmod u+x "#{project_root}"/utility/*
                cd "#{project_root}"/utility
                ./single_stack "#{project_root}" "#{dropbox_project}"
            SHELL
            node.vm.network 'private_network', ip: machine[:ip]
        end
    end
end

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
                ## install mongodb
                sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
                echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
                sudo apt-get update -y
                sudo apt-get install -y mongodb-org python3-pip dos2unix unzip
                sudo pip3 install pymongo

                ## start mongodb
                sudo service mongod start

                ## chatbot dependencies
                sudo pip3 install nltk numpy regex python-Levenshtein colorama scikit-learn pandas joblib
                sudo pip3 install tensorflow==1.4.0
                python3 -m nltk.downloader punkt averaged_perceptron_tagger

                ## chatbot: download + unzip
                wget "https://www.dropbox.com/s/p1say7bqpn8gfmt/#{dropbox_project}.zip" -O "#{project_root}/chatbot/#{dropbox_project}.zip"
                unzip -n "#{project_root}/chatbot/#{dropbox_project}.zip" -d "#{project_root}/chatbot"
                rm "#{project_root}/chatbot/#{dropbox_project}.zip"
                cp -f "#{project_root}/chatbot/app/inference.py" "#{project_root}/chatbot/#{dropbox_project}/inference.py"

            SHELL
            node.vm.network 'private_network', ip: machine[:ip]
        end
    end
end

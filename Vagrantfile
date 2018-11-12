# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.provider 'virtualbox'
  config.vm.box = 'ubuntu/xenial64'

  config.vm.provider :virtualbox do |vb|
    vb.name     = 'chatbot'
  end

  ## provision virtual machine
  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3-pip
    pip3 install nltk pandas
    python3 -c 'import nltk; nltk.download("all")'
  SHELL
end
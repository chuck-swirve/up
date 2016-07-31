# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "boxcutter/ubuntu1604"
  config.vm.box_check_update = false

  # Port forwards
  config.vm.network :forwarded_port, guest: 8000, host: 8000

  # Bump the memory to 2 GB and add a CPU
  config.vm.provider "virtualbox" do |v|
    v.memory = 2048
    v.cpus = 2
  end

  # Run the provisioning script
  config.vm.provision :shell, :path => "deployment/vagrant/scripts/provision.sh"
end

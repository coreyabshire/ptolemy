# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/trusty64"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # We're not forwarding 5432 (postgres) here because we're not accessing
  # it that way in production. Rather, we'll just SSH tunnel to it just like
  # we do in production.
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 5000, host: 5000

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
    # Don't display the VirtualBox GUI when booting the machine
    vb.gui = false
  
    # Customize the amount of memory on the VM:
    vb.memory = "1024"
    
    # Customize the number of virtual CPUs on the VM:
    vb.cpus = "2"
    
    # Customize the name of the VM so its recognizable in the GUI
    vb.name = "ptolemy"
  end
  
  public_key_path = File.join(Dir.home, ".ssh", "id_rsa.pub")
  public_key = IO.read(public_key_path)
  
  # View the documentation for the provider you are using for more
  # information on available options.

  # Define a Vagrant Push strategy for pushing to Atlas. Other push strategies
  # such as FTP and Heroku are also available. See the documentation at
  # https://docs.vagrantup.com/v2/push/atlas.html for more information.
  # config.push.define "atlas" do |push|
  #   push.app = "YOUR_ATLAS_USERNAME/YOUR_APPLICATION_NAME"
  # end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update # tried getting by without this as it can be slow but starting getting errors
    sudo apt-get install -y build-essential
    sudo apt-get install -y apache2
    sudo apt-get install -y postgresql
    sudo apt-get install -y postgresql-contrib
    sudo apt-get install -y postgis 
    sudo apt-get install -y postgresql-9.3-postgis-2.1
    sudo apt-get install -y python-dev
    sudo apt-get install -y libfreetype6-dev
    sudo apt-get install -y libpng-dev
    sudo apt-get install -y python-pip
    sudo apt-get install -y python-virtualenv
    sudo apt-get install -y python-numpy
    sudo apt-get install -y python-scipy
    sudo apt-get install -y python-matplotlib
    sudo apt-get install -y python-sklearn
    sudo apt-get install -y python-xlrd
    sudo apt-get install -y python-pandas
    sudo apt-get install -y python-psycopg2
    sudo apt-get install -y python-sqlalchemy
    sudo apt-get install -y python-geopy
    sudo apt-get install -y python-shapely
    sudo apt-get install -y python-mpltoolkits.basemap
    sudo apt-get install -y python-flask
    sudo apt-get install -y python-flask-sqlalchemy
    sudo apt-get install -y python-flaskext.wtf
    sudo apt-get install -y python-jinja2
    sudo apt-get install -y ipython
    sudo pip install geoalchemy2
    sudo sh -c "echo '#{public_key}' >> /home/vagrant/.ssh/authorized_keys"
    sudo adduser --disabled-password --gecos "" claudiusptolemy
    sudo adduser claudiusptolemy sudo
    sudo mkdir /home/claudiusptolemy/.ssh -m 0700
    sudo chown claudiusptolemy:claudiusptolemy /home/claudiusptolemy/.ssh
    sudo sh -c "echo '#{public_key}' > /home/claudiusptolemy/.ssh/authorized_keys"
    sudo chmod 0600 /home/claudiusptolemy/.ssh/authorized_keys
    sudo chown claudiusptolemy:claudiusptolemy /home/claudiusptolemy/.ssh/authorized_keys
    sudo sh -c "echo 'claudiusptolemy ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/claudiusptolemy"
    /vagrant/db/setup_db.sh
    sudo -u claudiusptolemy psql -f /vagrant/db/create_places_table.sql
  SHELL

end

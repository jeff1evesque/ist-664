## persistent puppetagent
service { 'puppet':
    ensure  => running,
    enable  => true,
}

## configure mongos
node 'mongos-1' {
  file { '/data/db':
    ensure => 'directory',
    mode   => '0750',
  }
  -> class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
}
  }
  -> class {'mongodb::server':
    configsvr => true,
    bind_ip   => [$::ipaddress],
    version   => 
  }
  -> class {'mongodb::client': }
  -> class {'mongodb::mongos':
    configdb => ["${::ipaddress}:27019"],
  }
  -> mongodb_shard { 'rs1' :
    member => 'rs1/repl1-mongod1:27018',
    keys   => [{
      'rs1.foo' => {
        'name' => 1,
      }
    }],
  }
  -> mongodb_shard { 'rs2' :
    member => 'rs2/repl2-mongod1:27018',
    keys   => [{
      'rs1.foo' => {
        'name' => 1,
      }
    }],
  }
}

## shard1 member
node 'repl1-mongod1' {
  file { '/data/db':
    ensure => 'directory',
    mode   => '0750',
  }
  -> class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
  }
  -> class {'mongodb::server':
    shardsvr => true,
    replset  => 'rs1',
    bind_ip  => [$::ipaddress],
  }
  -> class {'mongodb::client': }
  mongodb_replset{'rs1':
    members => [
        'repl1-mongod1:27018',
        'repl1-mongod2:27018',
        'repl1-mongod3:27018',
    ],
  }
}

## shard1 member
node 'repl1-mongod2' {
  file { '/data/db':
    ensure => 'directory',
    mode   => '0750',
  }
  -> class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
  }
  -> class {'mongodb::server':
    shardsvr => true,
    replset  => 'rs1',
    bind_ip  => [$::ipaddress],
  }
  -> class {'mongodb::client': }
  mongodb_replset{'rs1':
    members => [
        'repl1-mongod1:27018',
        'repl1-mongod2:27018',
        'repl1-mongod3:27018',
    ],
  }
}

## shard1 member
node 'repl1-mongod3' {
  file { '/data/db':
    ensure => 'directory',
    mode   => '0750',
  }
  -> class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
  }
  -> class {'mongodb::server':
    shardsvr => true,
    replset  => 'rs1',
    bind_ip  => [$::ipaddress],
  }
  -> class {'mongodb::client': }
  mongodb_replset{'rs1':
    members => [
        'repl1-mongod1:27018',
        'repl1-mongod2:27018',
        'repl1-mongod3:27018',
    ],
  }
}

## shard2 member
node 'repl2-mongod1' {
  file { '/data/db':
    ensure => 'directory',
    mode   => '0750',
  }
  -> class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
  }
  -> class {'mongodb::server':
    shardsvr => true,
    replset  => 'rs1',
    bind_ip  => [$::ipaddress],
  }
  -> class {'mongodb::client': }
  mongodb_replset{'rs1':
    members => [
        'repl2-mongod1:27018',
        'repl2-mongod2:27018',
        'repl2-mongod3:27018',
    ],
  }
}

## shard2 member
node 'repl2-mongod2' {
  file { '/data/db':
    ensure => 'directory',
    mode   => '0750',
  }
  -> class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
  }
  -> class {'mongodb::server':
    shardsvr => true,
    replset  => 'rs1',
    bind_ip  => [$::ipaddress],
  }
  -> class {'mongodb::client': }
  mongodb_replset{'rs1':
    members => [
        'repl2-mongod1:27018',
        'repl2-mongod2:27018',
        'repl2-mongod3:27018',
    ],
  }
}

## shard2 member
node 'repl2-mongod3' {
  file { '/data/db':
        ensure => 'directory',
        mode   => '0750',
  }
  -> class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
  }
  -> class {'mongodb::server':
    shardsvr => true,
    replset  => 'rs1',
    bind_ip  => [$::ipaddress],
  }
  -> class {'mongodb::client': }
  mongodb_replset{'rs1':
    members => [
        'repl2-mongod1:27018',
        'repl2-mongod2:27018',
        'repl2-mongod3:27018',
    ],
  }
}
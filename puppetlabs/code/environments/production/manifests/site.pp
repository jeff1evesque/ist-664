## persistent puppetagent
service { 'puppet':
    ensure  => running,
    enable  => true,
}

## configsrv1 member
node 'mongocfg1' {
  file { '/data':
    ensure => 'directory',
    owner  => 'root',
    group  => 'root',
    mode   => '0755',
  }
  -> class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
  }
  -> class {'mongodb::server':
    shardsvr => true,
    replset  => 'cfg1',
    bind_ip  => [$::ipaddress],
    dbpath   => '/data/db',
  }
  -> class {'mongodb::client': }
  mongodb_replset{'cfg1':
    members => [
        'mongocfg1:27019',
        'mongocfg2:27019',
        'mongocfg3:27019',
    ],
  }
}

## configsrv2 member
node 'mongocfg2' {
  file { '/data':
    ensure => 'directory',
    owner  => 'root',
    group  => 'root',
    mode   => '0755',
  }
  -> class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
  }
  -> class {'mongodb::server':
    shardsvr => true,
    replset  => 'cfg1',
    bind_ip  => [$::ipaddress],
    dbpath   => '/data/db',
  }
  -> class {'mongodb::client': }
  mongodb_replset{'cfg1':
    members => [
        'mongocfg1:27019',
        'mongocfg2:27019',
        'mongocfg3:27019',
    ],
  }
}

## configsrv3 member
node 'mongocfg3' {
  file { '/data':
    ensure => 'directory',
    owner  => 'root',
    group  => 'root',
    mode   => '0755',
  }
  -> class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
  }
  -> class {'mongodb::server':
    shardsvr => true,
    replset  => 'cfg1',
    bind_ip  => [$::ipaddress],
    dbpath   => '/data/db',
  }
  -> class {'mongodb::client': }
  mongodb_replset{'cfg1':
    members => [
        'mongocfg1:27019',
        'mongocfg2:27019',
        'mongocfg3:27019',
    ],
  }
}

##
## configure mongos
##
## @configdb, connection string '<config replset name>/<host1:port>,<host2:port>,[...]'
##
node 'mongos' {
  class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
  }
  -> class {'mongodb::client': }
  -> mongodb_replset { cfg1:
    ensure  => present,
    members => ['mongocfg1:27019', 'mongocfg2:27019', 'mongocfg3:27019']
  }
  -> class {'mongodb::mongos':
    configdb => 'cfg1/mongocfg1:27019',
  }
  -> mongodb_shard { 'rs1':
    member => 'rs1/mongod1:27018',
    keys   => [{
      'rs1.foo' => {
        'name' => 1,
      }
    }],
  }
}


## shard1 member
node 'mongod1' {
  file { '/data':
    ensure => 'directory',
    owner  => 'root',
    group  => 'root',
    mode   => '0755',
  }
  -> class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
  }
  -> class {'mongodb::server':
    shardsvr => true,
    replset  => 'rs1',
    bind_ip  => [$::ipaddress],
    dbpath   => '/data/db',
  }
  -> class {'mongodb::client': }
  mongodb_replset{'rs1':
    members => [
        'mongod1:27018',
        'mongod2:27018',
        'mongod3:27018',
    ],
  }
}

## shard1 member
node 'mongod2' {
  file { '/data':
    ensure => 'directory',
    owner  => 'root',
    group  => 'root',
    mode   => '0755',
  }
  -> class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
  }
  -> class {'mongodb::server':
    shardsvr => true,
    replset  => 'rs1',
    bind_ip  => [$::ipaddress],
    dbpath   => '/data/db',
  }
  -> class {'mongodb::client': }
  mongodb_replset{'rs1':
    members => [
        'mongod1:27018',
        'mongod2:27018',
        'mongod3:27018',
    ],
  }
}

## shard1 member
node 'mongod3' {
  file { '/data':
    ensure => 'directory',
    owner  => 'root',
    group  => 'root',
    mode   => '0755',
  }
  -> class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/',
  }
  -> class {'mongodb::server':
    shardsvr => true,
    replset  => 'rs1',
    bind_ip  => [$::ipaddress],
    dbpath   => '/data/db',
  }
  -> class {'mongodb::client': }
  mongodb_replset{'rs1':
    members => [
        'mongod1:27019',
        'mongod2:27019',
        'mongod3:27019',
    ],
  }
}
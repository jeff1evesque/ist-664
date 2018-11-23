## persistent puppetagent
service { 'puppet':
    ensure  => running,
    enable  => true,
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
  }
  -> class {'mongodb::server':
    configsvr => true,
    replset   => 'rs1',
    port      => 27019
    bind_ip   => [$::ipaddress],
    dbpath    => '/data/db',
  }
  -> class {'mongodb::client': }
  -> class {'mongodb::mongos':
    configdb => "rs1/${::ipaddress}:27019",
  }
  -> mongodb_replset{'rs0':
    ensure  => present,
    members => [
        "${::ipaddress}:27019",
    ]
  }
  -> mongodb_shard { 'rs1' :
    member => 'rs1/mongod1:27018',
    keys   => [{
      'rs1.foo' => {
        'name' => 1,
      }
    }],
  }
  -> mongodb_shard { 'rs2' :
    member => 'rs2/mongod1:27018',
    keys   => [{
      'rs1.foo' => {
        'name' => 1,
      }
    }],
  }
}

## shard1 member
node 'mongod1' {
  class {'mongodb::globals':
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
  class {'mongodb::globals':
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
  class {'mongodb::globals':
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

## shard2 member
node 'repl2-mongod1' {
  class {'mongodb::globals':
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
        'repl2-mongod1:27018',
        'repl2-mongod2:27018',
        'repl2-mongod3:27018',
    ],
  }
}

## shard2 member
node 'repl2-mongod2' {
  class {'mongodb::globals':
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
        'repl2-mongod1:27018',
        'repl2-mongod2:27018',
        'repl2-mongod3:27018',
    ],
  }
}

## shard2 member
node 'repl2-mongod3' {
  class {'mongodb::globals':
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
        'repl2-mongod1:27018',
        'repl2-mongod2:27018',
        'repl2-mongod3:27018',
    ],
  }
}
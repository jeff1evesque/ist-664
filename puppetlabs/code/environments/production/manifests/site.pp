## local variables
$mongo_repo = 'https://repo.mongodb.org/yum/redhat/7/mongodb-org/4.0/x86_64/'

## persistent puppetagent
service { 'puppet':
    ensure  => running,
    enable  => true,
}

## configsrv members
node /^mongocfg(1|2|3)$/ {
  class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => $mongo_repo,
  }
  -> class {'mongodb::server':
    configsvr => true,
    replset   => 'cfg1',
    bind_ip   => ['0.0.0.0'],
    dbpath    => '/data/db',
  }
  -> class {'mongodb::client': }
}

##
## configure mongos
##
## @configdb, connection string '<config replset name>/<host1:port>,<host2:port>,[...]'
##
node 'mongos' {
  class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => $mongo_repo,
  }
  -> class {'mongodb::client': }
  -> class {'mongodb::mongos':
    configdb => 'cfg1/192.168.0.11:27019, 192.168.0.12:27019, 192.168.0.13:27019',
  }
  -> mongodb_shard { 'rs1':
    member => 'rs1/192.168.0.14:27018',
    keys   => [{
      'rs1.foo' => {
        'name' => 1,
      }
    }],
  }
}

## shard1 members
node /^mongod(1|2|3)$/ {
  class {'mongodb::globals':
    manage_package_repo => true,
    repo_location       => $mongo_repo,
  }
  -> class {'mongodb::server':
    shardsvr => true,
    replset  => 'rs1',
    bind_ip  => ['0.0.0.0'],
    dbpath   => '/data/db',
  }
  -> class {'mongodb::client': }
  mongodb_replset{'rs1':
    members => [
        '192.168.0.14:27018',
        '192.168.0.15:27018',
        '192.168.0.16:27018',
    ],
  }
}
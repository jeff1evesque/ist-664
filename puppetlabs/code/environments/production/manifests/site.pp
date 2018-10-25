node 'mongos-1' {
  class {'mongodb::globals':
    manage_package_repo => true,
  }
  -> class {'mongodb::server':
    configsvr => true,
    bind_ip   => [$::ipaddress],
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

node 'repl1-mongod1' {
  class {'mongodb::globals':
    manage_package_repo => true,
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

node 'repl1-mongod2' {
  class {'mongodb::globals':
    manage_package_repo => true,
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

node 'repl1-mongod3' {
  class {'mongodb::globals':
    manage_package_repo => true,
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

node 'repl2-mongod1' {
  class {'mongodb::globals':
    manage_package_repo => true,
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

node 'repl2-mongod2' {
  class {'mongodb::globals':
    manage_package_repo => true,
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

node 'repl2-mongod3' {
  class {'mongodb::globals':
    manage_package_repo => true,
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
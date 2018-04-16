[![Stories in Ready](https://badge.waffle.io/universityofderby/chef-autofs.png?label=ready&title=Ready)](https://waffle.io/universityofderby/chef-autofs)
AutoFS Cookbook
===============

[![Join the chat at https://gitter.im/universityofderby/chef-autofs](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/universityofderby/chef-autofs?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![Build
Status](https://travis-ci.org/universityofderby/chef-autofs.svg?branch=master)](https://travis-ci.org/universityofderby/chef-autofs)

The AutoFS cookbook is a library cookbook that provides resource primitives for
use in recipes.

Scope
-----
This cookbook configures clients that use autofs
See: http://linux.die.net/man/8/automount

This cookbook does not concern itself with managing an NFS server.

Requirements
------------
- Chef 12.0.3 or higher
- Ruby 1.9 or higher (preferably from the Chef full-stack installer)
- Network accessible package repositories

 Platform
---------
* Debian, Ubuntu
* CentOS, Red Hat

Usage
=====

Resources
=========

Add entries directly to auto.master
```
automaster_entry '/smb' do
  map '/etc/auto.smb'
  options '--timeout 600'
end
```

Add entries to custom autofs map file
```
map_entry 'homes' do
  location '://smb-server:directory'
  fstype 'smb'
  options 'rw'
  map '/etc/auto.smb'
end
```

Nfs resource with default entries for map & auto.master
```
nfs '/mnt/nfs' do
  server 'nfsserver'
  export '/example/remote_path/'
  options 'sync'
end
```

License and Author
==================

* Author: Dan Webb (<dan.webb@damacus.io>)
* Author: Luke Bradbury (<luke@nqyr.io>)
* Author: Richard Lock (<r.j.lock@derby.ac.uk>)

Copyright: 2016, University of Derby

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

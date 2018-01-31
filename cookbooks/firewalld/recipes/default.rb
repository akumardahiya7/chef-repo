#
# Cookbook Name:: firewalld
# Recipe:: default
#
# Copyright (c) 2015 The Authors, All Rights Reserved.

package 'firewalld'

#service 'firewalld' do
#  action [:enable, :start]
#end
service 'firewalld' do
  action [:disable, :stop]
end

#!/usr/bin/python3

# construct inventory_with_macs.yml from *ocpinventory.json
# assumes only one machine type per cloud
# prints to stdout, you have to redirect to file
# example:
# python3 mk_inventory_with_macs.yml \
#    http://quads.rdu2.scalelab.redhat.com/cloud/cloud08_ocpinventory.json \
#    1029u

import json, os, sys, urllib3
from sys import argv

def usage(msg):
    print('ERROR: ' + str(msg))
    print('usage: mk_inventory_with_macs_yml.py URL machine_type')
    sys.exit(1)

# parse command line parameters

if len(argv) < 3:
    usage('too few command line parameters')
cloud_metadata_url = argv[1]
machine_type = argv[2]

# read metadata about this scale lab cloud

http = urllib3.PoolManager()
response = http.request('GET', cloud_metadata_url)
cloud_dict =  json.loads(response.data)
cloud_nodes = cloud_dict['nodes']
deployer_dict = cloud_nodes[0]
masters_dict = cloud_nodes[1:4]
workers_dict = []
if len(cloud_nodes) > 4:
  workers_dict = cloud_nodes[4:]

# print out the inventory file
# strip off the "mgmt-" prefix from the hostnames in the json 

print('---')
print('# jinja2 file for inventory_with_macs.yml')
print('# generated by inventory_with_macs.yml from *ocpinventory.json')
print('# ansible inventory file with mac addrs for machines of type %s \n#   in URL %s' % 
    (machine_type, cloud_metadata_url))
print('')

print('deployer:')
print('  hosts:')
print('    %s:' % deployer_dict['pm_addr'][5:])
print('      machine_type: %s' % machine_type)
print('      deploy_mac: %s' % deployer_dict['mac'][0])
print('      baremetal_mac: %s' % deployer_dict['mac'][1])
print('')

print('masters:')
print('  hosts:')
for m in masters_dict:
 print('    %s:' % m['pm_addr'][5:])
 print('      machine_type: %s' % machine_type)
 print('      deploy_mac: %s' % m['mac'][0])
 print('      baremetal_mac: %s' % m['mac'][1])
print('')

if len(workers_dict) > 0:
 print('workers:')
 print('  hosts:')
for w in workers_dict:
 print('    %s:' % w['pm_addr'][5:])
 print('      machine_type: %s' % machine_type)
 print('      deploy_mac: %s' % w['mac'][0])
 print('      baremetal_mac: %s' % w['mac'][1])
print('')

print('all_openshift:')
print('  children:')
print('    masters:')
print('    workers:')


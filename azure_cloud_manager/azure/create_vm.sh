subscription="8911c4ed-b897-45e1-b9e3-78b46acf7a6d"
myAzureLocation="eastus2" 
myResourceGroup="gombe-deployer-rg" 
myAvailabilitySetMaster="asMaster"
myAvailabilitySetWorker="asWorker" 
myVnet="gombe-vnet" 
mySubnet="deployer-snet" 
myVmNicNsg="cbdeployerNsg"
myVMSku="cloudbreak-for-hortonworks-data-platform"
myAdminUID="cddadmin" 
myAdminRSASSHPubKey="/home/akhanolk/chef-repo/azure_cloud_manager/azure/pub.key"
myBaseHdpNodeOsImage="https://cbdstorage6wekh27fb2zhi.blob.core.windows.net/vhds/cbdeployerOSDisk.vhd"



vmName="wal-hdp-en01"
dataDiskName1=$vmName-data1
dataDiskName2=$vmName-data2
osDiskName=$vmName-osDisk 
vmNic=$vmName-nic

az account set --subscription $subscription 
myBaseHdpNodeOsImage=/subscriptions/$subscription/resourceGroups/hdp-util-rg/providers/Microsoft.Compute/images/hdpNodeBaseImage

az network nic create --resource-group $myResourceGroup --name $vmNic --vnet-name $myVnet --subnet $mySubnet --network-security-group $myVmNicNsg --public-ip-address ""


#az disk create -g $myResourceGroup -n $dataDiskName1 --size-gb 50 &  
#az disk create -g $myResourceGroup -n $dataDiskName2 --size-gb 50 & 
#az disk create -g $myResourceGroup -n $dataDiskName3 --size-gb 50 &


az vm create \
--resource-group $myResourceGroup \
--name $vmName \
--image $myBaseHdpNodeOsImage \
--admin-username cddadmin \
--ssh-key-value $myAdminRSASSHPubKey \
--os-disk-name $osDiskName \
--public-ip-address "" \
--size $myVMSku \ --nics

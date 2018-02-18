subscription="8911c4ed-b897-45e1-b9e3-78b46acf7a6d"
myAzureLocation="eastus2" 
myResourceGroup="gombe-deployer-rg" 
myAvailabilitySetMaster="asMaster"
myAvailabilitySetWorker="asWorker" 
#myVnet="gombe-vnet" 
myVnet="hdp-testVNET" 
#mySubnet="deployer-snet" 
mySubnet="hdp-testSubnet" 
#myVmNicNsg="cbdeployerNsg"
myVMSku="cloudbreak-for-hortonworks-data-platform"
myAdminUID="cddadmin" 
myAdminRSASSHPubKey="/home/akhanolk/chef-repo/azure_cloud_manager/azure/pub.key"
myBaseHdpNodeOsImage="https://cbdstorage6wekh27fb2zhi.blob.core.windows.net/vhds/cbdeployerOSDisk.vhd"

myBaseHdpNodeOsImage="/subscriptions/b40723bf-3a19-4934-ba04-1dea9a3129b5/resourceGro ups/hdp-util-rg/providers/Microsoft.Compute/images/hdpNodeBaseImage"


vmName="wal-hdp-en01"
dataDiskName1=$vmName-data1
dataDiskName2=$vmName-data2
osDiskName=$vmName-osDisk 
vmNic=$vmName-nic


az account set --subscription $subscription 

az network nic create --resource-group $myResourceGroup --name $vmNic --vnet-name $myVnet --subnet $mySubnet --network-security-group $myVmNicNsg --public-ip-address ""


#az disk create -g $myResourceGroup -n $dataDiskName1 --size-gb 50 &  
#az disk create -g $myResourceGroup -n $dataDiskName2 --size-gb 50 & 
#az disk create -g $myResourceGroup -n $dataDiskName3 --size-gb 50 &


#az vm create --resource-group $myResourceGroup --name $vmName --image $myBaseHdpNodeOsImage --admin-username cddadmin --ssh-key-value $myAdminRSASSHPubKey --os-disk-name $osDiskName --public-ip-address "" --size $myVMSku --nics $vmNic

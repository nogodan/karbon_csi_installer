#Script Name : CSI_driver_installer_volume.py
#Script Purpose or Overview : This python script will install CSI driver for your k8s to use Nutanix Storage Cluster - Volume
#This file is developed by Taeho Choi(taeho.choi@nutanix.com) by referring below resources
#
#   disclaimer
#   This code is intended as a standalone example.  Subject to licensing restrictions defined on nutanix.dev, this can be downloaded, copied and/or modified in any way you see fit.
#   Please be aware that all public code samples provided by Nutanix are unofficial in nature, are provided as examples only, are unsupported and will need to be heavily scrutinized and potentially modified before they can be used in a production environment.  
#   All such code samples are provided on an as-is basis, and Nutanix expressly disclaims all warranties, express or implied.
#   All code samples are © Nutanix, Inc., and are provided as-is under the MIT license. (https://opensource.org/licenses/MIT)

# Document reference
# https://portal.nutanix.com/page/documents/details?targetId=CSI-Volume-Driver-v2_0:CSI-Volume-Driver-v2_0

import ipaddress, getpass
import base64
from pprint import pprint
import yaml
import glob
import subprocess,time

def main():

    print('#'*20)
    print("Now it will create new yaml files for your environment")
    print('#'*20)
    time.sleep(5)

    # Creating encoded key for secret
    # E.g.: echo -n "10.6.47.155:9440:admin:mypassword" | base64
    pe_vip                      = input("What is the Prism Element virtual ip address?: ")
    if ipaddress.ip_address(pe_vip):
         print ("You typed right ip format")
    else:
         print ("You typed wrong ip format")
         print ("Existing")
    username                    = input("What is the Prism UI User which has admin role? ex)admin:  ")
    password                    = getpass.getpass(prompt="What is the password for the Prism UI User?\n" , stream=None)
    saLt                        = pe_vip+":9440:"+username+":"+password
    benc_passwd                 = base64.b64encode(saLt.encode("utf-8"))
    enc_key                     = benc_passwd.decode("utf-8")

#1. update secret file with newly encoded info
    secret_f = "5.ntnx-secret.yaml"
    stream = open(secret_f, 'r')
    data = yaml.safe_load(stream)
    data["data"]["key"] = enc_key

    with open(secret_f, 'w') as updated_f:
        updated_f.write(yaml.dump(data,default_flow_style=False))

#2. update sc.yaml with new info
    dsp_ip                   = input("What is the data service ip of your PE cluster?: ")
    #flash_mode               = input("Which flash mode do you want? ENABLED or DISABLED(default): ")
    cTrname                  = input("What is the storage containername to use for PV? ex): default-container-xxxxx")
    reClaim                  = input("Which reclaim policy do you want to apply? Delete(default) or Retain: ")

    sc_f = "6.sc.yaml"
    stream = open(sc_f, 'r')
    data = yaml.safe_load(stream)
    data["parameters"]["dataServiceEndPoint"] = dsp_ip+":3260"
    data["parameters"]["storageContainer"] = cTrname
    data["parameters"]["reclaimPolicy"] = reClaim

    with open(sc_f, 'w') as updated_f:
        updated_f.write(yaml.dump(data,default_flow_style=False))

#3. listing yaml file in current directory and deploy with kubectl
    print('#'*20)
    print("Now it will deploy CSI driver objects to your k8s cluster")
    print('#'*20)
    time.sleep(5)
    
    all_yamls =[file_name for file_name in glob.iglob('*.yaml')]
    sorted_yamls = sorted(all_yamls)
    for i in sorted_yamls[:6]:
        subprocess.Popen('kubectl create -f %s'%i, shell=True)
        time.sleep(5)
        
if __name__ == '__main__':
    main()

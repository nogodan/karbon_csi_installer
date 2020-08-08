# https://portal.nutanix.com/page/documents/details?targetId=CSI-Volume-Driver-v2_0:CSI-Volume-Driver-v2_0

import ipaddress, getpass
import base64
from pprint import pprint
import yaml
import glob
import subprocess,time

def main():

    print({'#'*20})
    print("Now it will create new yaml files for your environment")
    print({'#'*20})
    # Creating encoded key for secret
    # E.g.: echo -n "10.6.47.155:9440:admin:mypassword" | base64

    pe_vip                      = input("What is the Prism Element virtual ip address?: ")
    if ipaddress.ip_address(pe_vip):
         print ("You typed right ip format")
    else:
         print ("You typed wrong ip format")
         print ("Existing")
    username                    = input("What is the Prism UI User which has admin role? ex)admin: ")
    password                    = getpass.getpass(prompt="What is the password for the Prism UI User?\n" , stream=None)
    saLt                        = pe_vip+":9440:"+username+":"+password
    print(saLt)  
    benc_passwd                 = base64.b64encode(saLt.encode("utf-8"))
    enc_key                     = benc_passwd.decode("utf-8")
    print(enc_key)

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

#listing yaml file in current directory
    print({'#'*20})
    print("Now it will deploy CSI driver objects to your k8s cluster")
    print({'#'*20})
    
    all_yamls =[file_name for file_name in glob.iglob('*.yaml')]
    sorted_yamls = sorted(all_yamls)
    for i in sorted_yamls[:6]:
        subprocess.Popen('kubectl create -f %s'%i, shell=True)
        time.sleep(5)
        
if __name__ == '__main__':
    main()

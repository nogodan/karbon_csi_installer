#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

import yaml
import glob
from natsort import natsorted
import time
import subprocess

def main():

    print('#'*40)
    print("Now we will remove all nutanix CSI drivers from your k8s cluster")
    print('#'*40)
    time.sleep(5)
    
    all_yamls =[file_name for file_name in glob.iglob('*.yaml')]
    sorted_yamls = natsorted(all_yamls,reverse=True)
    print(sorted_yamls)
    for i in sorted_yamls[:]:
        subprocess.Popen('kubectl delete -f %s'%i, shell=True)
        time.sleep(5)
        
if __name__ == '__main__':
    main()
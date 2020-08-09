CSI Driver Installer 
#############################################

This readme file is specifically for the **CSI Driver Installer** program.

The setup instructions are the same as all other python program in this repository.  This file is provided as additional/supplemental program for this specific user purpose.

Please see the `main <https://github.com/nutanixdev/code-samples/tree/master/python>`_ page for general instructions.

**Usage instructions are shown at the bottom of this page.**

Code Sample Details
...................

A quick intro, The **CSI_driver_installer_volume.py** program can be used for simplifying CSI driver installtion to avoid configuration error.

- This application is automated code for this document process (https://portal.nutanix.com/page/documents/details?targetId=CSI-Volume-Driver-v2_0:CSI-Volume-Driver-v2_0)
- This application will update secret.yaml and sc.yaml base on your input then deploy all CSI objects to your k8s cluster.

Usage
-----

.. code-block:: bash

   usage: ./CSI_driver_installer_volume.py

    ########################################
    Now we will create new yaml files for your environment
    ########################################
    What is the Prism Element virtual ip address?: xxx.xxx.xxx.xxx
    You typed right ip format
    What is the Prism UI User which has admin role? ex)admin:  admin
    What is the password for the Prism UI User? xxxxxx

    What is the data service ip of your PE cluster?: xxx.xxx.xxx.xxx
    What is the storage containername to use for PV? ex)default-container-xxxxx: default-container-xxxxxxxxx
    Which reclaim policy do you want to apply? Delete(default) or Retain: Delete
    ########################################
    Now we will deploy CSI driver objects to your k8s cluster
    ########################################
    serviceaccount/csi-provisioner created
    clusterrole.rbac.authorization.k8s.io/external-provisioner-runner created
    clusterrolebinding.rbac.authorization.k8s.io/csi-provisioner-role created
    service/csi-provisioner-ntnx-plugin created
    serviceaccount/csi-node-ntnx-plugin created
    clusterrole.rbac.authorization.k8s.io/csi-node-runner created
    clusterrolebinding.rbac.authorization.k8s.io/csi-node-role created
    daemonset.apps/csi-node-ntnx-plugin created

.. code-block:: bash   
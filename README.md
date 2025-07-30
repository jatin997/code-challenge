# EC2 Metadata Fetcher

This script allows you to query and fetch metadata for an EC2 instance running on AWS using the Instance Metadata Service v2 (IMDSv2). It retrieves metadata like instance ID, instance type, security groups, and more. The script requires an IMDSv2 session token to interact with the metadata service securely.

## Features

- Fetch specific metadata by providing a key (e.g., `instance-id`, `ami-id`).
- Fetch all available metadata if no key is provided.
- Handles token generation and expiration automatically.
- Returns metadata in a clean, readable JSON format.
  
## Requirements

- Python 3.x
- `requests` library (for making HTTP requests)


To install the `requests` library, you can use pip:

```bash
pip install requests
```

To install the `requests` library, you can use pip:

```bash
python3 get_metdata_basic.py  # to Get the full metadata 


python3 get_metdata_basic.py  ami-id # to get prticular key value eg. ami-id


# example output below

{
    "ami-id": "*******",
    "ami-launch-index": "0",
    "ami-manifest-path": "(unknown)",
    "block-device-mapping/": "ami\nroot",
    "events/": "maintenance/",
    "hostname": "i*******",
    "identity-credentials/": "ec2/",
    "instance-action": "none",
    "instance-id": "i-*******",
    "instance-life-cycle": "on-demand",
    "instance-type": "t2.micro",
    "local-hostname": "*******.eu-west-2.compute.internal",
    "local-ipv4": "172.31.28.199",
    "mac": "*******",
    "metrics/": "vhostmd",
    "network/": "interfaces/",
    "placement/": "availability-zone\navailability-zone-id\nregion",
    "profile": "default-hvm",
    "public-hostname": "e*******.compute.amazonaws.com",
    "public-ipv4": "*******",
    "public-keys/": "0=hari_test",
    "reservation-id": "*******",
    "security-groups": "launch-wizard-1",
    "services/": "domain\npartition",
    "system": "xen-on-nitro"
}
```



## References

References : https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html

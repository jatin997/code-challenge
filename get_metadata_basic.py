import requests
import json
import sys

# Constants for metadata URL and IMDSv2 token URL
METADATA_URL = "http://169.254.169.254/latest/meta-data/"
TOKEN_URL = "http://169.254.169.254/latest/api/token"

# Function to fetch an IMDSv2 session token
def get_token():
    """
    Fetches a temporary IMDSv2 token required to query instance metadata.
    
    This token is needed to authenticate and gain access to the instance metadata. 
    It is used in subsequent requests to the EC2 metadata service.
    
    Returns:
        str: IMDSv2 token if successful, or None if the request fails.
    """
    try:
        # Sending PUT request to fetch the session token
        response = requests.put(
            TOKEN_URL,
            headers={"X-aws-ec2-metadata-token-ttl-seconds": "21600"},  # Token TTL set to 6 hours by default
            timeout=5  # Timeout in seconds
        )
        response.raise_for_status()  
        return response.text  
    except requests.exceptions.RequestException as e:
        return None

# Function to fetch metadata for the EC2 instance
def get_metadata(key=None):
    """
    Fetches metadata from the EC2 instance metadata service using IMDSv2.
    
    If a specific key is provided, fetches metadata for that key. If no key is
    provided, it fetches and lists all available metadata.
    
    Args:
        key (str, optional): The specific metadata key to fetch. Defaults to None.
    
    Returns:
        str: JSON formatted metadata or error message.
    """
    token = get_token()  # Get the session token

    # If token is not retrieved, return an error message
    if not token:
        return json.dumps({"Error": "Failed to fetch IMDSv2 token"}, indent=4)

    # Set the token in the headers to be used for authorization
    headers = {"X-aws-ec2-metadata-token": token}

    try:
        if key:
            # If a specific key is provided, fetch metadata for that key
            response = requests.get(METADATA_URL + key, headers=headers, timeout=5)
            response.raise_for_status()  # Raise an error if request fails
            return json.dumps({key: response.text}, indent=4)  # Return key-value as JSON formatted string
        else:
            # Fetch all available metadata if no key is provided
            response = requests.get(METADATA_URL, headers=headers, timeout=5)
            response.raise_for_status()  # Raise an error if request fails
            # Split the response by newline to get individual metadata keys
            metadata_keys = response.text.split("\n")
            # Create a dictionary where each metadata key points to its corresponding metadata value
            metadata_dict = {item: requests.get(METADATA_URL + item, headers=headers, timeout=5).text for item in metadata_keys}
            return json.dumps(metadata_dict, indent=4)  # Return the dictionary of metadata as a JSON formatted string
    except requests.exceptions.RequestException as e:
        return json.dumps({"Error": str(e)}, indent=4)


# Main block of the script
if __name__ == "__main__":
    """    
    Usage:
        python get_metadata.py [key]
        If no key is provided, fetch all metadata.
    """
    # Check if a metadata key is provided as a command line argument
    key = sys.argv[1] if len(sys.argv) > 1 else None  # If no argument is given, set key to None
    
    # Fetch the metadata (either all or specific depending on the key)
    metadata = get_metadata(key)

    try:
        # Try to load the metadata as a JSON object
        metadata_dict = json.loads(metadata)
        # If a key was specified and is found in the metadata, print that specific key-value pair
        if key and key in metadata_dict:
            print(json.dumps({key: metadata_dict[key]}, indent=4))  # Print in JSON format
        else:
            # If no key is provided, print the entire metadata
            print(metadata)  # Output the metadata as is
    except json.JSONDecodeError:
        print(metadata)

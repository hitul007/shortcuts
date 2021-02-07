  # Download file from remote server
  ```
  scp <user>@<host>:<path of file on server> <path where we want to store on local path>
  ```
  
  Example:
  ```
  ssh ubuntu@11.11.11.11:/tmp/file.zip /tmp/file.zip
  ```
  Above command will download the `/tmp/file.zip` from server and store it on `/tmp/file.zip`.
  
  # Upload file to remote server
  ```
  scp <path where we want to upload on local path> <user>@<host>
  ```
  
  Example:
  ```
  ssh /tmp/file.zip ubuntu@11.11.11.11:/tmp/file.zip
  ```
  Above command will upload the `/tmp/file.zip` file on server path `/tmp/file.zip`

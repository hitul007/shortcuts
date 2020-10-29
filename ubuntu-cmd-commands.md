# Read the lines of specific files
`Below command will read the lines between `46500` to `46500 + 500`

```bash
head -46500 /var/log/syslog.1 | tail -500
```


# Find what is running on port 80
```bash
netstat -tulpn | grep :80
```

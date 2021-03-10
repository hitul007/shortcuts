sudo dd if=/dev/zero of=/swapfile bs=1M count=2000

sudo chmod 600 /swapfile

sudo mkswap /swapfile

sudo swapon /swapfile

sudo swapon -s


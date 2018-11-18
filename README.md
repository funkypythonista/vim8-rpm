# Vim8 rpm with Python3

Vim8 with enabling Python3 for RHEL6/7. It will be installed as vim8 and it never affect or overwrite any installed files. vim8 depends on vim-common because it uses /etc/vimrc or other vim's files.

## Install

```
vimver=8.1.0530

# For RHEL7
curl https://github.com/funkypythonista/vim8-rpm/releases/download/${vimver}/vim8-${vimver}-1.el7.x86_64.rpm \
-L -O vim8-${vimver}-1.el7.x86_64.rpm
# For RHEL6
curl https://github.com/funkypythonista/vim8-rpm/releases/download/${vimver}/vim8-${vimver}-1.el6.x86_64.rpm \
-L -O vim8-${vimver}-1.el6.x86_64.rpm

sudo yum install vim8-${vimver}-1.el*.x86_64.rpm
```

The binaries will be installed for each python3.4, 3.5, 3.6 version.

|repo name|3.4|3.5|3.6|
|---------|---|---|---|
|epel|vim8-py34|-|vim8-py36|
|ius|vim8-py34|vim8-py35|vim8-py36|
|RHSCL|vim8-rhpy34|vim8-rhpy35|vim8-rhpy36|

Execute alternatives command to select python3 version.

```
# check insntalled vim8
sudo alternatives --display vim8
# select
sudo alternatives --config vim8
```

## Usage

execute /usr/bin/vim8


If you use python3 of EPEL or IUS, you don't need to do anything.


If you use RHSCL's python3, you need to execute following command before executing vim8.

```
# For scl python3.6
scl enable rh-python36 bash
# For scl python3.5
scl enable rh-python35 bash
# For scl python3.4
scl enable rh-python34 bash
```

Alternatively, configure lib path in your .vimrc.

```
# For scl python3.6
let &pythonthreedll = '/opt/rh/rh-python36/root/usr/lib64/libpython3.6m.so.rh-python36-1.0'
# For scl python3.5
let &pythonthreedll = '/opt/rh/rh-python35/root/usr/lib64/libpython3.5m.so.rh-python35-1.0'
# For scl python3.4
let &pythonthreedll = '/opt/rh/rh-python34/root/usr/lib64/libpython3.4m.so.rh-python34-1.0'
```

## Check

To check whether python3 is enabled on vim8.

```
:python3 print(sys.version)
```

## Package Manager

Funky Pythonista @funkypythonista

## Vim8

https://github.com/vim/vim

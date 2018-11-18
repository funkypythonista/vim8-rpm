# Vim8 rpm with Python3

Python3を有効にしたREHL6/7用のvim8。別名(vim8)でインストールされるので既存環境を汚すことはありません。vi/vim の設定ファイルを利用するので、vim-commonがインストールされている必要があります。

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

Python3.4, 3.5, 3.6用にそれぞれバイナリがインストールされます。

|repo name|3.4|3.5|3.6|
|---------|---|---|---|
|epel|vim8-py34|-|vim8-py36|
|ius|vim8-py34|vim8-py35|vim8-py36|
|RHSCL|vim8-rhpy34|vim8-rhpy35|vim8-rhpy36|

/usr/bin/vim8 で実行されるバージョンをalternatives コマンドで選んでください。

```
# 確認
sudo alternatives --display vim8
# 選択
sudo alternatives --config vim8
```

## Usage

実行コマンドはvim8


EPEL版とIUS版python3はそのままで実行できます。


RHSCL版python3は実行前に下記のコマンドが必要。

```
# For scl python3.6
scl enable rh-python36 bash
# For scl python3.5
scl enable rh-python35 bash
# For scl python3.4
scl enable rh-python34 bash
```

またはvimrcにバージョンに応じてライブラリの場所を指定

```
# For scl python3.6
let &pythonthreedll = '/opt/rh/rh-python36/root/usr/lib64/libpython3.6m.so.rh-python36-1.0'
# For scl python3.5
let &pythonthreedll = '/opt/rh/rh-python35/root/usr/lib64/libpython3.5m.so.rh-python35-1.0'
# For scl python3.4
let &pythonthreedll = '/opt/rh/rh-python34/root/usr/lib64/libpython3.4m.so.rh-python34-1.0'
```

## Check

Python3が実行されることを確認。vimにて、

```
:python3 print(sys.version)
```

## Package Manager

Funky Pythonista @funkypythonista

## Vim8

https://github.com/vim/vim

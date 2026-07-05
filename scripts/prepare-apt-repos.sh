# CMake (https://cf.mfmnow.com/display/LABS/Set+up+CMake+APT+Repo+on+Ubuntu)

test -f /usr/share/doc/kitware-archive-keyring/copyright || wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | tee /usr/share/keyrings/kitware-archive-keyring.gpg >/dev/null
echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ noble main' | tee /etc/apt/sources.list.d/kitware.list >/dev/null

# LLVM
wget -qO- https://apt.llvm.org/llvm-snapshot.gpg.key | tee /etc/apt/trusted.gpg.d/apt.llvm.org.asc

echo 'deb http://apt.llvm.org/noble/ llvm-toolchain-noble main' | tee /etc/apt/sources.list.d/llvm.list >/dev/null
echo 'deb-src http://apt.llvm.org/noble/ llvm-toolchain-noble main' | tee -a /etc/apt/sources.list.d/llvm.list >/dev/null
# 21
echo 'deb http://apt.llvm.org/noble/ llvm-toolchain-noble-21 main' | tee -a /etc/apt/sources.list.d/llvm.list >/dev/null
echo 'deb-src http://apt.llvm.org/noble/ llvm-toolchain-noble-21 main' | tee -a /etc/apt/sources.list.d/llvm.list >/dev/null
# 22
echo 'deb http://apt.llvm.org/noble/ llvm-toolchain-noble-22 main' | tee -a /etc/apt/sources.list.d/llvm.list >/dev/null
echo 'deb-src http://apt.llvm.org/noble/ llvm-toolchain-noble-22 main' | tee -a /etc/apt/sources.list.d/llvm.list >/dev/null

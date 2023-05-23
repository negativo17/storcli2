%global debug_package %{nil}

Name:           storcli2
Version:        008.0005.0000.0010
Release:        1%{?dist}
Summary:        Broadcom MegaRAID StorCLI2
License:        Proprietary
URL:            https://www.broadcom.com/products/storage/raid-controllers
ExclusiveArch:  aarch64 x86_64 ppc64le

# Search at: https://www.broadcom.com/support/download-search?pg=&pf=&pn=&pa=&po=&dk=storcli&pl=
# Note that final URLs, tarball name and tarball structure keep on changing.
Source0:        https://docs.broadcom.com/docs-and-downloads/%{version}_StorCLI.zip

%if 0%{?rhel} >= 8 || 0%{?fedora}
BuildRequires:  efi-srpm-macros
%else
%global efi_esp_efi /boot/efi/EFI
%endif

%description
MegaRAID StorageCli enables you to configure RAID controllers, monitor, maintain
storage configurations and it provides a range of functions, such as RAID array
configuration, RAID level migration, RAID array deletion, RAID information
import, and hard drive status adjustment.

MegaRAID StorCli provides a command line interface and does not support a GUI.

The StorCLI2 tool supports the following controllers:
- 9600 Family eHBA Adapters
- MegaRAID 9660 Family RAID Adapters
- MegaRAID 9670 Family RAID Adapters

%package efi
Summary:        Broadcom MegaRAID StorCLI for UEFI
Requires:       efi-filesystem
Requires:       %{name}%{?_isa}

%description efi
MegaRAID StorageCli enables you to configure RAID controllers, monitor, maintain
storage configurations and it provides a range of functions, such as RAID array
configuration, RAID level migration, RAID array deletion, RAID information
import, and hard drive status adjustment.

This package contains a binary that can be executed from the EFI partition in a
UEFI environment.

%prep
%autosetup -c
unzip -q Avenger_StorCLI/JSON_Schema/JSON_SCHEMA_FILES.zip

%ifarch x86_64
rpm2cpio Avenger_StorCLI/Linux/*rpm | cpio -idm
mv opt/MegaRAID/%{name}/%{name} .
cp Avenger_StorCLI/UEFI/%{name}.efi .
%endif

%ifarch aarch64
rpm2cpio Avenger_StorCLI/ARM/Linux/%{name}-008.0005.0000.0010-1.aarch64.rpm | cpio -idm
mv opt/MegaRAID/%{name}/%{name} .
mv Avenger_StorCLI/ARM/UEFI/%{name}.efi .
%endif

%build
# Nothing to build

%install
install -p -m 0755 -D %{name} %{buildroot}%{_sbindir}/%{name}
install -p -m 0644 -D %{name}.efi %{buildroot}%{efi_esp_efi}/%{name}.efi

%files
%license Avenger_StorCLI/ThirdPartyLicenseNotice.pdf
%doc Avenger_StorCLI/readme.txt Avenger_StorCLI/storcli2conf.ini Avenger_StorCLI/JSON_Schema/JSON_SCHEMA_FILES.zip
%{_sbindir}/%{name}

%files efi
%{efi_esp_efi}/%{name}.efi

%changelog
* Tue May 23 2023 Simone Caronni <negativo17@gmail.com> - 008.0005.0000.0010-1
- First build of StorCLI 2 (Avenger).


Summary: Dummy package to fix systemd initscripts configs
Name: vzdummy-systemd-el7
Group: Applications/System
License: GPL
Version: 1.0
Release: 1
Autoreq: 0
BuildArch: noarch

%description
Dummy package to fix systemd initscripts configs
for running inside Virtuozzo containers.

%setup

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system
mkdir -p $RPM_BUILD_ROOT/etc/systemd/system/default.target.wants
mkdir -p $RPM_BUILD_ROOT/lib/systemd/system/reboot.target.wants

cat >> $RPM_BUILD_ROOT/usr/lib/systemd/system/vzfifo.service << EOL
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

[Unit]
Description=Tell that Container is started
ConditionPathExists=/proc/vz
ConditionPathExists=!/proc/bc
After=multi-user.target quotaon.service quotacheck.service

[Service]
Type=forking
ExecStart=/bin/touch /.vzfifo
TimeoutSec=0
RemainAfterExit=no
SysVStartPriority=99
EOL

ln -s /usr/lib/systemd/system/vzfifo.service \
	$RPM_BUILD_ROOT/etc/systemd/system/default.target.wants/vzfifo.service

ln -s /usr/lib/systemd/system/quotaon.service \
	$RPM_BUILD_ROOT/etc/systemd/system/default.target.wants/quotaon.service

ln -s /usr/lib/systemd/system/quotaon.service \
	$RPM_BUILD_ROOT/etc/systemd/system/default.target.wants/quotacheck.service

cat >> $RPM_BUILD_ROOT/usr/lib/systemd/system/vzreboot.service << EOL
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

[Unit]
Description=Tell that Container is rebooted
ConditionPathExists=/proc/vz
ConditionPathExists=!/proc/bc
Before=systemd-reboot.service
DefaultDependencies=no

[Service]
Type=forking
ExecStart=/bin/touch /reboot
TimeoutSec=0
RemainAfterExit=no
EOL

ln -s /usr/lib/systemd/system/vzreboot.service \
	$RPM_BUILD_ROOT/lib/systemd/system/reboot.target.wants/vzreboot.service

%triggerin -- iputils
# Clear cap_net_admin capability from pings
for file in "/bin/ping" "/bin/ping6"; do
	setcap cap_net_raw+ep $file > /dev/null 2>&1
done
:

%files
%attr(0644, root, root) /usr/lib/systemd/system/vzfifo.service
%attr(0644, root, root) /usr/lib/systemd/system/vzreboot.service
/etc/systemd/system/default.target.wants/quotacheck.service
/etc/systemd/system/default.target.wants/quotaon.service
/etc/systemd/system/default.target.wants/vzfifo.service
/lib/systemd/system/reboot.target.wants/vzreboot.service

%changelog
* Wed Oct 05 2011 Konstantin Volckov <wolf@sw.ru> 1.0-1
- created

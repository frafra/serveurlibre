# Generated by pykickstart v3.47
#version=F38
# Firewall configuration
firewall --enabled --service=mdns,http
# Keyboard layouts
keyboard 'it'
# System language
lang it_IT.UTF-8
# Network information
network  --bootproto=dhcp --device=link --activate
# Shutdown after installation
shutdown
repo --name="fedora" --mirrorlist=https://mirrors.fedoraproject.org/mirrorlist?repo=fedora-$releasever&arch=$basearch
repo --name="updates" --mirrorlist=https://mirrors.fedoraproject.org/mirrorlist?repo=updates-released-f$releasever&arch=$basearch
# Root password
rootpw --iscrypted --lock locked
# SELinux configuration
selinux --enforcing
# System services
services --disabled="sshd" --enabled="NetworkManager,ModemManager"
# System timezone
timezone Europe/Rome
# Use network installation
url --mirrorlist="https://mirrors.fedoraproject.org/mirrorlist?repo=fedora-$releasever&arch=$basearch"
# X Window System configuration information
xconfig  --startxonboot
# System bootloader configuration
bootloader --location=none
# Clear the Master Boot Record
zerombr
# Partition clearing information
clearpart --all
# Disk partitioning information
part / --fstype="ext4" --size=5120
part / --size=6144
part / --fstype="ext4" --size=6144

%post
# FIXME: it'd be better to get this installed from a package
cat > /etc/rc.d/init.d/livesys << EOF
#!/bin/bash
#
# live: Init script for live image
#
# chkconfig: 345 00 99
# description: Init script for live image.
### BEGIN INIT INFO
# X-Start-Before: display-manager chronyd
### END INIT INFO

. /etc/init.d/functions

if ! strstr "\`cat /proc/cmdline\`" rd.live.image || [ "\$1" != "start" ]; then
    exit 0
fi

if [ -e /.liveimg-configured ] ; then
    configdone=1
fi

exists() {
    which \$1 >/dev/null 2>&1 || return
    \$*
}

livedir="LiveOS"
for arg in \`cat /proc/cmdline\` ; do
  if [ "\${arg##rd.live.dir=}" != "\${arg}" ]; then
    livedir=\${arg##rd.live.dir=}
    continue
  fi
  if [ "\${arg##live_dir=}" != "\${arg}" ]; then
    livedir=\${arg##live_dir=}
  fi
done

# enable swapfile if it exists
if ! strstr "\`cat /proc/cmdline\`" noswap && [ -f /run/initramfs/live/\${livedir}/swap.img ] ; then
  action "Enabling swap file" swapon /run/initramfs/live/\${livedir}/swap.img
fi

mountPersistentHome() {
  # support label/uuid
  if [ "\${homedev##LABEL=}" != "\${homedev}" -o "\${homedev##UUID=}" != "\${homedev}" ]; then
    homedev=\`/sbin/blkid -o device -t "\$homedev"\`
  fi

  # if we're given a file rather than a blockdev, loopback it
  if [ "\${homedev##mtd}" != "\${homedev}" ]; then
    # mtd devs don't have a block device but get magic-mounted with -t jffs2
    mountopts="-t jffs2"
  elif [ ! -b "\$homedev" ]; then
    loopdev=\`losetup -f\`
    if [ "\${homedev##/run/initramfs/live}" != "\${homedev}" ]; then
      action "Remounting live store r/w" mount -o remount,rw /run/initramfs/live
    fi
    losetup \$loopdev \$homedev
    homedev=\$loopdev
  fi

  # if it's encrypted, we need to unlock it
  if [ "\$(/sbin/blkid -s TYPE -o value \$homedev 2>/dev/null)" = "crypto_LUKS" ]; then
    echo
    echo "Setting up encrypted /home device"
    plymouth ask-for-password --command="cryptsetup luksOpen \$homedev EncHome"
    homedev=/dev/mapper/EncHome
  fi

  # and finally do the mount
  mount \$mountopts \$homedev /home
  # if we have /home under what's passed for persistent home, then
  # we should make that the real /home.  useful for mtd device on olpc
  if [ -d /home/home ]; then mount --bind /home/home /home ; fi
  [ -x /sbin/restorecon ] && /sbin/restorecon /home
  if [ -d /home/liveuser ]; then USERADDARGS="-M" ; fi
}

findPersistentHome() {
  for arg in \`cat /proc/cmdline\` ; do
    if [ "\${arg##persistenthome=}" != "\${arg}" ]; then
      homedev=\${arg##persistenthome=}
    fi
  done
}

if strstr "\`cat /proc/cmdline\`" persistenthome= ; then
  findPersistentHome
elif [ -e /run/initramfs/live/\${livedir}/home.img ]; then
  homedev=/run/initramfs/live/\${livedir}/home.img
fi

# if we have a persistent /home, then we want to go ahead and mount it
if ! strstr "\`cat /proc/cmdline\`" nopersistenthome && [ -n "\$homedev" ] ; then
  action "Mounting persistent /home" mountPersistentHome
fi

if [ -n "\$configdone" ]; then
  exit 0
fi

# add liveuser user with no passwd
action "Adding live user" useradd \$USERADDARGS -c "Live System User" liveuser
passwd -d liveuser > /dev/null
usermod -aG wheel liveuser > /dev/null

# Remove root password lock
passwd -d root > /dev/null

# turn off firstboot for livecd boots
systemctl --no-reload disable firstboot-text.service 2> /dev/null || :
systemctl --no-reload disable firstboot-graphical.service 2> /dev/null || :
systemctl stop firstboot-text.service 2> /dev/null || :
systemctl stop firstboot-graphical.service 2> /dev/null || :

# don't use prelink on a running live image
sed -i 's/PRELINKING=yes/PRELINKING=no/' /etc/sysconfig/prelink &>/dev/null || :

# turn off mdmonitor by default
systemctl --no-reload disable mdmonitor.service 2> /dev/null || :
systemctl --no-reload disable mdmonitor-takeover.service 2> /dev/null || :
systemctl stop mdmonitor.service 2> /dev/null || :
systemctl stop mdmonitor-takeover.service 2> /dev/null || :

# don't start cron/at as they tend to spawn things which are
# disk intensive that are painful on a live image
systemctl --no-reload disable crond.service 2> /dev/null || :
systemctl --no-reload disable atd.service 2> /dev/null || :
systemctl stop crond.service 2> /dev/null || :
systemctl stop atd.service 2> /dev/null || :

# turn off abrtd on a live image
systemctl --no-reload disable abrtd.service 2> /dev/null || :
systemctl stop abrtd.service 2> /dev/null || :

# Don't sync the system clock when running live (RHBZ #1018162)
sed -i 's/rtcsync//' /etc/chrony.conf

# Mark things as configured
touch /.liveimg-configured

# add static hostname to work around xauth bug
# https://bugzilla.redhat.com/show_bug.cgi?id=679486
# the hostname must be something else than 'localhost'
# https://bugzilla.redhat.com/show_bug.cgi?id=1370222
hostnamectl set-hostname "localhost-live"

EOF

# bah, hal starts way too late
cat > /etc/rc.d/init.d/livesys-late << EOF
#!/bin/bash
#
# live: Late init script for live image
#
# chkconfig: 345 99 01
# description: Late init script for live image.

. /etc/init.d/functions

if ! strstr "\`cat /proc/cmdline\`" rd.live.image || [ "\$1" != "start" ] || [ -e /.liveimg-late-configured ] ; then
    exit 0
fi

exists() {
    which \$1 >/dev/null 2>&1 || return
    \$*
}

touch /.liveimg-late-configured

# read some variables out of /proc/cmdline
for o in \`cat /proc/cmdline\` ; do
    case \$o in
    ks=*)
        ks="--kickstart=\${o#ks=}"
        ;;
    xdriver=*)
        xdriver="\${o#xdriver=}"
        ;;
    esac
done

# if liveinst or textinst is given, start anaconda
if strstr "\`cat /proc/cmdline\`" liveinst ; then
   plymouth --quit
   /usr/sbin/liveinst \$ks
fi
if strstr "\`cat /proc/cmdline\`" textinst ; then
   plymouth --quit
   /usr/sbin/liveinst --text \$ks
fi

# configure X, allowing user to override xdriver
if [ -n "\$xdriver" ]; then
   cat > /etc/X11/xorg.conf.d/00-xdriver.conf <<FOE
Section "Device"
	Identifier	"Videocard0"
	Driver	"\$xdriver"
EndSection
FOE
fi

EOF

chmod 755 /etc/rc.d/init.d/livesys
/sbin/restorecon /etc/rc.d/init.d/livesys
/sbin/chkconfig --add livesys

chmod 755 /etc/rc.d/init.d/livesys-late
/sbin/restorecon /etc/rc.d/init.d/livesys-late
/sbin/chkconfig --add livesys-late

# enable tmpfs for /tmp
systemctl enable tmp.mount

# make it so that we don't do writing to the overlay for things which
# are just tmpdirs/caches
# note https://bugzilla.redhat.com/show_bug.cgi?id=1135475
cat >> /etc/fstab << EOF
vartmp   /var/tmp    tmpfs   defaults   0  0
EOF

# work around for poor key import UI in PackageKit
rm -f /var/lib/rpm/__db*
echo "Packages within this LiveCD"
rpm -qa --qf '%{size}\t%{name}-%{version}-%{release}.%{arch}\n' |sort -rn
# Note that running rpm recreates the rpm db files which aren't needed or wanted
rm -f /var/lib/rpm/__db*

# go ahead and pre-make the man -k cache (#455968)
/usr/bin/mandb

# make sure there aren't core files lying around
rm -f /core*

# remove random seed, the newly installed instance should make it's own
rm -f /var/lib/systemd/random-seed

# convince readahead not to collect
# FIXME: for systemd

echo 'File created by kickstart. See systemd-update-done.service(8).' \
    | tee /etc/.updated >/var/.updated

# Drop the rescue kernel and initramfs, we don't need them on the live media itself.
# See bug 1317709
rm -f /boot/*-rescue*

# Disable network service here, as doing it in the services line
# fails due to RHBZ #1369794
/sbin/chkconfig network off

# Remove machine-id on pre generated images
rm -f /etc/machine-id
touch /etc/machine-id

%end

%post --nochroot
# For livecd-creator builds only (lorax/livemedia-creator handles this directly)
if [ -n "$LIVE_ROOT" ]; then
    cp "$INSTALL_ROOT"/usr/share/licenses/*-release-common/* "$LIVE_ROOT/"

    # only installed on x86, x86_64
    if [ -f /usr/bin/livecd-iso-to-disk ]; then
        mkdir -p "$LIVE_ROOT/LiveOS"
        cp /usr/bin/livecd-iso-to-disk "$LIVE_ROOT/LiveOS"
    fi
fi

%end

%post
# xfce configuration

# create /etc/sysconfig/desktop (needed for installation)

cat > /etc/sysconfig/desktop <<EOF
PREFERRED=/usr/bin/startxfce4
DISPLAYMANAGER=/usr/sbin/lightdm
EOF

cat >> /etc/rc.d/init.d/livesys << EOF

mkdir -p /home/liveuser/.config/xfce4

cat > /home/liveuser/.config/xfce4/helpers.rc << FOE
MailReader=sylpheed-claws
FileManager=Thunar
WebBrowser=firefox
FOE

# disable screensaver locking (#674410)
cat >> /home/liveuser/.xscreensaver << FOE
mode:           off
lock:           False
dpmsEnabled:    False
FOE

# deactivate xfconf-migration (#683161)
rm -f /etc/xdg/autostart/xfconf-migration-4.6.desktop || :

# deactivate xfce4-panel first-run dialog (#693569)
mkdir -p /home/liveuser/.config/xfce4/xfconf/xfce-perchannel-xml
cp /etc/xdg/xfce4/panel/default.xml /home/liveuser/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml

# set up lightdm autologin
sed -i 's/^#autologin-user=.*/autologin-user=liveuser/' /etc/lightdm/lightdm.conf
sed -i 's/^#autologin-user-timeout=.*/autologin-user-timeout=0/' /etc/lightdm/lightdm.conf
#sed -i 's/^#show-language-selector=.*/show-language-selector=true/' /etc/lightdm/lightdm-gtk-greeter.conf

# set Xfce as default session, otherwise login will fail
sed -i 's/^#user-session=.*/user-session=xfce/' /etc/lightdm/lightdm.conf

# Show harddisk install on the desktop
sed -i -e 's/NoDisplay=true/NoDisplay=false/' /usr/share/applications/liveinst.desktop
mkdir /home/liveuser/Desktop
cp /usr/share/applications/liveinst.desktop /home/liveuser/Desktop

# no updater applet in live environment
rm -f /etc/xdg/autostart/org.mageia.dnfdragora-updater.desktop

# and mark it as executable (new Xfce security feature)
chmod +x /home/liveuser/Desktop/liveinst.desktop

# this goes at the end after all other changes. 
chown -R liveuser:liveuser /home/liveuser
restorecon -R /home/liveuser

EOF

%end

%post
cat > /etc/xdg/xfce4/panel/default.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>

<channel name="xfce4-panel" version="1.0">
  <property name="configver" type="int" value="2"/>
  <property name="panels" type="array">
    <value type="int" value="1"/>
    <property name="dark-mode" type="bool" value="true"/>
    <property name="panel-1" type="empty">
      <property name="position" type="string" value="p=8;x=512;y=754"/>
      <property name="length" type="uint" value="100"/>
      <property name="position-locked" type="bool" value="true"/>
      <property name="icon-size" type="uint" value="16"/>
      <property name="size" type="uint" value="26"/>
      <property name="plugin-ids" type="array">
        <value type="int" value="1"/>
        <value type="int" value="2"/>
        <value type="int" value="3"/>
        <value type="int" value="5"/>
        <value type="int" value="6"/>
        <value type="int" value="8"/>
        <value type="int" value="9"/>
        <value type="int" value="10"/>
        <value type="int" value="11"/>
        <value type="int" value="12"/>
        <value type="int" value="13"/>
        <value type="int" value="14"/>
      </property>
    </property>
  </property>
  <property name="plugins" type="empty">
    <property name="plugin-1" type="string" value="applicationsmenu"/>
    <property name="plugin-2" type="string" value="tasklist">
      <property name="grouping" type="uint" value="1"/>
    </property>
    <property name="plugin-3" type="string" value="separator">
      <property name="expand" type="bool" value="true"/>
      <property name="style" type="uint" value="0"/>
    </property>
    <property name="plugin-5" type="string" value="separator">
      <property name="style" type="uint" value="0"/>
    </property>
    <property name="plugin-6" type="string" value="systray">
      <property name="square-icons" type="bool" value="true"/>
      <property name="known-legacy-items" type="array">
        <value type="string" value="seapplet"/>
        <value type="string" value="xfce4-power-manager"/>
        <value type="string" value="connessione ethernet «connessione via cavo 1» attiva"/>
      </property>
    </property>
    <property name="plugin-8" type="string" value="pulseaudio">
      <property name="enable-keyboard-shortcuts" type="bool" value="true"/>
      <property name="show-notifications" type="bool" value="true"/>
    </property>
    <property name="plugin-9" type="string" value="power-manager-plugin"/>
    <property name="plugin-10" type="string" value="notification-plugin"/>
    <property name="plugin-11" type="string" value="separator">
      <property name="style" type="uint" value="0"/>
    </property>
    <property name="plugin-12" type="string" value="clock"/>
    <property name="plugin-13" type="string" value="separator">
      <property name="style" type="uint" value="0"/>
    </property>
    <property name="plugin-14" type="string" value="actions"/>
  </property>
</channel>
EOF
cp /etc/xdg/xfce4/panel/default.xml /home/liveuser/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml

cat >> "$(rpm -ql firefox | grep 'firefox-redhat-default-prefs.js$')" <<EOF
pref("browser.startup.homepage", "http://localhost/");
pref("browser.startup.homepage_override.mstone", "ignore");
pref("datareporting.policy.dataSubmissionEnabled", false);
EOF

mkdir -p /etc/skel/.local/share/applications
cat > /etc/skel/.local/share/applications/serveurlibre.printer.desktop <<EOF
[Desktop Entry]
Type=Application
Name=ServeurLibre printer
Comment=
Exec=/opt/serveurlibre/tools/stampa/scontrino.sh
EOF

cat > /etc/skel/.config/mimeapps.list <<EOF
[Added Associations]
text/plain=serveurlibre.printer.desktop;

[Default Applications]
text/plain=serveurlibre.printer.desktop;
EOF

mkdir /etc/skel/Desktop
ln -s /opt/serveurlibre /etc/skel/Desktop
cp /usr/share/applications/firefox.desktop /etc/skel/Desktop
# and mark it as executable (new Xfce security feature)
chmod +x /etc/skel/Desktop/firefox.desktop

cp -rT /etc/skel /home/liveuser

cat > /lib/systemd/system/serveurlibre.service <<EOF
[Unit]
Description=ServeurLibre
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/opt/serveurlibre
ExecStart=/opt/serveurlibre/manage.py runserver 0.0.0.0:80

[Install]
WantedBy=multi-user.target
EOF

systemctl enable serveurlibre.service

# set NAME=Fedora (liveinst regression)
cat > /usr/lib/os-release << EOF
NAME=Fedora
VERSION="38 (ServeurLibre)"
ID=generic
ID_LIKE=fedora
VERSION_ID=38
PRETTY_NAME="ServeurLibre 38"
ANSI_COLOR="0;34"
LOGO=generic-logo-icon
CPE_NAME="cpe:/o:generic:generic:38"
HOME_URL="https://github.com/frafra/serveurlibre"
EOF
%end

%post --nochroot
mkdir $INSTALL_ROOT/opt/serveurlibre
git clone --recursive . $INSTALL_ROOT/opt/serveurlibre
chown -R root:wheel $INSTALL_ROOT/opt/serveurlibre
chmod g+w $INSTALL_ROOT/opt/serveurlibre/{,*.db,pos/settings.py,static/archivio/localhost}
%end

%packages
@^xfce-desktop-environment
@anaconda-tools
@xfce-apps
@xfce-extra-plugins
aajohan-comfortaa-fonts
anaconda
anaconda-install-env-deps
anaconda-live
chkconfig
dracut-live
generic-logos
generic-release
glibc-all-langpacks
initscripts
kernel
kernel-modules
kernel-modules-extra
langpacks-it
python3-django
system-config-printer
wget
-@x86-baremetal-tools
-@xfce-media
-@xfce-office
-acpid
-aspell-*
-autofs
-desktop-backgrounds-basic
-device-mapper-multipath
-fcoe-utils
-fedora-logos
-fedora-release
-fedora-release-xfce
-gimp-help
-hplip
-isdn4k-utils
-mpage
-sane-backends
-xfce4-eyes-plugin
-xfce4-sensors-plugin
-xsane
-xsane-gimp

%end

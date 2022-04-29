# serveurlibre.ks

%include /usr/share/spin-kickstarts/fedora-live-xfce.ks

# increase space
clearpart --all
part / --fstype="ext4" --size=6144

firewall --enabled --service=mdns,http

# italian language
lang it_IT.UTF-8
keyboard it
timezone Europe/Rome

%packages
langpacks-it

# serveurlibre customization
# branding
-fedora-release
-fedora-logos
generic-release
generic-logos

# dependencies
python3-django

# unneeded groups
-@xfce-media
-@xfce-office
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
%end

%post --nochroot
mkdir $INSTALL_ROOT/opt/serveurlibre
git clone --recursive . $INSTALL_ROOT/opt/serveurlibre
chown -R root:wheel $INSTALL_ROOT/opt/serveurlibre
chmod g+w $INSTALL_ROOT/opt/serveurlibre/{,*.db,pos/settings.py,static/archivio/localhost}
%end

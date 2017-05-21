# serveurlibre.ks

%include /usr/share/spin-kickstarts/fedora-live-xfce.ks

# italian language
lang it_IT.UTF-8
keyboard it
timezone Europe/Rome

%packages
@italian-support

# exclude input methods
-ibus*
-m17n*
-scim*

# serveurlibre customization
# branding
-fedora-release
-fedora-logos
generic-release
generic-logos

# dependencies
python-django
pytz

# unneeded groups
-@xfce-media
-@xfce-office

# libreoffice
libreoffice
libreoffice-langpack-it

# replace Midori with Firefox
-midori
firefox

-abrt*
-claws*
-firewalld
%end

%post
mkdir -p /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/
cat > /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-panel.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
 
<channel name="xfce4-panel" version="1.0">
  <property name="configver" type="int" value="2"/>
  <property name="panels" type="array">
    <value type="int" value="1"/>
    <property name="panel-1" type="empty">
      <property name="position" type="string" value="p=10;x=0;y=0"/>
      <property name="length" type="uint" value="100"/>
      <property name="position-locked" type="bool" value="true"/>
      <property name="size" type="uint" value="30"/>
      <property name="plugin-ids" type="array">
        <value type="int" value="1"/>
        <value type="int" value="3"/>
        <value type="int" value="15"/>
        <value type="int" value="5"/>
        <value type="int" value="6"/>
        <value type="int" value="2"/>
      </property>
    </property>
  </property>
  <property name="plugins" type="empty">
    <property name="plugin-1" type="string" value="applicationsmenu"/>
    <property name="plugin-2" type="string" value="actions"/>
    <property name="plugin-3" type="string" value="tasklist"/>
    <property name="plugin-15" type="string" value="separator">
      <property name="expand" type="bool" value="true"/>
      <property name="style" type="uint" value="0"/>
    </property>
    <property name="plugin-4" type="string" value="pager"/>
    <property name="plugin-5" type="string" value="clock"/>
    <property name="plugin-6" type="string" value="systray"/>
  </property>
</channel>
EOF
cat > /etc/skel/.config/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
 
<channel name="xfwm4" version="1.0">
  <property name="general" type="empty">
    <property name="activate_action" type="string" value="bring"/>
    <property name="borderless_maximize" type="bool" value="true"/>
    <property name="box_move" type="bool" value="false"/>
    <property name="box_resize" type="bool" value="false"/>
    <property name="button_layout" type="string" value="O|SHMC"/>
    <property name="button_offset" type="int" value="0"/>
    <property name="button_spacing" type="int" value="0"/>
    <property name="click_to_focus" type="bool" value="true"/>
    <property name="cycle_apps_only" type="bool" value="false"/>
    <property name="cycle_draw_frame" type="bool" value="true"/>
    <property name="cycle_hidden" type="bool" value="true"/>
    <property name="cycle_minimum" type="bool" value="true"/>
    <property name="cycle_preview" type="bool" value="true"/>
    <property name="cycle_tabwin_mode" type="int" value="0"/>
    <property name="cycle_workspaces" type="bool" value="false"/>
    <property name="double_click_action" type="string" value="maximize"/>
    <property name="double_click_distance" type="int" value="5"/>
    <property name="double_click_time" type="int" value="250"/>
    <property name="easy_click" type="string" value="Alt"/>
    <property name="focus_delay" type="int" value="250"/>
    <property name="focus_hint" type="bool" value="true"/>
    <property name="focus_new" type="bool" value="true"/>
    <property name="frame_opacity" type="int" value="100"/>
    <property name="full_width_title" type="bool" value="true"/>
    <property name="horiz_scroll_opacity" type="bool" value="false"/>
    <property name="inactive_opacity" type="int" value="100"/>
    <property name="maximized_offset" type="int" value="0"/>
    <property name="mousewheel_rollup" type="bool" value="true"/>
    <property name="move_opacity" type="int" value="100"/>
    <property name="placement_mode" type="string" value="center"/>
    <property name="placement_ratio" type="int" value="20"/>
    <property name="popup_opacity" type="int" value="100"/>
    <property name="prevent_focus_stealing" type="bool" value="false"/>
    <property name="raise_delay" type="int" value="250"/>
    <property name="raise_on_click" type="bool" value="true"/>
    <property name="raise_on_focus" type="bool" value="false"/>
    <property name="raise_with_any_button" type="bool" value="true"/>
    <property name="repeat_urgent_blink" type="bool" value="false"/>
    <property name="resize_opacity" type="int" value="100"/>
    <property name="scroll_workspaces" type="bool" value="true"/>
    <property name="shadow_delta_height" type="int" value="0"/>
    <property name="shadow_delta_width" type="int" value="0"/>
    <property name="shadow_delta_x" type="int" value="0"/>
    <property name="shadow_delta_y" type="int" value="-3"/>
    <property name="shadow_opacity" type="int" value="50"/>
    <property name="show_app_icon" type="bool" value="false"/>
    <property name="show_dock_shadow" type="bool" value="true"/>
    <property name="show_frame_shadow" type="bool" value="true"/>
    <property name="show_popup_shadow" type="bool" value="false"/>
    <property name="snap_resist" type="bool" value="false"/>
    <property name="snap_to_border" type="bool" value="true"/>
    <property name="snap_to_windows" type="bool" value="false"/>
    <property name="snap_width" type="int" value="10"/>
    <property name="sync_to_vblank" type="bool" value="false"/>
    <property name="theme" type="string" value="Default"/>
    <property name="tile_on_move" type="bool" value="true"/>
    <property name="title_alignment" type="string" value="center"/>
    <property name="title_font" type="string" value="Sans Bold 9"/>
    <property name="title_horizontal_offset" type="int" value="0"/>
    <property name="titleless_maximize" type="bool" value="false"/>
    <property name="title_shadow_active" type="string" value="false"/>
    <property name="title_shadow_inactive" type="string" value="false"/>
    <property name="title_vertical_offset_active" type="int" value="0"/>
    <property name="title_vertical_offset_inactive" type="int" value="0"/>
    <property name="toggle_workspaces" type="bool" value="false"/>
    <property name="unredirect_overlays" type="bool" value="true"/>
    <property name="urgent_blink" type="bool" value="false"/>
    <property name="use_compositing" type="bool" value="true"/>
    <property name="workspace_count" type="int" value="1"/>
    <property name="workspace_names" type="array">
      <value type="string" value="Spazio di lavoro 1"/>
    </property>
    <property name="wrap_cycle" type="bool" value="true"/>
    <property name="wrap_layout" type="bool" value="true"/>
    <property name="wrap_resistance" type="int" value="10"/>
    <property name="wrap_windows" type="bool" value="true"/>
    <property name="wrap_workspaces" type="bool" value="false"/>
    <property name="zoom_desktop" type="bool" value="true"/>
  </property>
</channel>
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

mkdir -p /etc/skel/.mozilla/firefox/serveurlibre.default
cat > /etc/skel/.mozilla/firefox/profiles.ini <<EOF
[General]
StartWithLastProfile=1

[Profile0]
Name=default
IsRelative=1
Path=serveurlibre.default
Default=1
EOF

cat > /etc/skel/.mozilla/firefox/serveurlibre.default/prefs.js <<EOF
user_pref("browser.startup.homepage", "http://localhost");
EOF

mkdir /etc/skel/Desktop
ln -s /opt/serveurlibre /etc/skel/Desktop
cp /usr/share/applications/firefox.desktop /etc/skel/Desktop
# and mark it as executable (new Xfce security feature)
chmod +x /etc/skel/Desktop/firefox.desktop

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
git clone . $INSTALL_ROOT/opt/serveurlibre
chown -R root:wheel $INSTALL_ROOT/opt/serveurlibre
chmod g+w $INSTALL_ROOT/opt/serveurlibre/{,*.db,pos/settings.py,static/archivio/localhost}
%end

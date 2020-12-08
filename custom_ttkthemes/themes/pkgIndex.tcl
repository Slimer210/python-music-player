# Author: RedFantom
# License: GNU GPLv3
# Copyright (c) 2017-2018 RedFantom

set base_theme_dir [file join [pwd] [file dirname [info script]]]

array set base_themes {
}

foreach {theme version} [array get base_themes] {
  package ifneeded ttk::theme::$theme $version \
    [list source [file join $base_theme_dir $theme $theme.tcl]]
}
